from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.domain.models import SpyCat
from app.application.dto.spy_cat_dto import SpyCatCreate, SpyCatUpdate, SpyCatResponse
from app.application.mappers import SpyCatMapper
from app.infrastructure.spy_cat_repository import SpyCatRepository
from app.infrastructure.cat_api_client import CatApiClient

class SpyCatService:
    def __init__(self, db: Session):
        self.repository = SpyCatRepository(db)
        self.cat_api_client = CatApiClient()

    async def create_spy_cat(self, dto: SpyCatCreate) -> SpyCatResponse:
        is_valid_breed = await self.cat_api_client.validate_breed(dto.breed)
        if not is_valid_breed:
            raise HTTPException(status_code=400, detail="invalid breed")

        spy_cat = SpyCatMapper.to_entity(dto)
        created_cat = self.repository.create(spy_cat)
        return SpyCatMapper.to_response(created_cat)

    def get_spy_cat(self, cat_id: int) -> SpyCatResponse:
        spy_cat = self.repository.get_by_id(cat_id)
        if not spy_cat:
            raise HTTPException(status_code=404, detail="spy cat not found")
        return SpyCatMapper.to_response(spy_cat)

    def get_all_spy_cats(self) -> List[SpyCatResponse]:
        spy_cats = self.repository.get_all()
        return [SpyCatMapper.to_response(cat) for cat in spy_cats]

    def update_spy_cat(self, cat_id: int, dto: SpyCatUpdate) -> SpyCatResponse:
        spy_cat = self.repository.get_by_id(cat_id)
        if not spy_cat:
            raise HTTPException(status_code=404, detail="spy cat not found")

        spy_cat.salary = dto.salary
        updated_cat = self.repository.update(spy_cat)
        return SpyCatMapper.to_response(updated_cat)

    def delete_spy_cat(self, cat_id: int) -> None:
        spy_cat = self.repository.get_by_id(cat_id)
        if not spy_cat:
            raise HTTPException(status_code=404, detail="spy cat not found")

        if self.repository.has_active_mission(cat_id):
            raise HTTPException(status_code=400, detail="cannot delete cat with active mission")

        self.repository.delete(spy_cat)
