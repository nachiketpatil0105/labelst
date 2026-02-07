from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.items import router as items_router

app = FastAPI(title="MiniLabel")

# API routes
app.include_router(items_router, prefix="/api")

@app.get("/api")
def api_root():
    return {"status": "MiniLabel API running"}

# Frontend
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
