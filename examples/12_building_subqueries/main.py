from db_init import initialize_db, PetSession
from add_tables_to_db import add_data_to_tables
from models.kfai_pets_model import PetModel, EmployeeModel
from sqlalchemy.sql import func

# connect to our database with sqlalchemy
initialize_db("pet")

# create sample data and add to our tables
add_data_to_tables()


if __name__ == "__main__":

    """ Example code for subqueries with SQLAlchemy ORM"""
    # let's say we wanted to figure out the names of pets for employees with more than one pet
    # this means that we first have to group the pet table by employee_id
    # and then we get the count of rows for each employee_id
    # this will be our first query, which we structured in example 11_having_clause_queries
    # with the temporary table from this subquery, we can join on the pet table to get pet_name
    with PetSession() as session:
        t1 = (
            session.query(EmployeeModel.id, func.count(PetModel.pet_name).label("pet_count"))
            .join(EmployeeModel)
            .group_by(EmployeeModel.id)
            .having(func.count(PetModel.pet_name) > 1)
        ).subquery()

        result = (
            session.query(PetModel.pet_name, t1)
            .join(t1, PetModel.employee_id == t1.c.id)
        )
        session.expunge_all()
        print("SUBQUERY")
        print([r for r in result])