from typing import Dict

from kfai_sql_chemistry.db.database_config import DatabaseConfig
from kfai_sql_chemistry.db.engines import SQLEngineFactory

_db_map: Dict[str, DatabaseConfig] = {}
engines = SQLEngineFactory()


def register_databases(db_map: Dict[str, DatabaseConfig]):
    """
    Use this function to start up your application.
    :return:
    """
    global _db_map
    _db_map = db_map
    engines.create_all_engines(_db_map)

