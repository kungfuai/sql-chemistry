from typing import Dict

from kfai_sql_chemistry.query.constructor import QueryConstructor


def construct_query(session):
    return QueryConstructor.join(session)


