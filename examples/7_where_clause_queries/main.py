from sqlalchemy import not_, and_
from db_init import initialize_db, PetSession
from add_tables_to_db import add_data_to_tables

from models.kfai_pets_model import OfficePetModel, PetModel, InsuranceModel

# connect to our database with sqlalchemy
initialize_db("pet")

# create sample data and add to our tables
add_data_to_tables()


if __name__ == "__main__":

    """ Example code for using the WHERE clause with SQLAlchemy ORM"""
    # let's say we wanted to know which pet breeds are allowed in the office (or, where allowed_in_office = True)
    # this shows how we can use filter to get certain columns using SQLAlchemy ORM
    with PetSession() as session:
        result = (
            session.query(OfficePetModel)
            .filter(OfficePetModel.allowed_in_office==True)
        )
        session.expunge_all()
        print("WHERE clause using filter()")
        print([r for r in result])

    # let's say we wanted to know which pet breeds are allowed in the office (or, where allowed_in_office = True)
    # this shows a different way where we can use keyword arguments
    # this shows how we can use filter_by to get certain columns using SQLAlchemy ORM
    with PetSession() as session:
        result = (
            session.query(OfficePetModel)
            .filter_by(allowed_in_office=True)
        )
        session.expunge_all()
        print("WHERE clause using filter_by()")
        print([r for r in result])

    # let's say we wanted to know pet names for only cats and dogs (or, where pet_species in ["cat", "dog"] )
    # we need to use an "in" function, just like we use an "in" operator in  SQL
    # this shows how we can use filter and in_() to filter by a list of values using SQLAlchemy ORM
    with PetSession() as session:
        result = (
            session.query(PetModel)
            .filter(PetModel.pet_species.in_(["cat", "dog"]))
        )
        session.expunge_all()
        print("WHERE/IN clause using filter()")
        print([r for r in result])

    # let's say we wanted to know pet names for all pets besides cats and dogs (or, where pet_species not in ["cat", "dog"] )
    # we need to use an "not in" function, just like we use an "not in" operator in  SQL
    # this shows how we can use filter, not_() and in_() to filter by a list of values using SQLAlchemy ORM
    with PetSession() as session:
        result = (
            session.query(PetModel)
            .filter(not_(PetModel.pet_species.in_(["cat", "dog"])))
        )
        session.expunge_all()
        print("WHERE/NOT IN clause using filter()")
        print([r for r in result])

    # let's say we wanted to know information about insurance plans that cost more than 5500
    # but are less than or equal to 900 dollars
    # we need to use an "and_" function, just like we use an "and" operator in  SQL
    # this shows how we can use filter, and_() to filter by multiple criteria using SQLAlchemy ORM
    with PetSession() as session:
        result = (
            session.query(InsuranceModel)
            .filter(and_(InsuranceModel.insurance_cost > 5000, InsuranceModel.insurance_cost <= 9000))
        )
        session.expunge_all()
        print("WHERE/AND clause using filter()")
        print([r for r in result])


