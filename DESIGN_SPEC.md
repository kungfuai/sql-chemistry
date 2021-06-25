
## Problem
- SQLAlchemy is new to the team
- There is alot of ways to do it un-scalably, and we want to reduce the surface area
of problems for the team for the easiest adoption
  

## Potential Solutions
- Creating a Thin Abstraction over SQLAlchemy for Queries
- Creating a recipe guidebook in Confluence and/or this repo

## Examples and Use Cases


#### Selecting certain columns ("select" clause in SQL)
The SQL example we are trying to do:
```sql
select column1, column2, column3
from TableModel
```

There are two ways to do this:
```python
with AppSession("test") as session:
    session.query(TableModel.column1, TableModel.column2, TableModel.column3)
    .all()
```
and

```python
with AppSession("test") as session:
    session.query(TableModel)
    .options(
        load_only(
            "column1",
            "column2",
            "column3",
        )
    )
    .all()
```

To see an example, look at the "using Aliases" section of the docs here:
https://docs.sqlalchemy.org/en/14/orm/tutorial.html#querying

#### Labeling columns with aliases ("as" in SQL)
The SQL example we are trying to do:
```sql
select column1 as dog_name, column2 as dog_breed, column3 as dog_cuteness_level
from TableModel
```

This can be done in SQL Alchemy ORM like this:
```python
with AppSession("test") as session:
    session.query(
        TableModel.column1.label("dog_name"),
        TableModel.column2.label("dog_breed"),
        TableModel.column3.label("dog_cuteness_level")
        )
    .all()
```

#### Limiting results of a query ("limit" clause in SQL)
The SQL example we are trying to do:
```sql
select column1 as dog_name, column2 as dog_breed, column3 as dog_cuteness_level
from TableModel
limit 100
```

This can be done in SQL Alchemy ORM like this:
```python
with AppSession("test") as session:
    session.query(
        TableModel.column1.label("dog_name"),
        TableModel.column2.label("dog_breed"),
        TableModel.column3.label("dog_cuteness_level")
        )
    .limit(100)
```


#### Filtering results by a condition ("where" clause in SQL)
The SQL example we are trying to do:
```sql
select *
from TableModel
where column3 = 10
```

There are two ways to filter:
```python
with AppSession("test") as session:
    session.query(TableModel)
    .filter(TableModel.column3==10)
    .all()
```

and 
```python
with AppSession("test") as session:
    session.query(TableModel)
    .filter_by(column3=10)
    .all()
```

Both do the same things, but the syntax is slightly different. To do functions, using filter is easier because you can do it without function calls.

To apply another operator, instead of "==" or "=", you can type in ">" for greater than, ">=" for greater than or equals to, "<" for less than, ">=" for less than or equals to and "!=" for does not equals.


#### Filtering using a list of items ("in" operator in SQL)
The SQL example we are trying to do:
```sql
select *
from TableModel
where column3 in ('Krishna', 'Felix', 'Zhenchen')
```

To do this, we can define a list or a tuple with the values we want, as below:

```python
list_of_values = ['Krishna', 'Felix', 'Zhenchen']

with AppSession("test") as session:
    session.query(TableModel)
    .filter(TableModel.column3._in(list_of_values))
    .all()
```

This is useful when you have a pre-defined list of values that you want to search for in a column.

Look at this stackoverflow to see more: https://stackoverflow.com/questions/8603088/sqlalchemy-in-clause


#### Excluding using a list of items ("not in" operator in SQL)
The SQL example we are trying to do:
```sql
select *
from TableModel
where column3 not in ('Krishna', 'Felix', 'Zhenchen')
```
There are two ways to do this. As with the "in" operator, we need to define a list of the values we want to exclude.

The first way is this:
```python
list_of_values = ['Krishna', 'Felix', 'Zhenchen']

with AppSession("test") as session:
    session.query(TableModel)
    .filter(not_(TableModel.column3._in(list_of_values)))
    .all()
```

and the second way is to do this:
```python
list_of_values = ['Krishna', 'Felix', 'Zhenchen']

with AppSession("test") as session:
    session.query(TableModel)
    .filter(TableModel.column3._in(list_of_values))
    .all()
```

This is useful when you have a pre-defined list of values that you want to exclude from a search.

