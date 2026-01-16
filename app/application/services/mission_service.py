from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.domain.models import Mission, Target
from app.application.dto.mission_dto import MissionCreate, MissionResponse, TargetUpdate, MissionAssignCat
from app.application.mappers import MissionMapper
from app.infrastructure.mission_repository import MissionRepository, TargetRepository
from app.infrastructure.spy_cat_repository import SpyCatRepository

class MissionService:
    def __init__(self, db: Session):
        self.repository = MissionRepository(db)
        self.target_repository = TargetRepository(db)
        self.cat_repository = SpyCatRepository(db)

    def create_mission(self, dto: MissionCreate) -> MissionResponse:
        mission = Mission(is_complete=False)
        
        for target_dto in dto.targets:
            target = Target(
                name=target_dto.name,
                country=target_dto.country,
                notes=target_dto.notes,
                is_complete=False
            )
            mission.targets.append(target)

        created_mission = self.repository.create(mission)
        return MissionMapper.to_response(created_mission)

    def get_mission(self, mission_id: int) -> MissionResponse:
        mission = self.repository.get_by_id(mission_id)
        if not mission:
            raise HTTPException(status_code=404, detail="mission not found")
        return MissionMapper.to_response(mission)

    def get_all_missions(self) -> List[MissionResponse]:
        missions = self.repository.get_all()
        return [MissionMapper.to_response(mission) for mission in missions]

    def delete_mission(self, mission_id: int) -> None:
        mission = self.repository.get_by_id(mission_id)
        if not mission:
            raise HTTPException(status_code=404, detail="mission not found")

        if mission.cat_id is not None:
            raise HTTPException(status_code=400, detail="cannot delete mission assigned to a cat")

        self.repository.delete(mission)

    def assign_cat(self, mission_id: int, dto: MissionAssignCat) -> MissionResponse:
        mission = self.repository.get_by_id(mission_id)
        if not mission:
            raise HTTPException(status_code=404, detail="mission not found")

        cat = self.cat_repository.get_by_id(dto.cat_id)
        if not cat:
            raise HTTPException(status_code=404, detail="cat not found")

        if self.cat_repository.has_active_mission(dto.cat_id):
            raise HTTPException(status_code=400, detail="cat already has an active mission")

        mission.cat_id = dto.cat_id
        updated_mission = self.repository.update(mission)
        return MissionMapper.to_response(updated_mission)

    def update_target(self, target_id: int, dto: TargetUpdate) -> MissionResponse:
        target = self.target_repository.get_by_id(target_id)
        if not target:
            raise HTTPException(status_code=404, detail="target not found")

        mission = target.mission

        if dto.notes is not None:
            if target.is_complete or mission.is_complete:
                raise HTTPException(status_code=400, detail="cannot update notes for completed target or mission")
            target.notes = dto.notes

        if dto.is_complete is not None:
            target.is_complete = dto.is_complete

        self.target_repository.update(target)

        all_targets_complete = all(t.is_complete for t in mission.targets)
        if all_targets_complete and not mission.is_complete:
            mission.is_complete = True
            self.repository.update(mission)

        return MissionMapper.to_response(mission)
