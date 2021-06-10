import os
from kfai_env import Environment
from kfai_sql_chemistry.db.database_config import DatabaseConfig
from kfai_sql_chemistry.db.main import register_databases, engines
from kfai_sql_chemistry.db.session import AppSession
from models.pets_model import BaseDbModel
from env.database_enum import DatabaseEnum


def initialize_db():
    os.environ['ENV'] = 'local'
    e = Environment('env')
    e.load_env()

    database_map = {
        DatabaseEnum.PET.value: DatabaseConfig.from_local_env(DatabaseEnum.PET.value)
    }

    register_databases(database_map)

    BaseDbModel.metadata.drop_all(engines.get_engine("pet"))
    BaseDbModel.metadata.create_all(engines.get_engine("pet"))


def PetSession():
    return AppSession(DatabaseEnum.PET.value)


