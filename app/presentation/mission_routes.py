from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.application.dto.mission_dto import MissionCreate, MissionResponse, TargetUpdate, MissionAssignCat
from app.application.services.mission_service import MissionService

router = APIRouter(prefix="/missions", tags=["missions"])

@router.post("", response_model=MissionResponse, status_code=status.HTTP_201_CREATED)
def create_mission(dto: MissionCreate, db: Session = Depends(get_db)):
    service = MissionService(db)
    return service.create_mission(dto)

@router.get("/{mission_id}", response_model=MissionResponse)
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    service = MissionService(db)
    return service.get_mission(mission_id)

@router.get("", response_model=List[MissionResponse])
def get_all_missions(db: Session = Depends(get_db)):
    service = MissionService(db)
    return service.get_all_missions()

@router.delete("/{mission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    service = MissionService(db)
    service.delete_mission(mission_id)

@router.post("/{mission_id}/assign", response_model=MissionResponse)
def assign_cat_to_mission(mission_id: int, dto: MissionAssignCat, db: Session = Depends(get_db)):
    service = MissionService(db)
    return service.assign_cat(mission_id, dto)

@router.patch("/targets/{target_id}", response_model=MissionResponse)
def update_target(target_id: int, dto: TargetUpdate, db: Session = Depends(get_db)):
    service = MissionService(db)
    return service.update_target(target_id, dto)
