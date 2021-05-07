from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

BaseDbModel = declarative_base()


class CarModel(BaseDbModel):
    __tablename__ = "Car"

    id = Column("Id", Integer, primary_key=True, autoincrement=True)
    make = Column("Make", String(100))
    model = Column("Model", String(100))
    year = Column("Year", Integer)
    type = Column("Type", String(25))


class DriverModel(BaseDbModel):
    __tablename__ = "Driver"

    id = Column("Id", Integer, primary_key=True, autoincrement=True)
    first_name = Column("FirstName", String(100))
    last_name = Column("LastName", String(100))
    state = Column("State", String(2))