#### Joining another table with one foreign key ("join" clause in SQL)
The SQL example we are trying to do:
```sql
select *
from TableModel t
join ExampleModel e
  on e.example_colukmn = t.table_column
```
There are two ways to do this. The first is to use the filter function in SQL Alchemy ORM to combine two tables based on the equivalency of values for a column.

To do this, we write:
```python
with AppSession("test") as session:
    session.query(TableModel, ExampleModel)
    .filter(TableModel.table_column==ExampleModel.example_column)
    .all()
```

However, if there is a foreign key, we can also use the join syntax from SQL Alchemy ORM and join based on the foreign key.
```python
list_of_values = ['Krishna', 'Felix', 'Zhenchen']

with AppSession("test") as session:
    session.query(TableModel).join(ExampleModel)
    .all()
```

If there is not one foreign key, look below to see how to use the join syntax appropriately.

<mark>Note: by default, "join" refers to inner joins. To do an outer join, replace "join" with "outerjoin" in the example above.</mark>

For left and right joins, look below.

#### Joining in a direction another table with one foreign key "left/right [outer] join" clause in SQL)
With joins, we can join in a specific direction (left or right). With a left join, which in PostgreSQL and MySQL are equivalent to left outer joins, we include everything that is in the table listed in the from clause, and whatever is found based on the join key in the left join clause.  For a right join, which is a right outer join in PostgreSQL and MySQL, the opposite happens. Everything in the right join clause is included, and whatever is found based on the join key in the table in the from caluse is included. A visual to help can be found here: https://www.codeproject.com/Articles/33052/Visual-Representation-of-SQL-Joins

And a textual explanation can be found here: https://stackoverflow.com/questions/15425740/are-left-outer-joins-and-left-joins-the-same

In essence, a left join and right join are just opposites, and flipping the order that the tables are joined in the query results in the opposing join type. SQL syntax makes a distinction, but SQLAlchemy ORM does not - instead, the order the tables are referred to are what determines what direction the join happens in and what data is included.

The SQL example for a left join is:
```sql
select *
from TableModel t
left join ExampleModel e
  on e.example_colukmn = t.table_column
```

To do this, we use the outerjoin function.

```python
with AppSession("test") as session:
    session.query(TableModel).outerjoin(ExampleModel)
    .all()
```

The SQL example for a right join is:
```sql
select *
from TableModel t
right join ExampleModel e
  on e.example_colukmn = t.table_column
```

To do this, we use the outerjoin function.

```python
with AppSession("test") as session:
    session.query(ExampleModel).outerjoin(TableModel)
    .all()
```

SQLAlchemy ORM takes away the distinction and thus lets the order of tables guide the data included. The query function holds the table that you want to include all the data for, and the outerjoin 

#### Joining another table with one foreign key ("join" clause in SQL)

If there is not just one foreign key (none or more), then we can 


https://www.essentialsql.com/what-is-the-differenence-between-top-and-offset-fetch/

https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_working_with_joins.htm

https://docs-sqlalchemy.readthedocs.io/ko/latest/orm/tutorial.html 

https://stackoverflow.com/questions/20361017/sqlalchemy-full-outer-join # full outer join



#### Subquerying using the query function
The SQL example we are trying to do:
```sql
select column1 as dog_name, column2 as dog_breed, column3 as dog_cuteness_level
from (
    select *
    from 
)
limit 100
```

Leverage the query function to "create" a table from a subquery.

```python
with AppSession("test") as session:
    session.query(
        TableModel.column1
    )

```

#### Load a relationship with a specific loader option
```python
with AppSession("test") as session:
    session.query(TableModel)
    .options(
        LoaderType(TableModel.relationship)
    )
    .all()
```

where LoaderType can be joinedload(), lazyload(), selectinload().

For more information, visit this link: 
https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html

#### To retreive one instance of a primary key, we can use the identity map of the session
```python
with AppSession("test") as session:
    session.query(TableModel)
    .get(column)
```

The get() function is preferred over filter() when retrieving
a specific instance of a primary key identifier that is located in the
identity map of a session because it returns the result directly 
without emitting SQL, and raises an error if the object is expired
or not present.

To learn more about get, read here:
https://docs.sqlalchemy.org/en/14/orm/query.html

