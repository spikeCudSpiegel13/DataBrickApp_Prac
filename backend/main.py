import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from backend.data.databricks_customers import DatabricksCustomerRepository

logger = logging.getLogger(__name__)

app = FastAPI()
customer_repository = DatabricksCustomerRepository()


@app.get("/api/health")
def health():
    return {"status": "ok", "message": "FastAPI is connected"}


@app.get("/api/v1/customers")
def get_customers():
    try:
        items = customer_repository.list_customers()
        return {"items": items, "count": len(items)}
    except Exception as exc:
        logger.exception("Could not load customers from the data source")
        raise HTTPException(
            status_code=500,
            detail="Could not load customers",
        ) from exc


dist_dir = Path(__file__).resolve().parent.parent / "dist"
app.mount("/", StaticFiles(directory=dist_dir, html=True), name="frontend")