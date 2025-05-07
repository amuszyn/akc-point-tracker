from datetime import datetime
from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Float,
    Boolean,
)
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()


# Define a base class for declarative mapping
class Base(DeclarativeBase):
    pass


class Runs(db.Model):
    __bind_key__ = 'dogs'
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
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)

    dogs = db.relationship("Dogs", backref="runs", lazy=True)
    creator = db.relationship("User", backref="runs", lazy=True)


class Dogs(db.Model):
    __bind_key__ = 'dogs'
    __tablename__ = "dogs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    show_name: Mapped[str] = mapped_column(String(100), nullable=True, unique=True)
    points: Mapped[int] = mapped_column(Integer, nullable=True)
    owner: Mapped[str] = mapped_column(String(50), nullable=False)
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    
    creator = db.relationship("User", backref="dogs", lazy=True)


class Titles(db.Model):
    __bind_key__ = 'dogs'
    __tablename__ = "titles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    show_name: Mapped[str] = mapped_column(
        String(100), ForeignKey("dogs.show_name"), nullable=False
    )
    mach: Mapped[bool] = mapped_column(Boolean, nullable=True)
    agch: Mapped[bool] = mapped_column(Boolean, nullable=True)

    dogs = db.relationship("Dogs", backref="titles", lazy=True)


class Owner(db.Model):
    __bind_key__ = 'dogs'
    __tablename__ = "owners"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    deleted: Mapped[bool] = mapped_column(Boolean, nullable=True)


class User(UserMixin, db.Model):
    __bind_key__ = 'dogs'  # Using the same database as other tables
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    oauth_provider: Mapped[str] = mapped_column(String(20), nullable=True)  # 'google', 'github', etc.
    oauth_id: Mapped[str] = mapped_column(String(100), nullable=True)
    
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.set_password(password)
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Event(db.Model):
    __bind_key__ = 'dogs'
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    location_name: Mapped[str] = mapped_column(String(200), nullable=False)
    address: Mapped[str] = mapped_column(String(200), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(2), nullable=False)
    zipcode: Mapped[str] = mapped_column(String(10), nullable=False)
    club_name: Mapped[str] = mapped_column(String(200), nullable=False)
    website: Mapped[str] = mapped_column(String(500), nullable=True)
    entry_fee: Mapped[float] = mapped_column(Float, nullable=True)
    closing_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    judge_name: Mapped[str] = mapped_column(String(100), nullable=True)
    classes_offered: Mapped[str] = mapped_column(String(500), nullable=True)  # Stored as JSON string
    notes: Mapped[str] = mapped_column(String(1000), nullable=True)
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    creator = db.relationship("User", backref="events", lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'start_date': self.start_date.strftime('%Y-%m-%d'),
            'end_date': self.end_date.strftime('%Y-%m-%d'),
            'location_name': self.location_name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zipcode': self.zipcode,
            'club_name': self.club_name,
            'website': self.website,
            'entry_fee': self.entry_fee,
            'closing_date': self.closing_date.strftime('%Y-%m-%d') if self.closing_date else None,
            'judge_name': self.judge_name,
            'classes_offered': self.classes_offered,
            'notes': self.notes
        }
