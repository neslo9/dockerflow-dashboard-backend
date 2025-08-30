from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import SessionLocal
from ..core.security import create_access_token
from ..core.config import settings
from jose import jwt, JWTError

router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/token', response_model=schemas.Token)
def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    
    refresh_token_expires = timedelta(days=7)
    refresh_token = create_access_token(data={"sub": user.username, "type": "refresh"}, expires_delta=refresh_token_expires)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=7*24*3600
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post('/refresh', response_model=schemas.Token)
def refresh_token(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing refresh token")
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    access_token = create_access_token(data={"sub": username}, expires_delta=timedelta(minutes=15))
    return {"access_token": access_token, "token_type": "bearer"}
