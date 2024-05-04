import boto3
from email_reader import Email
from envs import AWS_REGION, SNS_TOPIC_ARN

sns = boto3.client('sns', region_name=AWS_REGION)

class SNS:
    def send_message(email: Email, original_email: str) -> None:
        try:
            sns.publish(
                TargetArn=SNS_TOPIC_ARN,
                Subject=f"[{email.sender}] {email.title}",
                Message=f"Check email content in the {original_email} email."
            )

        except Exception as e:
            print(f'Error publish message to topic: {str(e)}')
