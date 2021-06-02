# Recipe Guidebook
This provides examples for how to use SQLAlchemy. We will do this by setting up a problem, with sample tables (models) and relationships (join keys). Then, we will jump into how to query our tables with SQLAlchemy, giving examples of how to use the library and the SQL equivalent along the way.

Before that, let's give a quick introduction on SQLAlchemy.


## SQLAlchemy: Introduction + Table Setup
### About the Library
SQLAlchemy is a library that allows us to work with databases using Python. There are two main user-facing portions to SQLAlchemy: Core and ORM. At KF, we will focus on using SQLAlchemy ORM.


### Explaining ORM
ORM, or Object Relational Mapper, allows us to write SQL Queries using object oriented concepts. This is helpful because it allows us to query a database using any language, it allows us to use any database system the same way (no need to memorize the nuances between MySQL syntax versus Postgres), and it provides a lot of added functionality. SQL query strings are also vulnerable to attack, and ORMs can prevent some SQL injection attempts.

### Definitions
#### Primary and Foreign Keys
A primary key is a column in a table whose values uniquely identify a row in the table, and a foreign key is a column that corresponds tot he values of the primary key in another table. Together, the primary and foreign keys define relationships across tables. This will be useful for knowing how to join tables later on.


## Problem Setup
Let's say we have a database that we use for pets of KF employees. We use this database to find pet birthdays, whose pets can come into the office, and the most popular breeds among KF employees.

It has the employee's basic information, whether they have pets, information about any pets, if they have pet insurance through KF (made up, we do not over this, not even sure if this exists) and pets that KF allows into the office.

We have 5 tables: employees, pets, pet_info, insurance, office_pets

### Defining Our SQL Tables
Let's define our tables. Some tables will have primary keys and foreign keys. 

Here are our tables, primary and foreign keys:

Database: kungfu_pets

Table: employees
Primary key: employee_id

employee_id | employee_name  
-----------------------------
1			|	Endurance
-----------------------------
2			|	Tony
-----------------------------
3			|	Krishi	
-----------------------------
4			|	Max M.	
-----------------------------
5 			|	Reed C.
-----------------------------

Table: pets
Primary key: pet_name
Foreign key: employee_id

pet_name    | employee_id   
-----------------------------
Intel		|	1
-----------------------------
Misa		|	1
-----------------------------
Java	   	|	1	
-----------------------------
Shadow		|	2
-----------------------------
Callie  	|	4
-----------------------------
Yoshi		|	4
-----------------------------
Deohgie		|	4
-----------------------------

Table: pet_info
Primary key: pet_name

pet_name    | pet_species   | pet_breed
------------------------------------------
Intel		|	cat         | persian
------------------------------------------
Misa		|	cat         | siamese
------------------------------------------
Java	   	|	cat         | shorthair
------------------------------------------
Shadow		|	dog         | dachshund
------------------------------------------
Callie  	|	cat         | persian
------------------------------------------
Yoshi		|	bird        | parrot
------------------------------------------
Deohgie		|	dog         | husky
------------------------------------------

Table: insurance
Primary key: pet_name

employee_id | pet_name      | insured?
------------------------------------------
1			|	Intel       | True
------------------------------------------
1			|	Misa        | False
------------------------------------------
1			|	Java	    | True
------------------------------------------
2			|	Shadow	    | True
------------------------------------------
4 	        |	Callie      | True 
------------------------------------------
4	    	|	Yoshi       | False
------------------------------------------
4	     	|	Deohgie		| False
------------------------------------------

Table: office_pets
Primary key: pet_breed

pet_breed   | allowed_in_office   
--------------------------------
persian		|	1
--------------------------------
siamese		|	1
--------------------------------
shorthair 	|	1	
--------------------------------
dachschund	|	1
--------------------------------
persian 	|	1
--------------------------------
parrot		|	0
--------------------------------
husky		|	0
--------------------------------


### Creating Models and Relationships From the Tables
To get started with SQLAlchemy ORM, we have to have a way to somehow represent the information of the tables in an object-oriented way that SQLAlchemy ORM can understand (essentially, we must map to the table to an object). To do this, we build a "model" which represents our table. We also define "relationships" to define how different tables can join based on the primary and foreign keys defined.

