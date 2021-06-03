from logging import PercentStyle
from sqlalchemy import Column, ForeignKey, Integer, Boolean, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from uuid import uuid4

BaseDbModel = declarative_base()

class EmployeeModel(BaseDbModel):
    __tablename__ = "employee"

    id = Column(UUID(as_uuid=True), primary_key=True, autoincrement=True, default=uuid4)
    employee_name = Column("employee_name", String(100), nullable=False)

    pets = relationship("PetModel", back_populates="employees", lazy="joined")
    insurance = relationship("InsuranceModel", back_populates="employees")


class PetModel(BaseDbModel):
    __tablename__ = "pet"

    id = Column(UUID(as_uuid=True), primary_key=True, autoincrement=True, default=uuid4)
    pet_name = Column("pet_name", String(100), nullable=True)
    employee_id = Column(ForeignKey(EmployeeModel.id))

    employees = relationship("EmployeeModel", back_populates="pets")
    petinfo = relationship("PetInfoModel", back_populates="pets")


class PetInfoModel(BaseDbModel):
    __tablename__ = "pet_info"

    id = Column(UUID(as_uuid=True), primary_key=True, autoincrement=True, default=uuid4)
    pet_id = Column(ForeignKey(PetModel.id))
    pet_species = Column("pet_species", String(100), nullable=True)
    pet_breed = Column("pet_breed", String(100), nullable=True)

    pets = relationship("PetModel", back_populates="petinfo")
    officepets = relationship("OfficePetModel", back_populates="petinfo")


class InsuranceModel(BaseDbModel):
    __tablename__ = "insurance"

    id = Column(UUID(as_uuid=True), primary_key=True, autoincrement=True, default=uuid4)
    employee_id = Column(ForeignKey(EmployeeModel.id))
    pet_id = Column(ForeignKey(PetModel.id))
    insured = Column("insured", Boolean)

    employees = relationship("EmployeeModel", back_populates="insurance")


class OfficePetModel(BaseDbModel):
    __tablename__ = "office_pet"

    id = Column(UUID(as_uuid=True), primary_key=True, autoincrement=True, default=uuid4)
    pet_breed = Column(ForeignKey(PetInfoModel.pet_breed))
    allowed_in_office = Column("allowed_in_office", Boolean)

    petinfo = relationship("PetInfoModel", back_populates="officepets")
    