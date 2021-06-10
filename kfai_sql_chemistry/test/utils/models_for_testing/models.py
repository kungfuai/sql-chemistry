from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import declarative_base, relationship

BaseModel = declarative_base()


class Address(BaseModel):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)


class Person(BaseModel):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    address_id = Column(Integer, ForeignKey('address.id'))

    addresses = relationship(Address)






