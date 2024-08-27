from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, oauth2, schemas
from app.database import get_db
from app.yandex_speller import verify_with_speller

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)


@router.get("/", response_model=list[schemas.NoteOut])
def get_notes(
    limit: int = 10,
    skip: int = 0,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    stmt = (
        select(models.Note)
        .filter(models.Note.owner_id == current_user.id)
        .limit(limit)
        .offset(skip)
    )
    result = db.execute(stmt).all()

    notes = []
    for row in result:
        notes.append(row[0])

    return notes


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.NoteOut)
def create_note(
    note: schemas.NoteCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    spell_response = verify_with_speller(
        note.content,
        HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Yandex Speller sevice is not available",
        ),
    )

    if spell_response:
        detail_spell = [{i.get("word"): i.get("s")} for i in spell_response]
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"errors in content: {detail_spell}",
        )

    new_note = models.Note(**note.model_dump(), owner_id=current_user.id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note


@router.put("/{note_id}", response_model=schemas.NoteOut)
def update_note(
    note_id: int,
    note: schemas.NoteCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    
    spell_response = verify_with_speller(
        note.content,
        HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Yandex Speller sevice is not available",
        ),
    )

    if spell_response:
        detail_spell = [{i.get("word"): i.get("s")} for i in spell_response]
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"errors in content: {detail_spell}",
        )

    updated_note = db.get(models.Note, note_id)

    if updated_note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id: {note_id} was not found",
        )

    if updated_note.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    for key, value in note.model_dump(exclude_unset=True).items():
        setattr(updated_note, key, value)

    db.commit()
    db.refresh(updated_note)

    return updated_note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    deleted_note = db.get(models.Note, note_id)

    if deleted_note is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    if deleted_note.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    db.delete(deleted_note)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
