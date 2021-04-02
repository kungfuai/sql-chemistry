from typing import Dict

from kfai_env.environment.register import Environment

from kfai_sql_chemistry.aws.aws_db_config import AwsDbConfig
from kfai_sql_chemistry.db.database_config import DatabaseConfig

# Setup this object ahead of time
from kfai_sql_chemistry.db.main import register_databases

Environment('./env').load_env()

cfg = AwsDbConfig()

database_map: Dict[str, DatabaseConfig] = {
    "main": cfg.detect_db_config("main"),
}

if __name__ == "__main__":
    # Call Register at the beginning of your application
    register_databases(database_map)

