from sqlalchemy import distinct

from db_init import initialize_db, PetSession
from add_tables_to_db import add_data_to_tables
from models.kfai_pets_model import PetModel, EmployeeModel
from sqlalchemy.sql import func

# connect to our database with sqlalchemy
initialize_db("pet")

# create sample data and add to our tables
add_data_to_tables()


if __name__ == "__main__":

    """ Example code for using the HAVING clause with SQLAlchemy ORM"""
    # let's say we wanted to see pet names for employees that have more than 1 pet
    # this means that we first have to group the pet table by employee_id
    # and then we get the count of rows for each employee_id
    # after that, we filter by that value to ensure that the value is above 1
    # this shows how we can use having to get that answer using SQLAlchemy ORM
    with PetSession() as session:
        result = (
            session.query(EmployeeModel.employee_name, func.count(PetModel.pet_name))
            .join(EmployeeModel)
            .group_by(EmployeeModel.employee_name)
            .having(func.count(PetModel.pet_name) > 1)
        )
        session.expunge_all()
        print("HAVING clause")
        print([r for r in result])