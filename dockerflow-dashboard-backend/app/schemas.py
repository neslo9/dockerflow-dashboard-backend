from pydantic import BaseModel

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
