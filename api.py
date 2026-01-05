from pathlib import Path

from fastapi import FastAPI, Response, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/hello")
async def hello():
    """Dummy API endpoint."""
    return {"message": "Hello from FastAPI!"}


# Static assets (served after API routes)
frontend_dist = Path(__file__).resolve().parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/assets", StaticFiles(directory=frontend_dist / "assets"), name="assets")


@app.get("/{full_path:path}")
async def serve_spa(full_path: str) -> Response:
    """Serve index.html for all non-API routes (React Router handles routing)."""
    index_path = frontend_dist / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Frontend not built")
