from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.items import router as items_router

app = FastAPI(title="MiniLabel")

# API routes FIRST
app.include_router(items_router)

# Frontend served at /
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")


@app.get("/api")
def health_check():
    return {"status": "MiniLabel API running"}
