import os
import unittest
from typing import Dict

import boto3
from kfai_env import Environment
from moto import mock_secretsmanager

from kfai_sql_chemistry.aws.aws_db_config import AwsDbConfig
from kfai_sql_chemistry.db.database_config import DatabaseConfig
from kfai_sql_chemistry.utils.setup_for_testing import setup_db_for_tests


class QueryConstructorTest(unittest.TestCase):

    def setUp(self):
        os.environ['ENV'] = 'AWS-TEST'
        e = Environment('./kfai_sql_chemistry/test/env')
        e.register_environment("AWS-TEST")
        e.load_env()

    def tearDown(self):
        os.environ['ENV'] = ''


    # start the database session as session here

    VehicleTestDbModel = declarative_base()

    class CarModel(VehicleTestDbModel):
        __tablename__ = "Car"

        car_id = Column("CarId", Integer, primary_key=True, autoincrement=True)
        car_make = Column("CarMake", String(100))
        car_model = Column("CarModel", String(100))
        car_year = Column("CarYear", Integer)
        car_type = Column("CarType", String(25))

    class DriverModel(VehicleTestDbModel):
        __tablename__ = "Driver"

        driver_id = Column("DriverId", Integer, primary_key=True, autoincrement=True)
        driver_first_name = Column("DriverFirstName", String(100))
        driver_last_name = Column("DriverLastName", String(100))
        driver_state = Column("DriverState", String(2))

    test = engines.get_engine("test_db")
    setup_db_for_tests(test, VehicleTestDbModel.metadata)

    # figure out how to handle inputs
    QueryConstructor.join(session)

