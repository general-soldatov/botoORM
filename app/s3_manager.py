from typing import Dict, Optional, Union, List, Any
from app.models.client import Client
from app.models.config import AWSConfig, AWSSession, db_config


class S3Manager(Client):
    def __init__(self, bucket_name: str, config: Union[AWSConfig, dict] = db_config, session_aws: Union[AWSSession, dict] = AWSSession()):
        super().__init__(bucket_name, config, session_aws)

    def put_object(self):
        return self.client
