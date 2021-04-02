from typing import Dict

from kfai_env.environment.register import Environment

from kfai_sql_chemistry.db.database_config import DatabaseConfig

# Setup this object ahead of time
from kfai_sql_chemistry.db.main import register_databases
from kfai_sql_chemistry.db.session import AppSession

e = Environment('./env')
e.load_env()

database_map: Dict[str, DatabaseConfig] = {
    "main": DatabaseConfig.from_local_env("main"),
    "other": DatabaseConfig.from_local_env("other")
}

if __name__ == "__main__":
    # Call Register at the beginning of your application
    register_databases(database_map)

    with AppSession("main") as session:
        print(session.execute("SELECT 1").fetchall())

    with AppSession("other") as session:
        print(session.execute("SELECT 1").fetchall())