The model inherits from a base model that the SQLAlchemy ORM library has created with us that has all the basics that any table will need to be transformed into an object. To get started, we import the base model, declarative_base, and then use that to create classes that represents the objects we are mapping the table from.

```python
from sqlalchemy import Column, Integer, String, relationship
from sqlalchemy.orm import declarative_base

BaseDbModel = declarative_base()


class EmployeesModel(BaseDbModel):
    __tablename__ = "employees"

    employee_id = Column("EmployeeId", String(100), primary_key=True, autoincrement=True)		
    employee_name = Column("EmployeeName", String(100))

    pets = relationship("PetsModel", back_populates="employees")


class PetsModel(BaseDbModel):
    __tablename__ = "pets"

    pet_name = Column("PetName", String(100), primary_key=True)
    employee_id = Column("EmplyeeId", String(100), ForeignKey(employees.employee_id))

    employees = relationship("EmployeesModel", back_populates="pets")
    pet_info = relationship("PetInfoModel", back_populates="pets_petinfo")


class PetInfoModel(BaseDbModel):
    __tablename__ = "pet_info"

    pet_name = Column("Id", String(100), primary_key=True)
    pet_species = Column("PetSpecies", String(100))
    pet_breed = Column("PetBreed", String(100))

    pet_petinfo = relationship("PetsModel", back_populates="pet_info")


class InsuranceModel(BaseDbModel):
    __tablename__ = "insurance"

    employee_id = Column("EmployeeId", String(100))
    pet_name = Column("FirstName", String(100))
    insured = Column("Insured", Boolean)


class OfficePetsModel(BaseDbModel):
    __tablename__ = "office_pets"

    pet_breed = Column("PetBreed", Integer, primary_key=True, autoincrement=True)
    allowed_in_office = Column("AllowedInOffice", Boolean, create_constraint=True, name='valid_bool')
    valid_bool = CheckConstraint('allowed_in_office in (1, 0)', name='valid_bool')
```


## SQLAlchemy: Recipes Using Tables
We are going to show some common queries using made-up problems that utilize our tables for the kungfu_pets database. If something is missing from the recipe section, please let us know.


### Selecting certain columns ("select" clause in SQL)
Let's say we only want to know the names of the pet name and pet breed at KF. This the SQL:
```sql
select pet_name, pet_breed
from PetInfoModel
```

Using SQLAlchemy ORM syntax, we would have two ways to load a certain set of columns:

1. Directly in the query clause
```python
with AppSession("kungfu_pets") as session:
    session.query(PetInfoModel.pet_name, PetInfoModel.pet_breed).all()
```

2. Using the options argument
```python
with AppSession("kungfu_pets") as session:
    session.query(PetInfoModel)
    .options(
        load_only(
            "pet_name",
            "pet_breed"
        )
    )
    .all()
```

### Labeling columns with aliases ("as" in SQL)
Let's say that we want to rename the columsn that we just selected to be specific to KF:
The SQL example we are trying to do:
```sql
select pet_name as kf_pet_name, pet_breed as kf_pet_breed
from PetInfoModel
```

This can be done in SQL Alchemy ORM like this:
```python
with AppSession("kungfu_pets") as session:
    session.query(
        PetInfoModel.column1.label("kf_pet_name"),
        PetInfoModel.column2.label("kf_pet_breed")
        )
    .all()
```

To see another example, look at the "using Aliases" section of the docs here:
https://docs.sqlalchemy.org/en/14/orm/tutorial.html#querying


### Limiting results of a query ("limit" clause in SQL)
Let's say we only want information about five pets at KF (short attention span, we don't want to see all that data at once!):
The SQL example we are trying to do:
```sql
select pet_name, pet_breed
from PetInfoModel
limit 5
```

This can be done in SQL Alchemy ORM like this:
```python
with AppSession("kungfu_pets") as session:
    session.query(
        PetInfoModel.pet_name,
        PetInfoModel.pet_breed
        )
    .limit(5)
```

### Filtering results by a condition ("where" clause in SQL)
Now that we've looked at pet names and pet breeds, we want to know which ones are actually allowed in the office. This means we have to filter our OfficePetsModel table:
The SQL example we are trying to do:
```sql
select *
from OfficePetsModel
where allowed_in_office = 1
```

