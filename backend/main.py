from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()


@app.get("/api/health")
def health():
    return {"status": "ok", "message": "FastAPI is connected"}


dist_dir = Path(__file__).resolve().parent.parent / "dist"
app.mount("/", StaticFiles(directory=dist_dir, html=True), name="frontend")