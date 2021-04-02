import os
from dataclasses import dataclass
from typing import Optional

from dataclasses_json import LetterCase, Undefined, dataclass_json
from sqlalchemy.engine.url import URL


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
        return DatabaseConfig(
            username=os.getenv(f"{prefix_caps}_DB_USERNAME"),
            password=os.getenv(f"{prefix_caps}_DB_PASSWORD"),
            engine=os.getenv(f"{prefix_caps}_DB_ENGINE"),
            host=os.getenv(f"{prefix_caps}_DB_HOST"),
            port=int(os.getenv(f"{prefix_caps}_DB_PORT")),
            db_name=os.getenv(f"{prefix_caps}_DB_NAME"),
        )

    def make_url(self):
        return URL(
            self.engine,
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.dbname or self.db_name,
        )
