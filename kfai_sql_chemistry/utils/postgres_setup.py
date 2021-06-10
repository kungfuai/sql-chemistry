from sqlalchemy.engine import Engine


def setup_postgres(engine: Engine):
    with engine.connect() as c:
        c.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
