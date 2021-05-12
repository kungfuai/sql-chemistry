from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

BaseDbModel = declarative_base()


class CarModel(BaseDbModel):
    __tablename__ = "Car"

    car_id = Column("Id", Integer, primary_key=True, autoincrement=True)
    car_make = Column("Make", String(100))
    car_model = Column("Model", String(100))
    car_year = Column("Year", Integer)
    car_type = Column("Type", String(25))


class DriverModel(BaseDbModel):
    __tablename__ = "Driver"

    driver_id = Column("Id", Integer, primary_key=True, autoincrement=True)
    driver_first_name = Column("FirstName", String(100))
    driver_last_name = Column("LastName", String(100))
    driver_state = Column("State", String(2))