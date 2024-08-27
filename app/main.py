from fastapi import FastAPI
from app.routers import notes, users
from app import models
from app.database import engine


# models.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(notes.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Welcome to Notes API"}
