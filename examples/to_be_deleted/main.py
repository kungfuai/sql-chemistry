from sqlalchemy import not_, and_, distinct
from db_init import initialize_db, PetSession
from build_tables import build_stuff
from sqlalchemy.sql import func
from sqlalchemy.orm import load_only, lazyload, raiseload, joinedload
from models.pets_model import *

# start the pets database
initialize_db()

# populate data in tables
build_stuff()

""" This section has example queries in the RECIPES.md file in this repo"""
# Selecting certain columns ("select" clause in SQL)
with PetSession() as session:
    result = (
        session.query(
            OfficePetModel.pet_breed,
            OfficePetModel.allowed_in_office
        ).all())
    session.expunge_all()
    print("SELECT clause")
    print([r for r in result])


with PetSession() as session:
    result = (session.query(OfficePetModel)
              .options(load_only("pet_breed", "allowed_in_office"))
              .all())
    session.expunge_all()
    print("SELECT with load_only")
    print([r for r in result])


# Labeling columns with aliases ("as" in SQL)
with PetSession() as session:
    result = (
        session.query(
            OfficePetModel.pet_breed.label("breed"),
            OfficePetModel.allowed_in_office.label("allowed")
        ).all())
    print("SELECT AS clause")
    print(result[0].keys())


# Limiting results of a query ("limit" clause in SQL)
with PetSession() as session:
    result = (
        session.query(PetModel.pet_name, PetModel.pet_breed).limit(5))
    print("LIMIT clause")
    print([r for r in result])


# Filtering results by a condition ("where" clause in SQL)
with PetSession() as session:
    result = (
        session.query(OfficePetModel)
        .filter(OfficePetModel.allowed_in_office==True))
    print("WHERE clause with filter")
    print([r.pet_breed for r in result])


with PetSession() as session:
    result = (
        session.query(OfficePetModel).filter_by(allowed_in_office=True))
    print("WHERE clause with filter_by")
    print([r.pet_breed for r in result])


# Filtering using a list of items ("in" operator in SQL)
species = ["cat", "dog"]
with PetSession() as session:
    result = (
        session.query(PetModel)
        .filter(PetModel.pet_species.in_(species)))
    print("IN clause")
    print([r.pet_name for r in result])

# Excluding using a list of items ("not in" operator in SQL)
species = ["cat", "dog"]
with PetSession() as session:
    result = (
        session.query(PetModel)
        .filter(not_(PetModel.pet_species.in_(species))))
    print("NOT IN clause")
    print([r.pet_name for r in result])

# Filtering using operators ("<, >, >=, <=" operator in SQL)
with PetSession() as session:
    result = (
        session.query(InsuranceModel)
        .filter(and_(InsuranceModel.insurance_cost>5500, InsuranceModel.insurance_cost<=9000)))
    print("NOT IN clause")
    print([r.pet_species for r in result])


# Joining another table with one foreign key ("join" clause in SQL)
with PetSession() as session:
    result = (
        session.query(EmployeeModel, PetModel)
        .filter(EmployeeModel.id==PetModel.employee_id))
    print("JOIN clause using filter")
    print([[r.EmployeeModel.employee_name, r.PetModel.pet_name] for r in result])

with PetSession() as session:
    result = (
        session.query(EmployeeModel, PetModel)
        .join(PetModel))
    print("JOIN clause")
    print([[r.EmployeeModel.employee_name, r.PetModel.pet_name] for r in result])
    print(result)


# Directionally joining another table with one foreign key "left/right [outer] join" clause in SQL)
with PetSession() as session:
    result = (
        session.query(PetModel)
        .outerjoin(EmployeeModel))
    print("LEFT OUTER JOIN clause")
    print(result)


# Joining another table without defined relationships ("join" clause in SQL)
with PetSession() as session:
    result = (
        session.query(PetModel)
        .join(OfficePetModel, OfficePetModel.pet_breed==PetModel.pet_breed)
        .filter(OfficePetModel.allowed_in_office==True))
    print("JOIN clause with no relationship")
    print([r.pet_name for r in result])


# Getting an instance of a primary key value without SQL
with PetSession() as session:
    result = session.query(OfficePetModel).filter_by(id="df88f7ec-0e6a-4aa9-b4d6-61394e8a9ddb")
    session.flush()
    result = (
        session.query(OfficePetModel)
        .get("df88f7ec-0e6a-4aa9-b4d6-61394e8a9ddb")
    )
    print("SELECT clause for an object in identity map")
    print(result)


# Aggregate functions ("count", "sum" in SQL)
with PetSession() as session:
    result = (
        session.query(func.count(PetModel.pet_name)))
    print("COUNT function")
    print(result[0])

with PetSession() as session:
    result = (
        session.query(PetModel.pet_name).count())
    print("COUNT function")
    print(result)


# Finding the count of unique values ("count distinct" in SQL)
with PetSession() as session:
    result = (
        session.query(func.count(PetModel.pet_species)).distinct())
    print("COUNT DISTINCT function - 1")
    print(result[0])

    result = (
        session.query(distinct(PetModel.pet_species)).count())
    print("COUNT DISTINCT function - 2")
    print(result)


# Grouping values to get aggregate calculations at a specific level ("group by" in SQL)
with PetSession() as session:
    result = (
        session.query(PetModel.employee_id, func.count(PetModel.pet_name))
        .group_by(PetModel.employee_id)
    )
    print("GROUP BY clause")
    print([r for r in result])


with PetSession() as session:
    result = (
        session.query(EmployeeModel.employee_name, func.count(PetModel.pet_name))
        .join(EmployeeModel)
        .group_by(EmployeeModel.employee_name)
    )
    print("GROUP BY and JOIN clauses")
    print([r for r in result])


# Filtering results by aggregate calculations ("having" in SQL)
with PetSession() as session:
    result = (
        session.query(EmployeeModel.employee_name, func.count(PetModel.pet_name))
        .join(EmployeeModel)
        .group_by(EmployeeModel.employee_name)
        .having(func.count(PetModel.pet_name) > 1)
    )
    print("HAVING clause")
    print([r for r in result])


# Subquerying using the query function
with PetSession() as session:
    t1 = (
        session.query(EmployeeModel.id, func.count(PetModel.pet_name).label("pet_count"))
        .join(PetModel)
        .group_by(EmployeeModel.id)
        .having(func.count(PetModel.pet_name) > 1)
    ).subquery()

    result = (
        session.query(PetModel.pet_name, t1)
        .join(t1, PetModel.employee_id==t1.c.id)
    )
    print("SUBQUERY functionality")
    print(result[0].keys())
    print([r for r in result])


# Lazy Loading
with PetSession() as session:
    result = (
        session.query(EmployeeModel)
        .options(
            lazyload(EmployeeModel.pets)
        )
    )
    print("LAZY LOADING functionality")
    print(result)
    print([r.id for r in result])


# Raise Loading
with PetSession() as session:
    result = (
        session.query(EmployeeModel)
        .options(
            raiseload(EmployeeModel.pets)
        ),
        session.query(EmployeeModel).join(PetModel)
    )
    print("LAZY LOADING functionality")
    print(result[0])


# Joined Loading
with PetSession() as session:
    result = (
        session.query(EmployeeModel)
        .options(
            joinedload(EmployeeModel.pets)
        ),
        session.query(EmployeeModel).join(PetModel)
    )
    print("EAGER LOADING functionality")
    print(result[0])
    print([[r[i].id, r[i].employee_name] for r in result for i in range(len(result))]) # correct this







