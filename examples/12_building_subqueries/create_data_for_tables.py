from models.kfai_pets_model import EmployeeModel, PetModel, OfficePetModel, InsuranceModel


def create_employees():
    employee_0 = EmployeeModel(employee_name="Endurance")
    employee_1 = EmployeeModel(employee_name="Tony")
    employee_2 = EmployeeModel(employee_name="Krishi")
    employee_3 = EmployeeModel(employee_name="Max M.")
    employee_4 = EmployeeModel(employee_name="Reed C.")

    employees = [employee_0, employee_1, employee_2, employee_3, employee_4]

    return employees


def add_pet_to_employee():
    pet_0 = PetModel(pet_name="Intel", pet_species="cat", pet_breed="persian")
    pet_1 = PetModel(pet_name="Misa", pet_species="cat", pet_breed="siamese")
    pet_2 = PetModel(pet_name="Java", pet_species="cat", pet_breed="shorthair")
    pet_3 = PetModel(pet_name="Shadow", pet_species="dog", pet_breed="dachshund")
    pet_4 = PetModel(pet_name="Callie", pet_species="cat", pet_breed="persian")
    pet_5 = PetModel(pet_name="Yoshi", pet_species="bird", pet_breed="parrot")
    pet_6 = PetModel(pet_name="Deohgie", pet_species="dog", pet_breed="husky")

    pets = [pet_0, pet_1, pet_2, pet_3, pet_4, pet_5, pet_6]

    employees = create_employees()

    employees[0].pets.append(pets[0])
    employees[0].pets.append(pets[1])
    employees[0].pets.append(pets[2])
    employees[1].pets.append(pets[3])
    employees[3].pets.append(pets[4])
    employees[3].pets.append(pets[5])
    employees[3].pets.append(pets[6])

    return employees


def create_office_pets():
    office_pet_0 = OfficePetModel(pet_breed="persian", allowed_in_office=True)
    office_pet_1 = OfficePetModel(pet_breed="siamese", allowed_in_office=True)
    office_pet_2 = OfficePetModel(pet_breed="dachshund", allowed_in_office=True)
    office_pet_3 = OfficePetModel(pet_breed="parrot", allowed_in_office=False)
    office_pet_4 = OfficePetModel(pet_breed="husky", allowed_in_office=False)

    office_pets = [office_pet_0, office_pet_1, office_pet_2, office_pet_3, office_pet_4]

    return office_pets


def create_insurance():
    insurance_plan_0 = InsuranceModel(pet_species="cat", insurance_cost=5432)
    insurance_plan_1 = InsuranceModel(pet_species="dog", insurance_cost=9000)
    insurance_plan_2 = InsuranceModel(pet_species="parrot", insurance_cost=8080)

    insurance = [insurance_plan_0, insurance_plan_1, insurance_plan_2]

    return insurance



