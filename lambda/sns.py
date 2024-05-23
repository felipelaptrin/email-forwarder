import boto3
from email_reader import Email
from envs import AWS_REGION, SNS_TOPIC_ARN

sns = boto3.client('sns', region_name=AWS_REGION)

class SNS:
    def __init__(self):
        self.AWS_MAX_SIZE_SUBJECT = 100  # Subjects must be UTF-8 text with no line breaks or control characters, and less than 100 characters long.

    def send_message(self, email: Email, original_email: str) -> None:
        try:
            subject = f"[{email.sender}] {email.title}"[0:self.AWS_MAX_SIZE_SUBJECT]
            print(f"Final email Subject => {subject}")
            sns.publish(
                TargetArn=SNS_TOPIC_ARN,
                Subject=subject,
                Message=f"Check email content in the {original_email} email."
            )

        except Exception as e:
            msg = f'Error publish message to topic: {str(e)}'
            print(msg)
            raise Exception(msg)
