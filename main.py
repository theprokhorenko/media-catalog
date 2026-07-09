from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

app = FastAPI()


@app.get("/")
def read_root():
    return {"status": "ok"}


@app.get("/app", response_class=HTMLResponse)
def serve_app():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()


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
def update_genre(
    genre_id: int, genre: schemas.GenreCreate, db: Session = Depends(get_db)
):
    existing_genre = db.query(models.Genre).filter(models.Genre.id == genre_id).first()
    if existing_genre is None:
        raise HTTPException(status_code=404, detail="Жанр не найден")
    existing_genre.name = genre.name
    db.commit()
    db.refresh(existing_genre)
    return existing_genre


@app.post("/titles", response_model=schemas.TitleRead)
def create_title(title: schemas.TitleCreate, db: Session = Depends(get_db)):
    new_title = models.Title(
        name=title.name,
        media_type=title.media_type,
        year=title.year,
        country=title.country,
        director=title.director,
        description=title.description,
        rating=title.rating,
    )
    genres = db.query(models.Genre).filter(models.Genre.id.in_(title.genre_ids)).all()
    new_title.genres = genres
    db.add(new_title)
    db.commit()
    db.refresh(new_title)
    return new_title


@app.get("/titles", response_model=list[schemas.TitleRead])
def read_titles(
    skip: int = 0,
    limit: int = 20,
    search: str | None = None,
    media_type: str | None = None,
    genre: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Title)
    if search is not None:
        query = query.filter(models.Title.name.contains(search))
    if media_type is not None:
        query = query.filter(models.Title.media_type == media_type)
    if genre is not None:
        query = query.filter(models.Title.genres.any(models.Genre.name == genre))
    titles = query.offset(skip).limit(limit).all()
    return titles


@app.get("/titles/{title_id}", response_model=schemas.TitleRead)
def read_title(title_id: int, db: Session = Depends(get_db)):
    title = db.query(models.Title).filter(models.Title.id == title_id).first()
    if title is None:
        raise HTTPException(status_code=404, detail="Тайтл не найден")
    return title


@app.get("/titles/{title_id}/recommendations", response_model=list[schemas.TitleRead])
def recommendations(title_id: int, db: Session = Depends(get_db)):
    title = db.query(models.Title).filter(models.Title.id == title_id).first()
    if title is None:
        raise HTTPException(status_code=404, detail="Тайтл не найден")

    title_genres = set([g.name for g in title.genres])
    title_director = title.director

    other_titles = db.query(models.Title).filter(models.Title.id != title.id).all()
    scored = []
    for other in other_titles:
        other_genres = set(g.name for g in other.genres)
        score = len(title_genres & other_genres)
        if title_director is not None and title_director == other.director:
            score += 3
        if score > 0:
            scored.append((other, score))

    scored = sorted(scored, key=lambda x: x[1], reverse=True)
    return [t for t, score in scored[:5]]
