from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

title_genre = Table(
    "title_genre",
    Base.metadata,
    Column("title_id", Integer, ForeignKey("titles.id")),
    Column("genre_id", Integer, ForeignKey("genres.id")),
)


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    titles = relationship("Title", secondary=title_genre, back_populates="genres")


class Title(Base):
    __tablename__ = "titles"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    media_type = Column(String)
    year = Column(Integer)
    country = Column(String)
    description = Column(Text)
    rating = Column(Float)
    genres = relationship("Genre", secondary=title_genre, back_populates="titles")
