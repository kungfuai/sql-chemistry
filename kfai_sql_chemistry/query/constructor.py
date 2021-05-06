from typing import List

import logging

from sqlalchemy.orm import Session, sessionmaker

from kfai_sql_chemistry.db.main import engines

logger = logging.getLogger(__name__)


class QueryConstructor:
    def __init__(self, column: str, table_name: str, value:str):
        self._column = column
        self._table_name = table_name
        self._values = value

    def execute_session(session, statement):
        result = session.execute(statement)
        return result

    def filter(self, session, _values: List[int]) -> List[str]:
        statement = (self._table_name).filter(self._column.in_(self._values)).all()
        return self.execute_session(session, statement)

    def join(self, session):
        statement = (self._table_name).join(self._column)
        return self.execute_session(session, statement)

    def order(self, session):
        statement = (self._table_name).order_by(self._column)
        return self.execute_session(session, statement)

    def group(self, session):
        statement = (self._table_name).group_by(self._column)
        return self.execute_session(session, statement)
