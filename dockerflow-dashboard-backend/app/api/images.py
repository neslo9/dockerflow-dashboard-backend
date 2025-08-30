from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from .. import crud, schemas, models
from ..database import SessionLocal
from fastapi.security import OAuth2PasswordBearer
from ..core.config import settings
from jose import jwt, JWTError
from typing import List

router = APIRouter(prefix="/images", tags=["images"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(request: Request, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    auth_header_token = token
    cookie_token = request.cookies.get("access_token")
    actual_token = auth_header_token or cookie_token
    if not actual_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        payload = jwt.decode(actual_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

@router.get("/project/{project_name}", response_model=List[schemas.Image])
def get_images_by_project(
    project_name: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Get all images belonging to a specific project.
    Requires authentication.
    """
    images = crud.get_images_by_project(db, project_name)
    return images
