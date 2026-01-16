from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.domain.models import Mission, Target

class MissionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, mission: Mission) -> Mission:
        self.db.add(mission)
        self.db.commit()
        self.db.refresh(mission)
        return mission

    def get_by_id(self, mission_id: int) -> Optional[Mission]:
        return self.db.query(Mission).options(joinedload(Mission.targets)).filter(Mission.id == mission_id).first()

    def get_all(self) -> List[Mission]:
        return self.db.query(Mission).options(joinedload(Mission.targets)).all()

    def update(self, mission: Mission) -> Mission:
        self.db.commit()
        self.db.refresh(mission)
        return mission

    def delete(self, mission: Mission) -> None:
        self.db.delete(mission)
        self.db.commit()

class TargetRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, target_id: int) -> Optional[Target]:
        return self.db.query(Target).options(joinedload(Target.mission)).filter(Target.id == target_id).first()

    def update(self, target: Target) -> Target:
        self.db.commit()
        self.db.refresh(target)
        return target