There are two ways to do this in SQLAlchemy ORM.

1. Use filter and specify the model, with column name as an attribute (Pythonic, hence 2 equals signs)
```python
with AppSession("kungfu_pets") as session:
    session.query(OfficePetsModel)
    .filter(OfficePetsModel.allowed_in_office==1)
    .all()
```

2. Use filter_by and specify just the attribute (SQLish, hence 1 equals sign)
```python
with AppSession("kungfu_pets") as session:
    session.query(OfficePetsModel)
    .filter_by(allowed_in_office=1)
    .all()
```

Both do the same things, but the syntax is slightly different. To do functions, using filter is easier because you can do it without function calls.

To apply another operator, instead of "==" or "=", you can type in ">" for greater than, ">=" for greater than or equals to, "<" for less than, ">=" for less than or equals to and "!=" for does not equals.


### Filtering using a list of items ("in" operator in SQL)
We want to know pet names for members of the Software Engineering team, which we know are related to employee_ids 1, 2 and 3.

The SQL example we are trying to do:
```sql
select *
from PetsModel
where employee_id in (1, 2, 3)
```

To do this, we can define a list or a tuple with the values we want, as below:

```python
list_of_values = [1, 2, 3]

with AppSession("kungfu_pets") as session:
    session.query(PetsModel)
    .filter(PetsModel.employee_id._in(list_of_values))
    .all()
```

This is useful when you have a pre-defined list of values that you want to search for in a column.
Look at this stackoverflow to see more: https://stackoverflow.com/questions/8603088/sqlalchemy-in-clause


#### Excluding using a list of items ("not in" operator in SQL)
Let's say we want to take a quick look at pet names of members who are not part of the Software Engineering team. Instead of looking up the employee_ids, we can just use the opposite operator, not in.

The SQL example we are trying to do:
```sql
select *
from PetsModel
where employee_id not in (1, 2, 3)
```

To do this, we can define a list or a tuple with the values we want, as below:

```python
list_of_values = [1, 2, 3]

with AppSession("kungfu_pets") as session:
    session.query(PetsModel)
    .filter(not_(PetsModel.employee_id._in(list_of_values)))
    .all()
```

This is useful when you have a pre-defined list of values that you want to exclude from a search.


### Filtering using operators ("<, >, >=, <=" operator in SQL)
Since the employee_ids are simply integers, we realize that we can actually just use an operator to filter. Let's say we wanted to look again at Software Engineering employees that have pets (which we know have employee_ids of 1 to 3). 

To do this, we can use something similar to what we used to find which pets were allowed in the office:

The SQL example we are trying to do:
```sql
select *
from PetsModel
where employee_id > 0 and employee_id <= 3
```

To do this, we use the _and operator along with filter, as below:
```python
with AppSession("kungfu_pets") as session:
    session.query(PetsModel)
    .filter(and_(PetsModel.employee_id>0, PetsModel.employee_id<=3))
    .all()
```

If we wanted to filter by multiple columns, we can skip the and_. Instead, we simply list the different columns we want to filter by in a comma. If we wanted to filter using or, we use the or_ operator in the same way as we did with the and_ in the example above.


#### Joining another table with one foreign key ("join" clause in SQL)
Having a list of pet names by employee_ids is great, but having a list of pet names by the employee names would be even better. Let's make that happen with a simple join.

The SQL example we are trying to do:
```sql
select *
from EmployeesModel e
join PetsModel p
  on p.employee_id = e.employee_id
```

There are two ways to do this. The first is to use the filter function in SQL Alchemy ORM to combine two tables based on the equivalency of values for a column.

To do this, we write:
```python
with AppSession("kungfu_pets") as session:
    session.query(EmployeesModel, PetsModel)
    .filter(EmployeesModel.employee_id==PetsModel.employee_id)
    .all()
```

That's great, but we there's an easier way to do this. Since EmployeesModel has a primary key, and PetsModel has a foreign key that has a defined relationship with the primary key in EmployeesModel, we can just use the join attribute without even specifying the columns - SQLAlchemy ORM knows to use the predefined relationship.

