import logging
from sqlalchemy.orm import session
from typing import List, ClassVar


logger = logging.getLogger(__name__)


def select_columns(model, columns: List[ClassVar]):
    return session.query(model[columns[0]], model[columns[1]], model[columns[2]])


def filter_column(model, column, value):
    return session.query(model).filter(model[column] == value).all()


def exclude_values(model, column, exclusion_list: List[str]):
    return session.query(model).filter(~model[column]._in(exclusion_list))


def relationship_join(primary_key_model, foreign_key_model):
    return session.query(primary_key_model).join(foreign_key_model).all()


