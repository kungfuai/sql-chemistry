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

    """ Example code for using the GROUP BY clause with SQLAlchemy ORM"""
    # let's say we wanted to get the count of total pets each employee has
    # this means that we first have to group the pet table by employee_id
    # and then we get the count of rows for each employee_id
    # this shows how we can use group by to get that answer using SQLAlchemy ORM
    with PetSession() as session:
        result = (
            session.query(PetModel.employee_id, func.count(PetModel.pet_name))
            .group_by(PetModel.employee_id)
        )
        session.expunge_all()
        print("GROUP BY clause")
        print([r for r in result])

    # let's say we want the employee name by the count of pets rather than employee_id
    # this means that we have to join the employee table to get the employee_name column
    with PetSession() as session:
        result = (
            session.query(EmployeeModel.employee_name, func.count(PetModel.pet_name))
            .join(EmployeeModel)
            .group_by(EmployeeModel.employee_name)
        )
        session.expunge_all()
        print("GROUP BY/JOIN clauses")
        print([r for r in result])