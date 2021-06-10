from enum import Enum

from sqlalchemy.engine import Engine

from kfai_sql_chemistry.utils.postgres_setup import setup_postgres


def db_setup(engine: Engine):
    if 'postgres' in engine.name:
        setup_postgres(engine)
