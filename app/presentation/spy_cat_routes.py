from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.application.dto.spy_cat_dto import SpyCatCreate, SpyCatUpdate, SpyCatResponse
from app.application.services.spy_cat_service import SpyCatService
from app.infrastructure.cat_api_client import CatApiClient

router = APIRouter(prefix="/cats", tags=["spy-cats"])

@router.get("/breeds", response_model=List[str])
async def get_breeds():
    client = CatApiClient()
    return await client.get_breeds()

@router.post("", response_model=SpyCatResponse, status_code=status.HTTP_201_CREATED)
async def create_spy_cat(dto: SpyCatCreate, db: Session = Depends(get_db)):
    service = SpyCatService(db)
    return await service.create_spy_cat(dto)

@router.get("/{cat_id}", response_model=SpyCatResponse)
def get_spy_cat(cat_id: int, db: Session = Depends(get_db)):
    service = SpyCatService(db)
    return service.get_spy_cat(cat_id)

@router.get("", response_model=List[SpyCatResponse])
def get_all_spy_cats(db: Session = Depends(get_db)):
    service = SpyCatService(db)
    return service.get_all_spy_cats()

@router.patch("/{cat_id}", response_model=SpyCatResponse)
def update_spy_cat(cat_id: int, dto: SpyCatUpdate, db: Session = Depends(get_db)):
    service = SpyCatService(db)
    return service.update_spy_cat(cat_id, dto)

@router.delete("/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_spy_cat(cat_id: int, db: Session = Depends(get_db)):
    service = SpyCatService(db)
    service.delete_spy_cat(cat_id)
