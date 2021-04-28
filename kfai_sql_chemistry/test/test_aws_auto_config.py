import os
import unittest
from typing import Dict

import boto3
from kfai_env import Environment
from moto import mock_secretsmanager

from kfai_sql_chemistry.aws.aws_db_config import AwsDbConfig
from kfai_sql_chemistry.db.database_config import DatabaseConfig


class AWSAutoConfigTest(unittest.TestCase):

    def setUp(self):
        os.environ['ENV'] = 'AWS-TEST'
        e = Environment('./kfai_sql_chemistry/test/env')
        e.register_environment("AWS-TEST")
        e.load_env()

    def tearDown(self):
        os.environ['ENV'] = ''

    @mock_secretsmanager
    def test_autodetect(self):
        cfg = DatabaseConfig(
            username='postgres',
            password='password',
            engine='postgresql',
            host='localhost',
            port=9000,
            db_name='postgres',
            dbname=''
        )
        conn = boto3.client("secretsmanager")
        conn.create_secret(
            Name="SOMEFAKESECRETID", SecretString=cfg.to_json()
        )
        print(conn.get_secret_value(SecretId='SOMEFAKESECRETID'))

        database_map: Dict[str, DatabaseConfig] = {
            "main": AwsDbConfig().detect_db_config('main')
        }

        assert database_map['main'] == cfg

    @mock_secretsmanager
    def test_autodetect_callable_with_session_callable(self):
        cfg = DatabaseConfig(
            username='postgres',
            password='password',
            engine='postgresql',
            host='localhost',
            port=9000,
            db_name='postgres',
            dbname=''
        )
        conn = boto3.client("secretsmanager")
        conn.create_secret(
            Name="SOMEFAKESECRETID", SecretString=cfg.to_json()
        )
        print(conn.get_secret_value(SecretId='SOMEFAKESECRETID'))

        database_map: Dict[str, DatabaseConfig] = {
            "main": AwsDbConfig(
                boto3_secrets_client=lambda: boto3.client("secretsmanager")
            ).detect_db_config('main')
        }

        assert database_map['main'] == cfg

