import os
import unittest
from typing import Dict

import boto3
from kfai_env.environment.register import Environment
from moto import mock_secretsmanager

from kfai_sql_chemistry.aws.aws_db_config import AwsConfig
from kfai_sql_chemistry.db.database_config import DatabaseConfig


def setUpModule():
    os.environ['ENV'] = 'AWS-TEST'


def tearDownModule():
    os.environ['ENV'] = ''


class AWSAutoConfigTest(unittest.TestCase):

    def setUp(self):
        e = Environment('./env')
        e.register_environment("AWS-TEST")
        e.load_env()

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
        conn = boto3.client("secretsmanager", region_name="us-west-1")
        conn.create_secret(
            Name="SOMEFAKESECRETID", SecretString=cfg.to_json()
        )

        database_map: Dict[str, DatabaseConfig] = {
            # Act
            "main": AwsConfig().detect_db_config('main')
        }

        assert database_map['main'] == cfg
