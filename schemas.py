from pydantic import BaseModel, ConfigDict

class GenreCreate(BaseModel):
    name: str
    
class GenreRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str