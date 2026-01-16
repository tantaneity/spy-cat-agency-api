from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

class TargetCreate(BaseModel):
    name: str
    country: str
    notes: str = ""

class TargetUpdate(BaseModel):
    notes: Optional[str] = None
    is_complete: Optional[bool] = None

class TargetResponse(BaseModel):
    id: int
    name: str
    country: str
    notes: str
    is_complete: bool

    class Config:
        from_attributes = True

class MissionCreate(BaseModel):
    targets: List[TargetCreate] = Field(min_length=1, max_length=3)

    @field_validator('targets')
    @classmethod
    def validate_targets_count(cls, v):
        if not 1 <= len(v) <= 3:
            raise ValueError('mission must have between 1 and 3 targets')
        return v

class MissionAssignCat(BaseModel):
    cat_id: int

class MissionResponse(BaseModel):
    id: int
    cat_id: Optional[int]
    is_complete: bool
    targets: List[TargetResponse]

    class Config:
        from_attributes = True
