from models.pets_model import EmployeeModel, PetModel, OfficePetModel, InsuranceModel
from db_init import PetSession


def employee_tables(employee_list, pet_dicts):
    with PetSession() as session:
        for name in employee_list:
            e = EmployeeModel(employee_name=name)
            session.add(e)
            session.flush()

            for pet in pet_dicts:
                if pet_dicts[pet][0] == name:
                    p = PetModel(pet_name=pet,
                                 pet_species=pet_dicts[pet][1],
                                 pet_breed=pet_dicts[pet][2],
                                 employee_id=e.id)

                    session.add(p)

        session.commit()


def office_pet_table(office_pet_dicts):
    with PetSession() as session:
        for pet in office_pet_dicts:
            o = OfficePetModel(pet_breed=pet, allowed_in_office=office_pet_dicts[pet])
            session.add(o)

        session.commit()


def insurance_table(insurance_dicts):
    with PetSession() as session:
        for species in insurance_dicts:
            i = InsuranceModel(pet_species=species, insurance_cost=insurance_dicts[species])
            session.add(i)

        session.commit()
