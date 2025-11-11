import os
from typing import List, Optional, Any, Dict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId

from database import create_document, get_documents, db
from schemas import Dataset, Tool, Snippet

app = FastAPI(title="Open Source Sharing Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def serialize_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    out = {}
    for k, v in doc.items():
        if isinstance(v, ObjectId):
            out[k] = str(v)
        else:
            out[k] = v
    return out


@app.get("/")
def read_root():
    return {"message": "Open Source Sharing Platform API is running"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"

            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


# ---------------------------
# Schema Introspection
# ---------------------------
@app.get("/schema")
def get_schema():
    """Return JSON schema for key models so the viewer/clients can understand collections."""
    def schema_of(model: BaseModel.__class__):
        return model.model_json_schema()

    return {
        "dataset": schema_of(Dataset),
        "tool": schema_of(Tool),
        "snippet": schema_of(Snippet),
    }


# ---------------------------
# Datasets
# ---------------------------
@app.get("/api/datasets")
def list_datasets(tag: Optional[str] = None, q: Optional[str] = None, limit: int = 50):
    filt: Dict[str, Any] = {}
    if tag:
        filt["tags"] = tag
    if q:
        filt["$or"] = [
            {"name": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}},
        ]
    docs = get_documents("dataset", filt, limit)
    return [serialize_doc(d) for d in docs]


@app.post("/api/datasets", status_code=201)
def create_dataset(payload: Dataset):
    try:
        inserted_id = create_document("dataset", payload)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------------------------
# Tools
# ---------------------------
@app.get("/api/tools")
def list_tools(tag: Optional[str] = None, q: Optional[str] = None, limit: int = 50):
    filt: Dict[str, Any] = {}
    if tag:
        filt["tags"] = tag
    if q:
        filt["$or"] = [
            {"name": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}},
        ]
    docs = get_documents("tool", filt, limit)
    return [serialize_doc(d) for d in docs]


@app.post("/api/tools", status_code=201)
def create_tool(payload: Tool):
    try:
        inserted_id = create_document("tool", payload)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------------------------
# Snippets
# ---------------------------
@app.get("/api/snippets")
def list_snippets(tag: Optional[str] = None, q: Optional[str] = None, language: Optional[str] = None, limit: int = 50):
    filt: Dict[str, Any] = {}
    if tag:
        filt["tags"] = tag
    if language:
        filt["language"] = language
    if q:
        filt["$or"] = [
            {"title": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}},
            {"code": {"$regex": q, "$options": "i"}},
        ]
    docs = get_documents("snippet", filt, limit)
    return [serialize_doc(d) for d in docs]


@app.post("/api/snippets", status_code=201)
def create_snippet(payload: Snippet):
    try:
        inserted_id = create_document("snippet", payload)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
