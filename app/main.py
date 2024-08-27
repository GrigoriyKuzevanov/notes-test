from fastapi import FastAPI

from app import models
from app.database import engine
from app.routers import auth, notes, users

# models.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(notes.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Welcome to Notes API"}
