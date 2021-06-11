from db_init import initialize_db, PetSession
from add_tables_to_db import add_data_to_tables
from models.kfai_pets_model import PetModel, EmployeeModel, OfficePetModel

# connect to our database with sqlalchemy
initialize_db("pet")

# create sample data and add to our tables
add_data_to_tables()


if __name__ == "__main__":

    """ Example code for using the JOIN clause with SQLAlchemy ORM"""
    # let's say we wanted to know the employee names and pet names for each employee
    # since they are in two different tables, we need to filter both tables using attributes that work as join keys
    # this shows how we can use filter to do a simple join to get that data using SQLAlchemy ORM
    with PetSession() as session:
        result = (
            session.query(EmployeeModel, PetModel)
            .filter(EmployeeModel.id == PetModel.employee_id)
        )
        session.expunge_all()
        print("JOIN clause using filter()")
        print([r for r in result])

    # since we have defined a relationship for these two models, there is an easier way to do this
    # note: a relationship between a primary key and foreign key must be defined for this to work
    with PetSession() as session:
        result = (
            session.query(EmployeeModel)
            .join(PetModel)
        )
        session.expunge_all()
        print("JOIN clause using a relationship")
        print([r for r in result])

    # let's say we want to find pet names of pets allowed in the office
    # this means we want to join on tables that do not have a relationship defined
    # in this case, we need to use the attributes that could work as join keys
    with PetSession() as session:
        result = (
            session.query(PetModel)
            .join(OfficePetModel, PetModel.pet_breed==OfficePetModel.pet_breed)
            .filter(OfficePetModel.allowed_in_office==True)
        )
        session.expunge_all()
        print("JOIN clause without a relationship")
        print([r for r in result])


