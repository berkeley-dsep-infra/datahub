import os
import sys

from sign_url_and_send_emails import authenticate_gmail_api, create_message


NEW_REQUEST_URL = "https://github.com/berkeley-dsep-infra/datahub/issues/new?template=data_archival_request.yml"
SUPPORT_EMAIL = "datahub-dataretrieval@berkeley.edu"

FIND_LINK_STEPS = f"""To find the link to your files:
1. Log into the hub you used, for example https://datahub.berkeley.edu, https://data8.datahub.berkeley.edu or https://r.datahub.berkeley.edu.
2. Open the WHERE-ARE-MY-FILES.txt file in your home directory.
3. Copy the URL inside WHERE-ARE-MY-FILES.txt into your browser. This opens a new data retrieval request.
4. Fill in your UC Berkeley email address and submit the request.

If you no longer have access to the hub where WHERE-ARE-MY-FILES.txt is stored, or if you lost access to bCourses, please contact {SUPPORT_EMAIL}."""

MESSAGES = {
    "no_link": f"""Your data retrieval request did not include a valid link to your archived files, so we could not process it. Please submit a new request with a valid link.

{FIND_LINK_STEPS}""",
    "no_email": f"""Your data retrieval request did not include a UC Berkeley email address (ending in @berkeley.edu), so we could not process it. Please submit a new request with your UC Berkeley email address: {NEW_REQUEST_URL}""",
    "mismatch": f"""Some of the links in your data retrieval request do not match the owner of the email address you provided, so we could not process it. Please double check your email address and the links to your files, and submit a new request with the correct information: {NEW_REQUEST_URL}""",
    "send_error": f"""We could not complete your data retrieval request automatically. Please contact {SUPPORT_EMAIL} for help.""",
}


def main():
    failure_type = os.getenv("FAILURE_TYPE")
    recipient = os.getenv("CONTACT_EMAIL")
    if failure_type not in MESSAGES or not recipient:
        print(f"Nothing to send for failure type {failure_type!r}")
        sys.exit(1)

    service = authenticate_gmail_api()
    if not service:
        sys.exit(1)

    body = f"""Hello,

This is an automated email about your DataHub data retrieval request.

{MESSAGES[failure_type]}

For your privacy, your GitHub request has been moved to a private repository, and you will not be able to access it. Please submit a new request instead of replying to the old one.

Best,
DataHub Support Team"""
    message = create_message(SUPPORT_EMAIL, recipient, "Your DataHub data retrieval request could not be processed", body)
    sent_message = service.users().messages().send(userId="me", body=message).execute()
    print(f"Feedback email sent! Message ID: {sent_message['id']}")


if __name__ == "__main__":
    main()
