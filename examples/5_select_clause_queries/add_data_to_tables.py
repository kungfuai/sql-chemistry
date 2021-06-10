from typing import List
from models.kfai_pets_model import EmployeeModel, PetModel, OfficePetModel, InsuranceModel
from db_init import PetSession


def create_employees_bulk(employees: List[EmployeeModel]):
    with PetSession() as session:
        session.add_all(employees)
        session.commit()


def add_pet_for_employee(pet: PetModel, employee: EmployeeModel):
    with PetSession() as session:
        session.add(employee)
        employee.pets.append(pet)
        session.add(employee)
        session.commit()


def create_office_pets_bulk(office_pets: List[OfficePetModel]):
    with PetSession() as session:
        session.add_all(office_pets)
        session.commit()


def create_insurance_bulk(insurances: List[InsuranceModel]):
    with PetSession() as session:
        session.add_all(insurances)
        session.commit()