To do this, we write:
```python
with AppSession("kungfu_pets") as session:
    session.query(EmployeesModel)
    .join(PetsModel)
    .all()
```

If there is not one foreign key, look below to see how to use the join syntax appropriately.

<mark>Note: by default, "join" refers to inner joins. To do an outer join, replace "join" with "outerjoin" in the example above.</mark>

For left and right joins, look below.


### Directionally joining another table with one foreign key "left/right [outer] join" clause in SQL)
With joins, we can join in a specific direction (left or right). With a left join, which in PostgreSQL and MySQL are equivalent to left outer joins, we include everything that is in the table listed in the from clause, and whatever is found based on the join key in the left join clause.  For a right join, which is a right outer join in PostgreSQL and MySQL, the opposite happens. Everything in the right join clause is included, and whatever is found based on the join key in the table in the from caluse is included. A visual to help can be found here: https://www.codeproject.com/Articles/33052/Visual-Representation-of-SQL-Joins

And a textual explanation can be found here: https://stackoverflow.com/questions/15425740/are-left-outer-joins-and-left-joins-the-same

In essence, a left join and right join are just opposites, and flipping the order that the tables are joined in the query results in the opposing join type. SQL syntax makes a distinction, but SQLAlchemy ORM does not - instead, the order the tables are referred to are what determines what direction the join happens in and what data is included.

Let's put this to use. Let's say that we only really want to know the employee names and pet names of employees who have pets. Because left and right joins are opposites, we can do it using both.

To do the left join, we know that we want to use the PetsModel and join only employees from EmployeesModel that have employee_ids in PetsModel.

The SQL example for a left join is:
```sql
select *
from PetsModel p
left join EmployeesModel e
  on p.employee_id = e.employee_id
```

The SQL example for a right join is:
```sql
select *
from EmployeesModel e
right join PetsModel p
  on p.employee_id = e.employee_id
```

In SQLAlchemy ORM, we use outerjoin to specify which table we want to join against. There isn't a left or right join specified because SQLAlchemy ORM knows that the left and right joins are opposites, so there is only one way to do the joins we did above.

For the join to get pet names only employees with pets, the syntax is:
```python
with AppSession("kungfu_pets") as session:
    session.query(PetsModel)
    .outerjoin(EmployeesModel)
    .all()
```

SQLAlchemy ORM takes away the distinction and thus lets the order of tables guide the data included. The query function holds the table that you want to include all the data for, and the outerjoin holds the table that you want to display only the data found in the query clause's table.


### Joining another table without defined relationships ("join" clause in SQL)
Let's say that we want to find the pet names of pets allowed in the office. Since we don't have a relationship defined in our models (there is no primary/foreign key relationship defined), we have to be more explicit when building our join clause.

The SQL example we are trying to do:
```sql
select *
from PetInfoModel i
join OfficePetsModel o
  on i.pet_breed = o.pet_breed
where o.allowed_in_office = 1
```

To do this, the syntax is:
```python
with AppSession("kungfu_pets") as session:
    session.query(PetsModel)
    .join(OfficePetsModel, PetInfoModel.pet_breed==OfficePetsModel.pet_breed)
    .filter(OfficePetsModel.allowed_in_office==1)
    .all()
```

## SQLAlchemy: Advanced Recipes Using Tables
### Getting an instance of a primary key value without SQL
Let's say that we want to find the employee_name associated with employee_id = 5. 

In this scenario, let's say that we just started a session and have queried this exact same thing within the session. 

SQLAlchemy ORM provides an identity map, which keeps a record of all objects that have been read from the database in a session. Whenever you want an object, you check the identity map first to see if you already have it.

The advantage of doing it this way is that we can get the object without every having to query the database. This makes object retrieval more efficient.

For our case, the SQL we are trying to do is:
```sql
select *
from EmployeesModel
where employee_id = 5
```

This basically means that we want to retrieve the object from the EmployeesModel that has an employee_id of 5. Because we are filtering based on a primary key of the EmployeesModel table, we can use the identity map to first check if we already have the object related to employee_id = 5 rather than querying our kungfu_pets database.

To do this with SQLAlchemy ORM, all we do is:
```python
with AppSession("kungfu_pets") as session:
    session.query(EmployeesModel)
    .get(5)
```

