import logging

from sqlalchemy.orm import Session, sessionmaker

from kfai_sql_chemistry.db.main import engines

logger = logging.getLogger(__name__)


class AppSession:
    def __init__(self, db_name: str):
        self._engine = engines.get_engine(db_name)
        self._session_instance = self._create_session()

    def _create_session(self) -> Session:
        session_obj = sessionmaker()
        session_obj.configure(bind=self._engine)
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
        if exc_type:
            logger.error("Exception found: Rollback Transaction")
            self.instance.rollback()

        self.instance.close()

