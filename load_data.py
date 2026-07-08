import pandas as pd
from database import SessionLocal
import models

df = pd.read_csv("netflix_titles.csv")
db = SessionLocal()

genre_cache = {}


def get_or_create_genre(name):
    name = name.strip()
    if name in genre_cache:
        return genre_cache[name]
    genre = db.query(models.Genre).filter(models.Genre.name == name).first()
    if genre is None:
        genre = models.Genre(name=name)
        db.add(genre)
    genre_cache[name] = genre
    return genre


for _, row in df.iterrows():
    genres = []
    if pd.notna(row["listed_in"]):
        for genre_name in row["listed_in"].split(","):
            genres.append(get_or_create_genre(genre_name))

    title = models.Title(
        name=row["title"],
        media_type=row["type"],
        country=row["country"] if pd.notna(row["country"]) else None,
        year=int(row["release_year"]) if pd.notna(row["release_year"]) else None,
        description=row["description"] if pd.notna(row["description"]) else None,
    )
    title.genres = genres
    db.add(title)

db.commit()
db.close()
print(f"Загружено тайтлов: {len(df)}")
