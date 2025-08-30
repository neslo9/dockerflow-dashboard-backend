from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    username: str
    password: str
    project_id: int

class User(BaseModel):
    id: int
    username: str
    project_id: int

    class Config:
        orm_mode = True

class Project(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class Image(BaseModel):
    id: int
    repo_name: str
    image_name: str
    image_tag: str
    build_status: str
    deploy_status: str
    security_checks: Optional[Dict[str, Any]]
    vulnerabilities: Optional[Dict[str, Any]]
    project: str
    created_at: datetime

    class Config:
        orm_mode = True
