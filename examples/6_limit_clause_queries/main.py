from db_init import initialize_db, PetSession
from add_tables_to_db import add_data_to_tables
from models.kfai_pets_model import OfficePetModel

# connect to our database with sqlalchemy
initialize_db("pet")

# create sample data and add to our tables
add_data_to_tables()


if __name__ == "__main__":

    """ Example code for using the LIMIT clause with SQLAlchemy ORM"""
    # let's say we wanted to get only three rows from the office pet table
    # this shows how we can use limit to get certain columns with SQLAlchemy ORM
    with PetSession() as session:
        result = (
            session.query(
                OfficePetModel.pet_breed,
                OfficePetModel.allowed_in_office
            )
            .limit(3))
        session.expunge_all()
        print("LIMIT clause")
        print([r for r in result])