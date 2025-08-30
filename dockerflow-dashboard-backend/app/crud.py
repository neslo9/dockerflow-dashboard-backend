from sqlalchemy.orm import Session
from . import models
from passlib.context import CryptContext
from typing import List

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, username: str, password: str, project_id: int):
    hashed_password = pwd_context.hash(password)
    user = models.User(username=username, hashed_password=hashed_password, project_id=project_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user

def get_images_by_project(db: Session, project_name: str) -> List[models.ImageDetails]:
    """Get all images belonging to a specific project"""
    return db.query(models.ImageDetails).filter(models.ImageDetails.project == project_name).all()
