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
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import uuid
from datetime import date

class Base(DeclarativeBase):
    pass

mission_cats = Table(
    "mission_cats",
    Base.metadata,
    Column("mission_uuid", UUID(as_uuid=True), ForeignKey("missions.uuid"), primary_key=True),
    Column("cat_uuid", UUID(as_uuid=True), ForeignKey("cats.uuid"), primary_key=True),
)

targets_cats = Table(
    "targets_cats",
    Base.metadata,
    Column("target_uuid", UUID(as_uuid=True), ForeignKey("targets.uuid"), primary_key=True),
    Column("cat_uuid", UUID(as_uuid=True), ForeignKey("cats.uuid"), primary_key=True),
)

class Cat(Base):
    __tablename__ = "cats"

    uuid: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    reset_token: Mapped[str] = mapped_column(String(255), nullable=True)
    years_of_experience: Mapped[int] = mapped_column(Integer, nullable=False)
    breed: Mapped[str] = mapped_column(String(50), nullable=False)
    salary: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[date] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False)
    cat_note = relationship("Note", foreign_keys="[Note.cat_uuid]", back_populates="note_cat")
    mission = relationship("Mission", secondary=mission_cats, back_populates="cat")
    targets = relationship("Target", secondary=targets_cats, back_populates="cats")

class Mission(Base):
    __tablename__ = "missions"

    uuid: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    created_at: Mapped[date] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    completed_at: Mapped[date] = mapped_column(DateTime, nullable=True)
    mission_target = relationship("Target", foreign_keys="[Target.mission_uuid]", back_populates="target_mission", cascade="all, delete-orphan")
    cat = relationship("Cat", secondary=mission_cats, back_populates="mission")

class Target(Base):
    __tablename__ = "targets"

    uuid: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    mission_uuid: Mapped[UUID] = mapped_column(ForeignKey("missions.uuid"), nullable=False)
    created_at: Mapped[date] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    target_mission = relationship("Mission", foreign_keys=[mission_uuid], back_populates="mission_target")
    target_notes = relationship("Note", foreign_keys="[Note.target_uuid]", back_populates="note_target")
    cats = relationship("Cat", secondary=targets_cats, back_populates="targets")

class Note(Base):
    __tablename__ = "notes"

    uuid: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content: Mapped[str] = mapped_column(String(255), nullable=False)
    cat_uuid: Mapped[UUID] = mapped_column(ForeignKey("cats.uuid"), nullable=False)
    target_uuid: Mapped[UUID] = mapped_column(ForeignKey("targets.uuid"), nullable=True)
    created_at: Mapped[date] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    note_cat = relationship("Cat", foreign_keys=[cat_uuid], back_populates="cat_note")
    note_target = relationship("Target", foreign_keys=[target_uuid], back_populates="target_notes")

