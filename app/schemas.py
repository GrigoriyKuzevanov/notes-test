from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    username: str
    


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class NoteBase(BaseModel):
    title: str
    content: str


class NoteCreate(NoteBase):
    pass


class NoteOut(NoteBase):
    id: int
    created_at: datetime
    owner: UserOut


    class Config:
        from_attributes = True


