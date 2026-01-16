from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.domain.models import SpyCat

class SpyCatRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, spy_cat: SpyCat) -> SpyCat:
        self.db.add(spy_cat)
        self.db.commit()
        self.db.refresh(spy_cat)
        return spy_cat

    def get_by_id(self, cat_id: int) -> Optional[SpyCat]:
        return self.db.query(SpyCat).filter(SpyCat.id == cat_id).first()

    def get_all(self) -> List[SpyCat]:
        return self.db.query(SpyCat).all()

    def update(self, spy_cat: SpyCat) -> SpyCat:
        self.db.commit()
        self.db.refresh(spy_cat)
        return spy_cat

    def delete(self, spy_cat: SpyCat) -> None:
        self.db.delete(spy_cat)
        self.db.commit()

    def has_active_mission(self, cat_id: int) -> bool:
        cat = self.db.query(SpyCat).options(joinedload(SpyCat.mission)).filter(SpyCat.id == cat_id).first()
        return cat is not None and cat.mission is not None
