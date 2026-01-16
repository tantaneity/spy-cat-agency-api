from sqlalchemy import Integer, String, Float, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base
from typing import Optional, List

class SpyCat(Base):
    __tablename__ = "spy_cats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    years_of_experience: Mapped[int] = mapped_column(Integer, nullable=False)
    breed: Mapped[str] = mapped_column(String, nullable=False)
    salary: Mapped[float] = mapped_column(Float, nullable=False)

    mission: Mapped[Optional["Mission"]] = relationship("Mission", back_populates="cat", uselist=False)

class Mission(Base):
    __tablename__ = "missions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cat_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("spy_cats.id"), nullable=True)
    is_complete: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    cat: Mapped[Optional["SpyCat"]] = relationship("SpyCat", back_populates="mission")
    targets: Mapped[List["Target"]] = relationship("Target", back_populates="mission", cascade="all, delete-orphan")

class Target(Base):
    __tablename__ = "targets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    mission_id: Mapped[int] = mapped_column(Integer, ForeignKey("missions.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)
    notes: Mapped[str] = mapped_column(Text, default="")
    is_complete: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    mission: Mapped["Mission"] = relationship("Mission", back_populates="targets")
