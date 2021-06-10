from sqlalchemy import Column, ForeignKey, Boolean, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from uuid import uuid4

BaseDbModel = declarative_base()


class EmployeeModel(BaseDbModel):
    __tablename__ = "employee"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    employee_name = Column("employee_name", String(100), nullable=False)

    pets = relationship("PetModel", back_populates="employees")


class PetModel(BaseDbModel):
    __tablename__ = "pet"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    pet_name = Column("pet_name", String(100), nullable=True)
    pet_species = Column("pet_species", String(100), nullable=True)
    pet_breed = Column("pet_breed", String(100), nullable=True)
    employee_id = Column(UUID(as_uuid=True), ForeignKey(EmployeeModel.id), nullable=False)

    employees = relationship("EmployeeModel", back_populates="pets")


class OfficePetModel(BaseDbModel):
    __tablename__ = "office_pet"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    pet_breed = Column("pet_breed", String(100))
    allowed_in_office = Column("allowed_in_office", Boolean)


class InsuranceModel(BaseDbModel):
    __tablename__ = "insurance"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    pet_species = Column("pet_species", String(100))
    insurance_cost = Column("insurance_cost", Integer)