This will get the value of the primary key for the table in the query clause and return this, if it is in our identity map:

class EmployeesModel:
	employee_id: 5
	employee_name: 'Reed C.'


If we have multiple primary keys, we can pass a dictionary listing the primary keys and values that we are searching for in our identity map:

```python
with AppSession("kungfu_pets") as session:
	session.query(EmployeesModel)
	.get({employee_id: 5, "new_column": 'ML Engineer'})
```

where new_column is another primary key that we are defining for illustrative purposes.

To learn more about get, read here: https://docs.sqlalchemy.org/en/14/orm/query.html


### Aggregate functions ("count", "sum" in SQL)
Let's say that we want to get the count of pet names in KF. To do this, we need to import "func" from sqlalchemy.sql and use one of the aggregate functions. For this, we use count.

Note: There is also max, min, sum and many other aggregate functions. To see this full list, visit this link: https://docs.sqlalchemy.org/en/14/core/functions.html

The SQL example we are trying to do:
```sql
select count(pet_name)
from PetInfoModel
```

To do this, the syntax is:
```python
from sqlalchemy.sql import func

with AppSession("kungfu_pets") as session:
    session.query(func.count(PetInfoModel.pet_name))
```

If we wanted to specify a name, which is usually a good idea since the default name for an aggregate function is just the name of the aggregate function (in this case, count), we do:
```python
from sqlalchemy.sql import func

with AppSession("kungfu_pets") as session:
    session.query(func.count(PetInfoModel.pet_name).label("pet_name_count"))
```

### Finding the count of unique values ("count distinct" in SQL)
Let's say that we want to get the count of distinct pet species in KF. This means that we are combining an aggregate function with the distinct selector so that don't just get a count of all rows that have a pet_species value, but we get only the count of unique pet_species values.


The SQL example we are trying to do:
```sql
select count(distinct pet_species) as unique_pet_species_count
from PetInfoModel
```

To do this, we simply add .distinct() at the end of our query attribute. The aggregate function and alias are defined in the query selector itself, while the .distinct() is added as an attribute of query.


This is how we do it:
```python
from sqlalchemy.sql import func

with AppSession("kungfu_pets") as session:
    session.query(func.count(PetInfoModel.pet_species).label("pet_name_count"))
    .distinct()
```

### Grouping values to get aggregate calculations at a specific level ("group by" in SQL)
Let's say we want to get a count of total pets that each employee has. This means that we can't just do an overall count - we want to first group the table by the employee_id column in PetsModel and then get a count of the number of rows for each employee_id (assuming that there are no duplicate pet_names in our PetsModel).

This sounds complicated, but it's not too bad.  

The SQL example we are trying to do:
```sql
select employee_id, count(*) as pet_count
from PetsModel
group by employee_id
```

This is how we do it using SQLAlchemy ORM:
```python
with AppSession("kungfu_pets") as session:
    session.query(PetsModel.employee_id,func.count(PetsModel.pet_name).label("pet_count"))
    .group_by(PetsModel.employee_id)
    .all()
```

In SQLAlchemy, for a count(*), it is standard to use the primary key as the column since that can make querying the database more efficient, and there should be a unique value for each row in the primary key column.

Let's say we aren't satisfied with getting the employee_id and pet_count - we want the employee_name alongside the pet_count. This would make the output more understandable. To do this, we want to perform that same group by, but also join on the EmployeesModel table to get the name of the employees by joining based on the primay key, foreign key relationship we defined above.

The SQL example we are trying to do:
```sql
select employee_name, count(*) as pet_count
from PetsModel p 
left join EmployeesModel e
  on e.employee_id = p.employee_id
group by employee_name
```

To do this, we write the SQLAlchemy ORM statement like this:
```python
with AppSession("kungfu_pets") as session:
    session.query(EmployeesModel.employee_name, func.count(PetsModel.pet_name).label("pet_count"))
    .join(EmployeesModel)
    .group_by(EmployeesModel.employee_name)
    .all()
```

### Filtering results by aggregate calculations ("having" in SQL)
Let's say that we only want to see the pet names for employees that have more than 1 pet. To do this, we would first need to perform an aggregate calculation to count the number of pets that an employee has, and then filter by that value to ensure that the value is above 1.

