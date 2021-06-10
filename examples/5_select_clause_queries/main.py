from db_init import initialize_db
from create_data_for_tables import *
from add_data_to_tables import *
from query_constructor import *


# connect to our database with sqlalchemy
initialize_db("pet")


# get data for tables
employees_list = create_employees()
pets_dicts = create_pets()
office_pets_list = create_office_pets()
insurance_list = create_insurance()


# add data to tables
create_employees_bulk(employees_list)
create_insurance_bulk(insurance_list)
create_office_pets_bulk(office_pets_list)


for key in pets_dicts:
    add_pet_for_employee(key, pets_dicts[key])


# select certain columns using query function
query_select_columns()

# select certain columns using options function
load_select_columns()

# rename columns using label in query function
rename_columns()




