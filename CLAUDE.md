# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a full-stack Python/React project template with:
- **Backend**: FastAPI with SQLAlchemy (async) and SQLite
- **Frontend**: React 18 with Vite and React Router
- **Database migrations**: Alembic
- **Process management**: Overmind (runs multiple services from Procfiles)
- **Containerization**: Docker with Traefik for routing

## Commands

### Development (via Docker)
```bash
docker compose up abrarenameme_dev    # Starts all services via Procfile.dev
```

### Running services individually (inside container or locally with uv)
```bash
# Frontend dev server (port 80)
cd frontend && npm install && npm run dev -- --host 0.0.0.0 --port 80

# Backend API (port 8000 in dev, port 80 in prod)
uv run uvicorn api:app --host 0.0.0.0 --port 8000 --reload

# Jupyter Lab (port 8080)
uv run jupyter lab --no-browser --allow-root --ip=0.0.0.0 --port=8080
```

### Frontend
```bash
cd frontend && npm run dev      # Development
cd frontend && npm run build    # Production build
```

### Database migrations (Alembic)
```bash
alembic revision --autogenerate -m "description"  # Create migration
alembic upgrade head                               # Apply migrations
alembic downgrade -1                               # Rollback one migration
```

### Dependencies
```bash
uv sync           # Install Python dependencies
uv add <package>  # Add a new dependency
```

## Architecture

### Backend (`api.py`, `model.py`)
- `api.py`: FastAPI app that serves API routes under `/api/*` and the React SPA for all other routes
- `model.py`: SQLAlchemy async models with a common `DefaultModelMixin` (id, created_at, updated_at)
- Database: SQLite at `db.sqlite` (async via aiosqlite)
- All relationships use `lazy="selectin"` by default for async compatibility

### Frontend (`frontend/`)
- Vite + React 18 with React Router for client-side routing
- Built assets served from `frontend/dist/` by FastAPI in production
- Development: Vite dev server runs separately (Procfile.dev)

### Procfiles
- `Procfile.dev`: Runs frontend dev server, API with hot reload, and Jupyter Lab
- `Procfile.prod`: Builds frontend then runs API serving static files
