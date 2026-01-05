# Database management commands

# Initialize alembic (only needed once)
db-init:
    uv run alembic init alembic

# Create a new migration with autogenerate
db-migrate message="":
    uv run alembic revision --autogenerate -m "{{message}}"

# Apply all pending migrations
db-upgrade:
    uv run alembic upgrade head

# Rollback one migration
db-downgrade:
    uv run alembic downgrade -1
