import os

from email_reader import EmailReader, Parameters
from envs import (
    PARAMETER_STORE_EMAIL,
    PARAMETER_STORE_EMAIL_PASSWORD,
    PARAMETER_STORE_LAST_EMAIL_ID_READ,
)
from sns import SNS


def lambda_handler(event, context):
    print(f"Event ==> {event}")
    print(f"Context ==> {context}")

    sns = SNS()
    reader = EmailReader(Parameters(**event["parameterStore"]))
    emails = reader.read_emails()
    if emails:
        for email in emails:
            print(f"Sending email ({email})...")
            sns.send_message(email, reader.email)
        max_id = max(emails, key=lambda email: email.id).id
        reader.update_latest_email_read(int(max_id.decode('ascii')))

if(os.getenv('LOCAL_DEVELOPMENT') == 'TRUE'):
   print("---- Running the code locally ----")
   lambda_handler({
       "parameterStore": {
           "lastEmailIdRead": PARAMETER_STORE_LAST_EMAIL_ID_READ,
           "email": PARAMETER_STORE_EMAIL,
           "password": PARAMETER_STORE_EMAIL_PASSWORD,
          }
    }, None)