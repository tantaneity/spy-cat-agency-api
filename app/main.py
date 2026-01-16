from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.presentation.spy_cat_routes import router as spy_cat_router
from app.presentation.mission_routes import router as mission_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Spy Cat Agency API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(spy_cat_router)
app.include_router(mission_router)

@app.get("/")
def root():
    return {"message": "spy cat agency api"}
