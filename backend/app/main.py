"""Read-only FastAPI layer for the AI Deal Discovery Agent prototype."""
import json
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query

from recommendations import PERSONAS, recommend_products

ROOT = Path(__file__).resolve().parents[2]
CATALOGUE_PATH = ROOT / "data" / "products.json"

app = FastAPI(
    title="AakankshLabs AI Deal Discovery API",
    description="Prototype API over synthetic sample products only; no live retailer inventory or pricing is connected.",
    version="0.1.0",
)


def load_catalogue() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Load the checked-in sample catalogue."""
    try:
        with CATALOGUE_PATH.open("r", encoding="utf-8") as file:
            payload = json.load(file)
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError("The product catalogue could not be loaded.") from exc
    products = payload.get("products")
    if not isinstance(products, list):
        raise RuntimeError("The product catalogue has an invalid products field.")
    return payload, products


@app.get("/health", tags=["operations"])
def health() -> dict[str, str]:
    """Process health, not a database readiness check."""
    return {"status": "ok", "service": "ai-deal-discovery-api"}


@app.get("/api/v1/catalogue", tags=["catalogue"])
def catalogue_summary() -> dict[str, Any]:
    """Expose metadata while clearly labelling synthetic records."""
    try:
        metadata, products = load_catalogue()
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return {
        "catalogue_name": metadata.get("catalogue_name"),
        "version": metadata.get("version"),
        "record_count": len(products),
        "currency": metadata.get("currency", "INR"),
        "data_status": metadata.get("data_status", "unknown"),
        "disclaimer": metadata.get("disclaimer"),
    }


@app.get("/api/v1/products/search", tags=["products"])
def search_products(
    q: str = Query(min_length=1, max_length=120),
    budget_inr: float = Query(gt=0, le=1_000_000),
    persona: str | None = Query(default=None),
    limit: int = Query(default=10, ge=1, le=50),
) -> dict[str, Any]:
    """Search using the existing deterministic baseline recommender."""
    query = q.strip()
    if not query:
        raise HTTPException(status_code=422, detail="Search query cannot be blank.")
    if persona is not None and persona not in PERSONAS:
        raise HTTPException(
            status_code=422,
            detail={"message": "Unknown persona.", "valid_personas": list(PERSONAS)},
        )
    try:
        metadata, products = load_catalogue()
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    results = recommend_products(products, query, budget_inr, persona)
    return {
        "query": query,
        "budget_inr": budget_inr,
        "persona": persona,
        "result_count": min(len(results), limit),
        "data_status": metadata.get("data_status", "unknown"),
        "disclaimer": metadata.get("disclaimer"),
        "results": results[:limit],
    }
