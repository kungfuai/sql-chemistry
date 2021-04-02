import os
import unittest
from typing import Dict

from kfai_env import Environment

from kfai_sql_chemistry.db.database_config import DatabaseConfig
from kfai_sql_chemistry.db.engines import SQLEngineFactory


def setUpModule():
    os.environ['ENV'] = 'TEST'


def tearDownModule():
    os.environ['ENV'] = ''


class CreateDbConnectionTest(unittest.TestCase):

    def setUp(self):
        e = Environment('./kfai_sql_chemistry/test/env')
        e.register_environment("TEST")
        e.load_env()

    @unittest.skip("Skip until we run databases in github actions")
    def test_registration_and_access(self):
        database_map: Dict[str, DatabaseConfig] = {
            "main": DatabaseConfig.from_local_env("main")
        }

        factory = SQLEngineFactory()
        factory.create_all_engines(database_map)

        engine = factory.get_engine("main")

        with engine.connect() as conn:
            print(conn.execute("SELECT 1").fetchall())
