from table_pop import create_employees_bulk, add_pet_for_employee, create_office_pets_bulk, create_insurance_bulk
from models.pets_model import EmployeeModel, PetModel, OfficePetModel, InsuranceModel


def build_stuff():
    employee_1 = EmployeeModel(employee_name="Endurance")
    employee_2 = EmployeeModel(employee_name="Tony")
    employee_3 = EmployeeModel(employee_name="Krishi")
    employee_4 = EmployeeModel(employee_name="Max M.")
    employee_5 = EmployeeModel(employee_name="Reed C.")

    employees = [employee_1, employee_2, employee_3, employee_4, employee_5]

    create_employees_bulk(employees)

    pets = {PetModel(pet_name="Intel", pet_species="cat", pet_breed="persian"): employee_1,
            PetModel(pet_name="Misa", pet_species="cat", pet_breed="siamese"): employee_1,
            PetModel(pet_name="Java", pet_species="cat", pet_breed="shorthair"): employee_1,
            PetModel(pet_name="Shadow", pet_species="dog", pet_breed="dachshund"): employee_2,
            PetModel(pet_name="Callie", pet_species="cat", pet_breed="persian"): employee_4,
            PetModel(pet_name="Yoshi", pet_species="bird", pet_breed="parrot"): employee_4,
            PetModel(pet_name="Deohgie", pet_species="dog", pet_breed="husky"): employee_4}

    for key in pets:
        add_pet_for_employee(key, pets[key])

    office_pet_1 = OfficePetModel(pet_breed="persian", allowed_in_office=True)
    office_pet_2 = OfficePetModel(pet_breed="siamese", allowed_in_office=True)
    office_pet_3 = OfficePetModel(pet_breed="dachshund", allowed_in_office=True)
    office_pet_4 = OfficePetModel(pet_breed="parrot", allowed_in_office=False)
    office_pet_5 = OfficePetModel(pet_breed="husky", allowed_in_office=False)

    office_pets = [office_pet_1, office_pet_2, office_pet_3, office_pet_4, office_pet_5]

    create_office_pets_bulk(office_pets)

    insurance_plan_1 = InsuranceModel(pet_species="cat", insurance_cost=5432)
    insurance_plan_2 = InsuranceModel(pet_species="dog", insurance_cost=9000)
    insurance_plan_3 = InsuranceModel(pet_species="parrot", insurance_cost=8080)

    insurances = [insurance_plan_1, insurance_plan_2, insurance_plan_3]

    create_insurance_bulk(insurances)
