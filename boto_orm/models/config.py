from dataclasses import dataclass
from typing_extensions import Annotated

from pydantic_settings import BaseSettings, SettingsConfigDict

class ConfigENV(BaseSettings):
    access_key: str
    secret_key: str
    region_name: str
    endpoint_db: str
    endpoint_s3: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

service = ConfigENV()

@dataclass
class AWSSession:
    access_key: str = service.access_key
    secret_key: str = service.secret_key

@dataclass
class AWSConfig:
    service_name: Annotated[str, 'dynamodb', 's3']
    endpoint_url: str
    region_name: str = service.region_name

db_config = AWSConfig(service_name='dynamodb', endpoint_url=service.endpoint_db)
s3_config = AWSConfig(service_name='s3', endpoint_url=service.endpoint_s3)