#!/bin/bash

# set -e

# all hub configuration
config_values="/etc/jupyterhub/config/values.yaml"

# output location
profile_dir="/srv/jupyterhub/profiles.d"

course_emails="/usr/local/bin/course-emails.py"

# space 24 hours apart; TODO: guessing k8s can loop this for us somehow
sleep_time=86400

while true ; do

	if [ ! -f $config_values ]; then
		echo "No such file: $config_values"
	else

		if [ ! -d $profile_dir ]; then mkdir -p $profile_dir ; fi

		profiles=`cat ${config_values} | yq .custom.profiles | jq -r 'keys[]'`
		echo profiles: ${profiles}

		# write out email lists for each profile
		for profile in ${profiles} ; do
			for people in students instructors ; do
				filename="${profile_dir}/${profile}-${people}.txt"
				# write to tempfile because gathering addresses takes time
				# and we don't want the hub to read an abbreviated list
				outfile=`mktemp`
				echo $profile $people $outfile
				$course_emails $profile $people > $outfile
				if [ -f $outfile ]; then mv $outfile $filename ; fi
			done
		done
	fi

	sleep $sleep_time
done
