from pydantic import BaseModel, ConfigDict


class GenreCreate(BaseModel):
    name: str


class GenreRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class TitleCreate(BaseModel):
    name: str
    media_type: str | None = None
    year: int | None = None
    country: str | None = None
    description: str | None = None
    rating: float | None = None
    genre_ids: list[int] = []


class TitleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    media_type: str | None = None
    year: int | None = None
    country: str | None = None
    director: str | None = None
    description: str | None = None
    rating: float | None = None
    genres: list[GenreRead] = []
