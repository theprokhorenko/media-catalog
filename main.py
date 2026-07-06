from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

app = FastAPI()
@app.get("/")
def read_root():
    return {"status": "ok"}

@app.post("/genres", response_model=schemas.GenreRead)
def create_genre(genre: schemas.GenreCreate, db: Session = Depends(get_db)):
    new_genre = models.Genre(name=genre.name)
    db.add(new_genre)
    db.commit()
    db.refresh(new_genre)
    return new_genre

@app.get("/genres", response_model=list[schemas.GenreRead])
def read_genres(db: Session = Depends(get_db)):
    genres = db.query(models.Genre).all()
    return genres

@app.get("/genres/{genre_id}", response_model=schemas.GenreRead)
def read_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = db.query(models.Genre).filter(models.Genre.id == genre_id).first()
    if genre is None:
        raise HTTPException(status_code=404, detail="Жанр не найден")
    return genre

@app.delete("/genres/{genre_id}")
def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = db.query(models.Genre).filter(models.Genre.id == genre_id).first()
    if genre is None:
        raise HTTPException(status_code=404, detail="Жанр не найден")
    db.delete(genre)
    db.commit()
    return {"detail": "Жанр удален"}

@app.put("/genres/{genre_id}", response_model=schemas.GenreRead)
def update_genre(genre_id: int, genre: schemas.GenreCreate, db: Session = Depends(get_db)):
    existing_genre = db.query(models.Genre).filter(models.Genre.id == genre_id).first()
    if existing_genre is None:
        raise HTTPException(status_code=404, detail="Жанр не найден")
    existing_genre.name = genre.name
    db.commit()
    db.refresh(existing_genre)
    return existing_genre