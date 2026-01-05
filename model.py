from datetime import datetime

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

import functools
mapped_column = functools.partial(mapped_column)
relationship = functools.partial(relationship, lazy="selectin")

engine = create_async_engine("sqlite+aiosqlite:///db.sqlite")
async_session = async_sessionmaker(engine, expire_on_commit=False)


# Base class for declarative models.
# Using AsyncAttrs allows awaitable access to lazy-loaded attributes.
class Base(AsyncAttrs, DeclarativeBase):
    pass


class DefaultModelMixin:
    """A mixin that adds id, created_at, and updated_at columns to a model."""

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), server_onupdate=func.now()
    )


class Test(Base, DefaultModelMixin):
    """A test model inheriting common fields from DefaultModelMixin."""

    __tablename__ = "tests"

    val: Mapped[str] = mapped_column(String(1_000_000))


class User(Base, DefaultModelMixin):
    """A user of the system."""

    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(255))
    repos: Mapped[list["Repo"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"


class Repo(Base, DefaultModelMixin):
    """A repository owned by a user."""

    __tablename__ = "repos"

    name: Mapped[str] = mapped_column(String(255))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship(back_populates="repos")

    def __repr__(self) -> str:
        return f"Repo(id={self.id!r}, name={self.name!r})"
