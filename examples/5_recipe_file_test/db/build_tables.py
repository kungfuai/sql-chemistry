from table_pop import employee_tables, office_pet_table, insurance_table


def populate_data():
    employees = ["Endurance", "Tony", "Krishi", "Max M.", "Reed C."]

    pets = {'Intel': ('Endurance', 'cat', 'persian'),
            'Misa': ('Endurance', 'cat', 'siamese'),
            'Java': ('Endurance', 'cat', 'shorthair'),
            'Shadow': ('Tony', 'dog', 'dachshund'),
            'Callie': ('Max M.', 'cat', 'persian'),
            'Yoshi': ('Max M.', 'bird', 'parrot'),
            'Deohgie': ('Max M.', 'dog', 'husky')}

    office_pets = {'persian': True,
                   'siamese': True,
                   'dachshund': True,
                   'parrot': False,
                   'husky': False}

    insurance_cost = {'cat': 5432,
                      'dog': 9000,
                      'parrot': 8080}

    employee_tables(employees, pets)
    office_pet_table(office_pets)
    insurance_table(insurance_cost)