We cannot use the where clause in SQL, or the filter clause in SQLAlchemy ORM, because that does the filtering before the group by occurs. It also does not handle aggregate calculations. Therefore, we use the having clause in SQL and SQLAlchemy ORM to achieve the result we want.

The SQL example we are trying to do:
```sql
select employee_name, count(*) as pet_count
from PetsModel p 
left join EmployeesModel e
  on e.employee_id = p.employee_id
group by employee_name
having count(*) > 1
```

To do this, we write the SQLAlchemy ORM statement like this:
```python
with AppSession("kungfu_pets") as session:
    session.query(EmployeesModel.employee_name, func.count(PetsModel.pet_name).label("pet_count"))
    .join(EmployeesModel)
    .group_by(EmployeesModel.employee_name)
    .having(func.count(PetsModel.pet_name) > 1)
    .all()
```

### Subquerying using the query function
Let's say we want that we want to see which pets have pet insurance for all employees that have at least one pet. This means that we need to first figure out which employees have at least one pet, and then use that information to figure out which pets have insurance.

The first part of the SQL example we are trying to do is similar to the one above:
```sql
select employee_id, count(*) as pet_count
from PetsModel p 
left join EmployeesModel e
  on e.employee_id = p.employee_id
group by employee_id
having count(*) > 1
```

The second part of the SQL example we are trying to do is:
```sql
select pet_name 
from (the table we created in the first part) t1
left join InsuranceModel i
  on i.employee_id = t1.employee_id
where insured = True
```

The full SQL query will look like this:
```sql
select pet_name
from (
	select employee_id, count(*) as pet_count
	from PetsModel p 
	left join EmployeesModel e
	  on e.employee_id = p.employee_id
	group by employee_id
	having count(*) > 1
	) t1
left join InsuranceModel i
  on i.employee_id = t1.employee_id
where insured = True

To transform this into SQLAlchemy ORM syntax, we can break the query into two parts, like we did when constructing the SQL statement.

The first part looks like this:
```python
with AppSession("kungfu_pets") as session:
    t1 = session.query(EmployeesModel.employee_id, func.count(PetsModel.pet_name).label("pet_count"))
    .join(EmployeesModel)
    .group_by(EmployeesModel.employee_id)
    .having(func.count(PetsModel.pet_name) > 1)
    .all()
```


The second part looks like this (we are within the same session):

```python
	session.query(InsuranceModel.pet_name)
	.join(InsuranceModel, InsuranceModel.employee_id==t1.employee_id)
	.filter(InsuranceModel.insurance==True)
	.all()
```

When we combine the two parts, we get something like this:

```python
with AppSession("kungfu_pets") as session:
    t1 = session.query(EmployeesModel.employee_id, func.count(PetsModel.pet_name).label("pet_count"))
    .join(EmployeesModel)
    .group_by(EmployeesModel.employee_id)
    .having(func.count(PetsModel.pet_name) > 1)
    .all()

    session.query(InsuranceModel.pet_name)
	.join(InsuranceModel, InsuranceModel.employee_id==t1.employee_id)
	.filter(InsuranceModel.insurance==True)
	.all()
```


## SQLAlchemy: Loading Relationships for Tables
### Load a relationship with a specific loader options
```python
with AppSession("kungfu_pets") as session:
    session.query(EmployeesModel)
    .options(
        LoaderType(EmployeesModel.relationship)
    )
    .all()
```

where LoaderType can be joinedload(), lazyload(), selectinload().

For more information, visit this link: 
https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html


## Appendix 
### Additional Resources
https://www.essentialsql.com/what-is-the-differenence-between-top-and-offset-fetch/
https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_working_with_joins.htm
https://docs-sqlalchemy.readthedocs.io/ko/latest/orm/tutorial.html 
https://stackoverflow.com/questions/20361017/sqlalchemy-full-outer-join # full outer join


### Future Stuff
We can build a thin abstraction over SQLAlchemy to make it more
approachable to the KungFu team. To do this, we can use these simple
recipes and place them in a package within our library.

(Come up with a plan for how to build this on Monday)

May be a nicer solution
```python
with AppSession("test") as session:
    session\
        .Query(TableModel)\
        .select_by("col1", "col2", "col3")
```



