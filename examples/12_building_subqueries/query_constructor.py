from db_init import PetSession
from sqlalchemy.orm import load_only
from models.kfai_pets_model import OfficePetModel


def query_select_columns():
    with PetSession() as session:
        result = (
            session.query(
                OfficePetModel.pet_breed,
                OfficePetModel.allowed_in_office
            ).all())
        session.expunge_all()
        print("SELECT clause")
        print([r for r in result])


def load_select_columns():
    with PetSession() as session:
        result = (
            session.query(OfficePetModel)
            .options(load_only("pet_breed", "allowed_in_office"))
            .all())
        session.expunge_all()
        print("SELECT with load_only")
        print([r for r in result])


def rename_columns():
    with PetSession() as session:
        result = (
            session.query(
                OfficePetModel.pet_breed.label("breed"),
                OfficePetModel.allowed_in_office.label("allowed")
            ).all())
        print("SELECT AS clause")
        print(result[0].keys())