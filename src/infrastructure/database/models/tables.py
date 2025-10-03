from sqlalchemy import (
    String,
    DateTime,
    Table,
    func,
    Boolean,
    Integer,
    Column,
    ForeignKey,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import date

class Base(DeclarativeBase):
    pass

mission_cat = Table(
    "mission_cat",
    Base.metadata,
    Column("mission_id", Integer, ForeignKey("missions.id"), primary_key=True),
    Column("cat_id", Integer, ForeignKey("cats.id"), primary_key=True),
)

class Cat(Base):
    __tablename__ = "cats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    reset_token: Mapped[str] = mapped_column(String(255), nullable=True)
    years_of_experience: Mapped[int] = mapped_column(Integer, nullable=False)
    breed: Mapped[str] = mapped_column(String(50), nullable=False)
    salary: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[date] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False)
    cat_note = relationship("Notes", foreign_keys="[Notes.cat_id]", back_populates="note_cat")
    mission = relationship("Mission", secondary=mission_cat, back_populates="cat")

class Mission(Base):
    __tablename__ = "missions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[date] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    mission_target = relationship("Target", foreign_keys="[Target.mission_id]", back_populates="target_mission")
    cat = relationship("Cat", secondary=mission_cat, back_populates="mission")

class Target(Base):
    __tablename__ = "targets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    mission_id: Mapped[int] = mapped_column(ForeignKey("missions.id"), nullable=False)
    created_at: Mapped[date] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    target_mission = relationship("Mission", foreign_keys=[mission_id], back_populates="mission_target")
    target_notes = relationship("Notes", foreign_keys="[Notes.target_id]", back_populates="note_target")

class Notes(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(String(255), nullable=False)
    cat_id: Mapped[int] = mapped_column(ForeignKey("cats.id"), nullable=False)
    target_id: Mapped[int] = mapped_column(ForeignKey("targets.id"), nullable=True)
    created_at: Mapped[date] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    note_cat = relationship("Cat", foreign_keys=[cat_id], back_populates="cat_note")
    note_target = relationship("Target", foreign_keys=[target_id], back_populates="target_notes")

