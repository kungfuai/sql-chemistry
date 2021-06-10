import os
from dataclasses import dataclass
from typing import Optional

from dataclasses_json import LetterCase, Undefined, dataclass_json
from sqlalchemy.engine.url import URL


def _engine_string_transform(engine_name):
    if "postgres" in engine_name:
        # SQL Alchemy expects 'postgresql' if the engine is postgres.
        return "postgresql"
    return engine_name


@dataclass_json(letter_case=LetterCase.CAMEL, undefined=Undefined.EXCLUDE)
@dataclass
class DatabaseConfig:
    username: str
    password: str
    engine: str
    host: str
    port: int
    db_name: Optional[str] = ""
    dbname: Optional[str] = ""

    @staticmethod
    def from_local_env(prefix_str: str):
        prefix_caps = prefix_str.upper()
        cfg = DatabaseConfig(
            username=os.getenv(f"{prefix_caps}_DB_USERNAME"),
            password=os.getenv(f"{prefix_caps}_DB_PASSWORD"),
            engine=os.getenv(f"{prefix_caps}_DB_ENGINE"),
            host=os.getenv(f"{prefix_caps}_DB_HOST"),
            port=int(os.getenv(f"{prefix_caps}_DB_PORT")),
            db_name=os.getenv(f"{prefix_caps}_DB_NAME"),
        )
        return cfg

    def make_url(self, query=None):
        return URL(
            _engine_string_transform(self.engine),
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.dbname or self.db_name,
            query=query
        )
