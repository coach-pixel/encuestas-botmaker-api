from fastapi import FastAPI
from app.routers.surveys import router as surveys_router

app = FastAPI(title="Encuestas Backend", version="1.0.0")

app.include_router(surveys_router, prefix="/surveys", tags=["surveys"])


@app.get("/")
async def root():
    return {"status": "ok", "message": "Backend de encuestas activo"}