from pydantic import BaseModel
from pydantic_settings import (BaseSettings, SettingsConfigDict,
                               PydanticBaseSettingsSource, YamlConfigSettingsSource)
from typing import Type, Tuple
import os.path

class AWSSession(BaseModel):
    access_key: str
    secret_key: str

class AWSConfig(BaseModel):
    service_name: str
    endpoint_url: str
    region_name: str

class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(yaml_file='boto-orm.yaml')

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (YamlConfigSettingsSource(settings_cls), )


class Configure(BaseConfig):
    session: AWSSession
    db_config: AWSConfig
    s3_config: AWSConfig


if os.path.exists('boto-orm.yaml'):
    config = Configure()
else:
    config = None


# class ConfigENV(BaseSettings):
#     access_key: str
#     secret_key: str
#     region_name: str
#     endpoint_db: str
#     endpoint_s3: str

#     model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

# service = ConfigENV()

# @dataclass
# class AWSSession:
#     access_key: str = service.access_key
#     secret_key: str = service.secret_key

# @dataclass
# class AWSConfig:
#     service_name: Annotated[str, 'dynamodb', 's3']
#     endpoint_url: str
#     region_name: str = service.region_name

# db_config = config.db_config #AWSConfig(service_name='dynamodb', endpoint_url=service.endpoint_db)
# s3_config = config.s3_config #AWSConfig(service_name='s3', endpoint_url=service.endpoint_s3)
# session = co