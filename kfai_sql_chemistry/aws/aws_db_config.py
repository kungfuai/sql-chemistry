import logging
import os

import boto3

from kfai_sql_chemistry.aws.secrets import SecretValue
from kfai_sql_chemistry.db.database_config import DatabaseConfig

logger = logging.getLogger(__name__)


def _create_default_client():
    return boto3.client("secretsmanager")


class AwsDbConfig:

    def __init__(self, boto3_secrets_client=None):
        if not boto3_secrets_client:
            self._boto3_secrets_client = _create_default_client()
        else:
            self._boto3_secrets_client = boto3_secrets_client

    def detect_db_config(self, db_name: str) -> DatabaseConfig:
        db_name_str = db_name.upper()
        secret_id_env = f"{db_name_str}_DB_SECRET_ID"
        possible_secret = os.getenv(secret_id_env)
        if possible_secret:
            logger.info(f"create the database config from the db secret id.")
            logger.info(f"A secret ID has been found")
            logger.info(f"Env ID: {possible_secret}")
            logger.info(f"Secret ID: {secret_id_env}")
            return self._get_aws_config(possible_secret)
        else:
            logger.info("create a database config from the local environment.")
            return self._get_local_config(db_name_str)

    def _get_aws_config(self, secret_id) -> DatabaseConfig:
        secret_client = self._boto3_secrets_client
        raw_secret_value = secret_client.get_secret_value(SecretId=secret_id)
        sv = SecretValue(**raw_secret_value)
        return DatabaseConfig.from_json(sv.SecretString)

    def _get_local_config(self, db_name) -> DatabaseConfig:
        return DatabaseConfig.from_local_env(db_name)
