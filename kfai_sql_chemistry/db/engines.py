from typing import Dict

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from kfai_sql_chemistry.db.database_config import DatabaseConfig


class SQLEngineFactory:

    def __init__(self):
        self._engines: Dict[str, Engine] = {}

    def create_all_engines(self, database_map: Dict[str, DatabaseConfig]):
        for db_name in database_map.keys():
            cfg = database_map[db_name]
            # https://docs.sqlalchemy.org/en/13/dialects/mysql.html#charset-selection
            # Mysql requires specific encoding
            if "mysql" in cfg.engine:
                print(cfg.make_url())
                engine: Engine = create_engine(
                    f"{cfg.make_url()}?charset=utf8mb4", pool_recycle=3600
                )
            else:
                engine: Engine = create_engine(cfg.make_url(), pool_recycle=3600)
            self._engines[db_name] = engine

    def get_engine(self, db_name) -> Engine:
        return self._engines[db_name]
