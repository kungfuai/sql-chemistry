from sqlalchemy import inspect
from sqlalchemy.engine import Engine
from sqlalchemy.schema import (DropConstraint, DropTable, ForeignKeyConstraint, MetaData, Table)

from kfai_sql_chemistry.utils.db_setup import db_setup


def setup_db_for_tests(engine, metadata):
    db_setup(engine)
    metadata.create_all(engine)


def tear_down_db_for_tests(engine):
    _drop_everything(engine)


def _drop_everything(engine: Engine):
    # From http://www.sqlalchemy.org/trac/wiki/UsageRecipes/DropEverything

    conn = engine.connect()

    # the transaction only applies if the DB supports
    # transactional DDL, i.e. Postgresql, MS SQL Server
    trans = conn.begin()

    # inspector = reflection.Inspector.from_engine(engine)
    inspector = inspect(engine)
    # gather all data first before dropping anything.
    # some DBs lock after things have been dropped in
    # a transaction.
    metadata = MetaData()

    tbs = []
    all_fks = []

    for table_name in inspector.get_table_names():
        fks = []
        for fk in inspector.get_foreign_keys(table_name):
            if not fk['name']:
                continue
            fks.append(
                ForeignKeyConstraint((), (), name=fk['name'])
            )
        t = Table(table_name, metadata, *fks)
        tbs.append(t)
        all_fks.extend(fks)

    for fkc in all_fks:
        conn.execute(DropConstraint(fkc))

    for table in tbs:
        conn.execute(DropTable(table))

    trans.commit()
