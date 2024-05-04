import boto3
from envs import AWS_REGION

ssm = boto3.client('ssm', region_name=AWS_REGION)

class ParameterStore:

    def get_parameter(self, name: str) -> str:
        try:
            response = ssm.get_parameter(Name=name)
            value = response['Parameter']['Value']
            return value.strip()

        except Exception as e:
            print(f'Error fetching parameter from SSM Parameter Store: {str(e)}')

    def update_parameter(self, name: str, value: str) -> None:
        try:
            ssm.put_parameter(
                Name=name,
                Value=value,
                Overwrite=True
            )
        except Exception as e:
            print(f'Error trying to update parameter from SSM Parameter Store: {str(e)}')