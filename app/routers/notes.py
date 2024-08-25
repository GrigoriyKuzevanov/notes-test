from fastapi import APIRouter, status
from app import schemas


router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)


@router.get("/")
def get_notes(limit: int = 10, skip: int = 0):
    return {"message": "success"}


@router.post("/", response_model=schemas.NoteOut, status_code=status.HTTP_201_CREATED)
def create_note(note: schemas.NoteCreate):
    return {"message": "success"}
