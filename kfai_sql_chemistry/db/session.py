import logging
import time
from contextlib import contextmanager

import typing

from sqlalchemy.orm import Session, sessionmaker

from kfai_sql_chemistry.db.main import engines

logger = logging.getLogger(__name__)


class AppSession:
    def __init__(self, db_name: str):
        self._engine = engines.get_engine(db_name)
        self._session_instance = self._create_session()

    def _create_session(self) -> Session:
        session_obj = sessionmaker()
        # create a configured "Session" class
        session_obj.configure(bind=self._engine)
        # create a Session
        return session_obj()

    @property
    def instance(self) -> Session:
        return self._session_instance

    @property
    def engine(self):
        return self._engine

    def __enter__(self):
        return self.instance

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.instance.close()


@contextmanager
def DBContext(db_name: str) -> typing.ContextManager[Session]:
    """
    Use the DatabaseEnum to select the database you want to use
    :param enum:
    :return:
    """
    session = AppSession(db_name)
    try:
        yield session.instance
        session.instance.commit()
    except Exception as err:
        logger.error(f"Failed to perform query: {err}")
        session.instance.rollback()
        raise err
    finally:
        session.instance.close()


class RawDBQuery:
    def __init__(self, db_name):
        self._total_retries = 10
        self._db_name = db_name

    def execute(self, query):
        return self._do_query(query, self._total_retries)

    def _do_query(self, query, retries):
        if retries < 0:
            raise

        engine = engines.get_engine(self._db_name)
        connection = engine.connect()  # replace your connection
        try:
            return connection.execute(query)
        except Exception as err:  # may need more exceptions here (or trap all)
            connection.close()
            logger.error("Failed to perform query, will do retry")
            logger.error(err)
            # wait before retry
            time.sleep(5)
            self._do_query(query, retries - 1)
        finally:
            connection.close()
