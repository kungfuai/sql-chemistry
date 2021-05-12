from typing import List

import logging

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import text

from kfai_sql_chemistry.db.main import engines

logger = logging.getLogger(__name__)


class QueryConstructor:
    def __init__(self, column: str, table_name: str, value:str):
        self._column = column
        self._table_name = table_name
        self._values = value

    def join(self, session):
        #statement = self._table_name.join(self._column)
        #statement = '''select * from Car'''
        return session.query(self._table_name).join(self._column).all()



