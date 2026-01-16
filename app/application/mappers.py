from app.domain.models import SpyCat, Mission, Target
from app.application.dto.spy_cat_dto import SpyCatCreate, SpyCatResponse
from app.application.dto.mission_dto import MissionResponse, TargetResponse

class SpyCatMapper:
    @staticmethod
    def to_entity(dto: SpyCatCreate) -> SpyCat:
        return SpyCat(
            name=dto.name,
            years_of_experience=dto.years_of_experience,
            breed=dto.breed,
            salary=dto.salary
        )

    @staticmethod
    def to_response(entity: SpyCat) -> SpyCatResponse:
        return SpyCatResponse(
            id=entity.id,
            name=entity.name,
            years_of_experience=entity.years_of_experience,
            breed=entity.breed,
            salary=entity.salary
        )

class TargetMapper:
    @staticmethod
    def to_response(entity: Target) -> TargetResponse:
        return TargetResponse(
            id=entity.id,
            name=entity.name,
            country=entity.country,
            notes=entity.notes,
            is_complete=entity.is_complete
        )

class MissionMapper:
    @staticmethod
    def to_response(entity: Mission) -> MissionResponse:
        return MissionResponse(
            id=entity.id,
            cat_id=entity.cat_id,
            is_complete=entity.is_complete,
            targets=[TargetMapper.to_response(t) for t in entity.targets]
        )
