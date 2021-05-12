
## Problem
- SQLAlchemy is new to the team
- There is alot of ways to do it un-scalably, and we want to reduce the surface area
of problems for the team for the easiest adoption
  

## Potential Solutions
- Creating a Thin Abstraction over SQLAlchemy for Queries
- Creating a recipe guidebook in Confluence and/or this repo

## Examples and Use Cases


#### Simple Projection Case 1

Select a couple of columns instead of all of the columns on demand easily.

SELECT col1, col2, col3 FROM TableModel

How we may implement this in sql alchemy with our standards
```python
with AppSession("test") as session:
    session.query(TableModel)
    .options(
        load_only(
            "col1",
            "col2",
            "col3",
        )
    )
    .all()
```

May be a nicer solution
```python
with AppSession("test") as session:
    session\
        .Query(TableModel)\
        .select_by("col1", "col2", "col3")
```
