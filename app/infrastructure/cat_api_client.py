import httpx
from typing import List, Optional
from app.config import settings

class CatApiClient:
    def __init__(self):
        self.base_url = settings.cat_api_url

    async def get_breeds(self) -> List[str]:
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url)
            response.raise_for_status()
            breeds = response.json()
            return [breed['name'] for breed in breeds]

    async def validate_breed(self, breed: str) -> bool:
        breeds = await self.get_breeds()
        return breed in breeds
