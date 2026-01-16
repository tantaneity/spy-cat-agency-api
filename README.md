# spy cat agency api

fastapi backend for managing spy cats and missions

## tech stack

- fastapi
- postgresql
- sqlalchemy
- docker

## architecture

clean architecture with clear separation:
- domain: business entities
- application: services, dtos, mappers
- infrastructure: repositories, external apis
- presentation: http routes

## setup

local development:

```bash
python -m venv .venv
source .venv/bin/activate  # windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

docker:

```bash
docker-compose up
```

## environment

create `.env` file:

```env
DATABASE_URL=postgresql://spycat:spycat@localhost:5432/spycatdb
CAT_API_URL=https://api.thecatapi.com/v1/breeds
```

## run

local:

```bash
uvicorn app.main:app --reload
```

docker:

```bash
docker-compose up
```

api available at `http://localhost:8000`

docs at `http://localhost:8000/docs`

## api documentation

postman collection: https://consentantaneity-8197353.postman.co/workspace/Tantan's-Workspace~1a5cf94f-15c4-49a5-83cf-6859a08a7127/request/51582497-58455d25-d7ce-451d-a4bb-8a2c80d7c6bc?action=share&creator=51582497&ctx=documentation

## endpoints

### spy cats

- `POST /cats` - create spy cat
- `GET /cats` - list all cats
- `GET /cats/{id}` - get cat by id
- `PATCH /cats/{id}` - update salary
- `DELETE /cats/{id}` - delete cat
- `GET /cats/breeds` - get valid breeds

### missions

- `POST /missions` - create mission
- `GET /missions` - list all missions
- `GET /missions/{id}` - get mission by id
- `PATCH /missions/{id}` - update mission
- `DELETE /missions/{id}` - delete mission
- `PATCH /missions/{id}/targets/{target_id}` - update target notes
- `PATCH /missions/{id}/assign/{cat_id}` - assign cat to mission
- `PATCH /missions/{id}/complete` - complete mission

## validation rules

- breed must be valid from cat api
- cat cannot be deleted if has active mission
- mission cannot be deleted if assigned to cat
- targets cannot be updated once mission is assigned
- only salary and target notes can be updated
