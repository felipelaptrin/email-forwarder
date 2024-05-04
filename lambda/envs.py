import os

AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
SNS_TOPIC_ARN = os.getenv('SNS_TOPIC_ARN')

# All the Env Vars below are used locally to test the code but in AWS it will be passed 
# as an event by the EventBridge (cron-based triggered)
PARAMETER_STORE_LAST_EMAIL_ID_READ = os.getenv('PARAMETER_STORE_LAST_EMAIL_ID_READ')
PARAMETER_STORE_EMAIL = os.getenv('PARAMETER_STORE_EMAIL')
PARAMETER_STORE_EMAIL_PASSWORD = os.getenv('PARAMETER_STORE_EMAIL_PASSWORD')
