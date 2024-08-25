from pydantic import BaseModel
from datetime import datetime


class NoteBase(BaseModel):
    title: str
    content: str


class NoteCreate(NoteBase):
    pass


class NoteOut(NoteBase):
    created_at: datetime
    id: int
