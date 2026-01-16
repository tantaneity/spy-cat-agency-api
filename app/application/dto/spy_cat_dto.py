from pydantic import BaseModel, Field
from typing import Optional

class SpyCatCreate(BaseModel):
    name: str
    years_of_experience: int = Field(ge=0)
    breed: str
    salary: float = Field(ge=0)

class SpyCatUpdate(BaseModel):
    salary: float = Field(ge=0)

class SpyCatResponse(BaseModel):
    id: int
    name: str
    years_of_experience: int
    breed: str
    salary: float

    class Config:
        from_attributes = True
