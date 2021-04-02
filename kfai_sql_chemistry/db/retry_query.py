import logging
import time

from kfai_sql_chemistry.db.main import engines

logger = logging.getLogger(__name__)


class RetryQuery:
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
