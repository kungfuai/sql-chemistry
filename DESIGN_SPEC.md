
## Problem
- SQLAlchemy is new to the team
- There is alot of ways to do it un-scalably, and we want to reduce the surface area
of problems for the team for the easiest adoption
  

## Potential Solutions
- Creating a Thin Abstraction over SQLAlchemy for Queries
- Creating a recipe guidebook in Confluence and/or this repo

## Examples and Use Cases


#### Selecting certain columns
There are two ways to do this:
```python
with AppSession("test") as session:
    session.query(TableModel.column1, TableModel.column2)
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

#### Filtering ("where" clause in SQL)
There are two ways to filter:
```python
with AppSession("test") as session:
    session.query(TableModel)
    .filter(TableModel.column==value)
    .all()
```

and 
```python
with AppSession("test") as session:
    session.query(TableModel)
    .filter_by(column=value)
    .all()
```

Both do the same things, but the syntax is slightly different.
To do functions, using filter is easier because you can do it without function calls.

#### Filter using an list of items ("in" operator in SQL)
```python
with AppSession("test") as session:
    session.query(TableModel)
    .filter(TableModel.column._in(list_of_values))
    .all()
```

This is useful when you have a pre-defined list of values that you want 
to search for in a column.

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


#### Future Stuff

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
