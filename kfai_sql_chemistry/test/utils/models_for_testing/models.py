from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base

BaseModel = declarative_base()


class Person(BaseModel):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
