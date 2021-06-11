from sqlalchemy.orm import load_only
from db_init import initialize_db, PetSession
from add_tables_to_db import add_data_to_tables

from models.kfai_pets_model import OfficePetModel

# connect to our database with sqlalchemy
initialize_db("pet")

# create sample data and add to our tables
add_data_to_tables()


if __name__ == "__main__":

    """ Example code for using the SELECT clause with SQLAlchemy ORM"""
    # let's say we wanted to get only the pet_breed and allowed_in_office columns for the office_pet table
    # this shows how we can use select to get certain columns using query function in SQLAlchemy ORM
    with PetSession() as session:
        result = (
            session.query(
                OfficePetModel.pet_breed,
                OfficePetModel.allowed_in_office
            ).all())
        session.expunge_all()
        print("SELECT clause")
        print([r for r in result])

    # let's say that we wanted to get only the pet_breed and allowed_in_office columns a different way
    # this shows howe can use options in SQLAlchemy ORM to get certain columns
    with PetSession() as session:
        result = (
            session.query(OfficePetModel)
                .options(load_only("pet_breed", "allowed_in_office"))
                .all())
        session.expunge_all()
        print("SELECT with load_only")
        print([r for r in result])

    # let's say that we wanted to rename the pet_breed and allowed_in_office columns to be shorter
    # this shows how to rename columns using label in SQLAlchemy ORM, which is like "AS" in SQL
    with PetSession() as session:
        result = (
            session.query(
                OfficePetModel.pet_breed.label("breed"),
                OfficePetModel.allowed_in_office.label("allowed")
            ).all())
        print("SELECT AS clause")
        print(result[0].keys())








