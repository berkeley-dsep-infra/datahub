#!/usr/bin/python3.7

import argparse
import asyncio
import logging
import os
import shutil
import sys
import time
import tempfile

# We use f-strings from python >= 3.6.
assert sys.version_info >= (3, 6)

from ruamel.yaml import YAML
yaml = YAML(typ='safe')

from sis import classes, enrollments, student, terms
from ucbhr import info as ucbhr_info
 
# logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger('fetch-course-emails')

def parse_course(course):
	'''Parse {year}-{semester}-{class_number}.'''
	year, semester, class_number = course.split('-', 3)
	# type check
	year = int(year) ; class_number = int(class_number)
	semester = semester.lower()
	# validate semester
	semesters = ['summer', 'spring', 'fall']
	assert semester in semesters, f"{semester} not one of {semesters}"
	return year, semester, class_number

async def instructor_emails(term_id, class_number):
	'''Return the business emails of instructors for courses matching
	   {term_id} and {class_number.'''
	# get the instructors of our course. sis only has their uids, not emails.
	uids = await classes.get_instructors(
		SIS_CLASSES_ID, SIS_CLASSES_KEY,
		term_id, class_number, include_secondary='true'
	)

	# ask hr for the emails
	emails = set()
	for uid in uids:
		# get all emails
		items = await ucbhr_info.get(UCB_HR_ID, UCB_HR_KEY, uid, 'campus-uid')
		# extract the business (berkeley.edu) addresses
		hr_emails = set(ucbhr_info.emails(items, 'BUSN'))
		emails |= hr_emails
		logger.debug(f"HR emails: {hr_emails}")
		# also look up their student emails in SIS; students' emails
		# aren't in HR apparently, even if they're employed as GSIs
		sis_emails = set(
			await student.get_emails(SIS_STUDENTS_ID, SIS_STUDENTS_KEY, uid)
		)
		logger.debug(f"SIS emails: {sis_emails}")
		emails |= sis_emails
	return emails

async def student_emails(term_id, class_number):
	'''Return the campus emails of students in courses matching
	   {term_id} and {class_number.'''
	# get the data for all sections for the specified course
	sections = await classes.get_sections_by_id(
		SIS_CLASSES_ID, SIS_CLASSES_KEY, term_id, class_number,
		include_secondary='true'
	)

	emails = set()
	for section in sections:
		section_id = enrollments.section_id(section)

		section_enrollments = await enrollments.get_section_enrollments(
			SIS_ENROLLMENTS_ID, SIS_ENROLLMENTS_KEY,
			term_id, section_id)

		# extract the unique student email addresses (students can be in the
		# main section as well as the lab, discussions, etc.)
		emails |= set(enrollments.get_enrollment_emails(section_enrollments))
		
	return emails

def read_profiles(values_file):
	'''Return the custom.profiles names from jupyterhub config values.'''
	if not os.path.exists(values_file):
		print(f"No such file: {values}")
		return

	values = yaml.load(open(values_file).read())
	if 'custom' not in values:
		print("No 'custom' in values.yaml.")
		return []
	if 'profiles' not in values['custom']:
		print("No 'custom.profiles' in values.yaml.")
		return []

	return list(values['custom']['profiles'].keys())

def save_emails(profile_dir, profile, people, emails):
	'''Save the list of emails into the profile directory.'''
	filename = os.path.join(profile_dir, f"{profile}-{people}.txt")
	with tempfile.NamedTemporaryFile(mode='w', delete=False) as fp:
		for email in emails: fp.write(email + '\n')
	if not os.path.exists(profile_dir):
		os.mkdir(profile_dir)
	shutil.move(fp.name, filename)
	logger.info(f"saved {filename}")

async def handle_profile(profile, profile_dir):
	year, semester, class_number = parse_course(profile)

	# fetch the SIS term id, e.g. 2195
	term_id = await terms.get_term_id_from_year_sem(
		SIS_TERMS_ID, SIS_TERMS_KEY, year, semester
	)
	term_id = int(term_id)
	logger.debug(f"{year} {term_id} {class_number}")

	s_emails = await student_emails(term_id, class_number)
	save_emails(profile_dir, profile, 'students', s_emails)
	i_emails = await instructor_emails(term_id, class_number)
	save_emails(profile_dir, profile, 'instructors', i_emails)

async def main():
	logging.basicConfig(stream=sys.stdout)
	logger = logging.getLogger()
	logger.setLevel(logging.ERROR)

	# check for creds in environment and set them as global vars
	required_env_vars = [
			'SIS_CLASSES_ID', 'SIS_CLASSES_KEY',
		'SIS_ENROLLMENTS_ID', 'SIS_ENROLLMENTS_KEY',
		   'SIS_STUDENTS_ID', 'SIS_STUDENTS_KEY',
			  'SIS_TERMS_ID', 'SIS_TERMS_KEY',
				 'UCB_HR_ID', 'UCB_HR_KEY',
	]
	for v in required_env_vars:
		assert v in os.environ, f"{v} not defined in environment."
		globals()[v] = os.environ[v]

	# arg parsing
	parser = argparse.ArgumentParser(
        description="Get UCB course enrollee and instructor email addresses.")
	parser.add_argument('-d', dest='debug', action='store_true',
		help='set debug log level')
	parser.add_argument('-v', dest='verbose', action='store_true',
		help='set info log level')
	parser.add_argument('-c', '--values',
		default='/etc/jupyterhub/config/values.yaml',
		help='path to jupyterhub config values')
	parser.add_argument('-p', '--profile_dir',
		default='/srv/jupyterhub/profiles.d',
		help='path to profiles output directory')
	args = parser.parse_args()
	
	if args.debug:
		logger.setLevel(logging.DEBUG)
	elif args.verbose:
		logger.setLevel(logging.INFO)

	while True:
		# read custom.profiles from jupyterhub config values
		profiles = read_profiles(args.values)
		for profile in profiles:
			# don't bail on bad profiles
			try:
				await handle_profile(profile, args.profile_dir)
			except Exception as e:
				print(f'Error: {e}')
				continue

		time.sleep(86400)

# main
asyncio.run(main())
