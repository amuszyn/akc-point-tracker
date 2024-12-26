from datetime import datetime
from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Float,
    Boolean,
)
from sqlalchemy.orm import DeclarativeBase, backref, mapped_column, Mapped
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Define a base class for declarative mapping
class Base(DeclarativeBase):
    pass


class Runs(Base):
    __tablename__ = "runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    pet_id: Mapped[int] = mapped_column(Integer, nullable=False)
    show_name: Mapped[str] = mapped_column(
        String(100), ForeignKey("dogs.show_name"), nullable=False
    )
    run_time: Mapped[float] = mapped_column(Float, nullable=False)
    course_time: Mapped[float] = mapped_column(Float, nullable=False)
    qualification: Mapped[bool] = mapped_column(Boolean, nullable=False)
    points: Mapped[int] = mapped_column(Integer, nullable=False)
    handler: Mapped[str] = mapped_column(String(50))
    trial: Mapped[str] = mapped_column(String(100), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    height: Mapped[str] = mapped_column(String(8), nullable=False)
    place: Mapped[str] = mapped_column(String(20), nullable=False)
    judge: Mapped[str] = mapped_column(String(50), nullable=False)
    run_class: Mapped[str] = mapped_column(String(10), nullable=False)
    deleted: Mapped[bool] = mapped_column(Boolean, nullable=True)

    db.relationship("dogs", backref=backref("show_name"), lazy=True)


db.Table("runs", Runs.metadata)


class Dogs(Base):
    __tablename__ = "dogs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    show_name: Mapped[str] = mapped_column(String(100), nullable=True)
    points: Mapped[int] = mapped_column(Integer, nullable=True)
    owner: Mapped[str] = mapped_column(String(50), nullable=False)


db.Table("dogs", Dogs.metadata)


class Titles(Base):
    __tablename__ = "titles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    show_name: Mapped[str] = mapped_column(
        String(100), ForeignKey("dogs.show_name"), nullable=False
    )
    mach: Mapped[bool] = mapped_column(Boolean, nullable=True)
    agch: Mapped[bool] = mapped_column(Boolean, nullable=True)

    db.relationship("dogs", backref=backref("show_name"), lazy=True)


class Owner(Base):
    __tablename__ = "owners"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    deleted: Mapped[bool] = mapped_column(Boolean, nullable=True)
