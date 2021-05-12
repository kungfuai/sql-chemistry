import os
import unittest
from typing import Dict

import boto3
from kfai_env import Environment
from moto import mock_secretsmanager

from kfai_sql_chemistry.aws.aws_db_config import AwsDbConfig
from kfai_sql_chemistry.db.database_config import DatabaseConfig
from kfai_sql_chemistry.db.main import engines, register_databases
from kfai_sql_chemistry.test.query.models import BaseDbModel
from kfai_sql_chemistry.utils.setup_for_testing import setup_db_for_tests


class QueryConstructorTest(unittest.TestCase):

    def setUp(self):
        os.environ['ENV'] = 'TEST'
        e = Environment('./kfai_sql_chemistry/test/env')
        e.register_environment("TEST")
        e.load_env()

        database_map: Dict[str, DatabaseConfig] = {
            "test": DatabaseConfig.from_local_env("main")
        }

        register_databases(database_map)

        engine = engines.get_engine("main")
        setup_db_for_tests(engine, BaseDbModel.metadata)

    def tearDown(self):
        os.environ['ENV'] = ''

    def test_something(self):
        pass






    test = engines.get_engine("test_db")
    setup_db_for_tests(test, VehicleTestDbModel.metadata)

    # figure out how to handle inputs
    QueryConstructor.join(session)

