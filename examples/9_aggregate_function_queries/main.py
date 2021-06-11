from sqlalchemy import distinct

from db_init import initialize_db, PetSession
from add_tables_to_db import add_data_to_tables
from models.kfai_pets_model import PetModel, EmployeeModel, OfficePetModel
from sqlalchemy.sql import func

# connect to our database with sqlalchemy
initialize_db("pet")

# create sample data and add to our tables
add_data_to_tables()


if __name__ == "__main__":

    """ Example code for using the aggregate functions with SQLAlchemy ORM"""
    # let's say we wanted to get the count of pet_names in the pet table
    # this shows how we can use count to get that answer using SQLAlchemy ORM
    with PetSession() as session:
        result = (
            session.query(func.count(PetModel.pet_name))
        )
        session.expunge_all()
        print("COUNT function using func")
        print(result)

    # there is also an easier way to do a simple count
    with PetSession() as session:
        result = (
            session.query(PetModel.pet_name)
            .count()
        )
        session.expunge_all()
        print("COUNT function simple format")
        print(result)

    # let's say we want to get a count of distinct pet species from our pet table
    # we can just use the distinct after func.count()
    with PetSession() as session:
        result = (
            session.query(func.count(PetModel.pet_species))
            .distinct()
        )
        session.expunge_all()
        print("COUNT DISTINCT function using func")
        print(result)

    # let's say we want to get a count of distinct pet species from our pet table
    # we can just use the distinct after func.count()
    with PetSession() as session:
        result = (
            session.query(distinct(PetModel.pet_species)).count()
        )
        session.expunge_all()
        print("COUNT DISTINCT function simple format")
        print(result)