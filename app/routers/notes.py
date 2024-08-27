from fastapi import APIRouter, status, Depends, HTTPException
from app import schemas, models, oauth2
from app.database import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)


@router.get("/", response_model=list[schemas.NoteOut])
def get_notes(limit: int = 10, skip: int = 0, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    stmt = select(models.Note).filter(models.Note.owner_id == current_user.id).limit(limit).offset(skip)
    result = db.execute(stmt).all()
    
    notes = []
    for row in result:
        notes.append(row[0])

    return notes


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.NoteOut)
def create_note(note: schemas.NoteCreate, owner_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_note = models.Note(**note.model_dump(), owner_id=current_user.id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note
