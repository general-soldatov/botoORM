from dataclasses import dataclass
from os import getenv
from dotenv import load_dotenv
from typing_extensions import Annotated

load_dotenv()

@dataclass
class AWSSession:
    access_key: str = getenv('AWS_ACCESS_KEY_ID')
    secret_key: str = getenv('AWS_SECRET_ACCESS_KEY')

@dataclass
class AWSConfig:
    service_name: Annotated[str, 'dynamodb', 's3']
    endpoint_url: str
    region_name: str = getenv('AWS_DEFAULT_REGION')

db_config = AWSConfig(service_name='dynamodb', endpoint_url=getenv('ENDPOINT'))
s3_config = AWSConfig(service_name='s3', endpoint_url=getenv('ENDPOINT_STORAGE'))