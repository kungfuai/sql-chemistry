import unittest

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from kfai_sql_chemistry.test.utils.models_for_testing.models import BaseModel
from kfai_sql_chemistry.utils.setup_for_testing import setup_db_for_tests


class TestTestSetup(unittest.TestCase):

    def test_setup_works(self):
        engine: Engine = create_engine('sqlite://')
        setup_db_for_tests(engine, BaseModel.metadata)
        engine.execute("SELECT * FROM person")

        engine: Engine = create_engine('sqlite://')
        try:
            engine.execute("SELECT * FROM person")
        except:
            assert True
        else:
            assert False, "Person somehow exists in the database when it shouldn't"
