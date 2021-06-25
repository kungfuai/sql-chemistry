from create_data_for_tables import add_pet_to_employee, create_office_pets, create_insurance
from add_data_to_tables import create_employees_bulk, create_insurance_bulk, create_office_pets_bulk


def _get_employee_data():
    # get data for tables
    employees_list = add_pet_to_employee()
    return employees_list


def _get_office_pets_data():
    office_pets_list = create_office_pets()
    return office_pets_list


def _get_insurance_data():
    insurance_list = create_insurance()
    return insurance_list


def add_data_to_tables():
    employees = _get_employee_data()
    office_pets = _get_office_pets_data()
    insurance = _get_insurance_data()

    # add data to tables
    create_employees_bulk(employees)
    print('Employees added to pet database.')

    create_office_pets_bulk(office_pets)
    print('Office pets added to pet database.')

    create_insurance_bulk(insurance)
    print('Insurance added to pet database.')
