from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import declarative_base, relationship

BaseDBModel = declarative_base()


class Address(BaseDBModel):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)


class Person(BaseDBModel):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    address_id = Column(Integer, ForeignKey('address.id'))

    addresses = relationship(Address)






