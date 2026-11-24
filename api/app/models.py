from datetime import date, datetime
from sqlalchemy import String, Integer, Date, DateTime, ForeignKey, Text, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    trips: Mapped[list["Trip"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class Destination(Base):
    __tablename__ = "destinations"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    trips: Mapped[list["Trip"]] = relationship(back_populates="destination")

class Trip(Base):
    __tablename__ = "trips"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    budget: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    destination_id: Mapped[int] = mapped_column(ForeignKey("destinations.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="trips")
    destination: Mapped["Destination"] = relationship(back_populates="trips")
    days: Mapped[list["TripDay"]] = relationship(back_populates="trip", cascade="all, delete-orphan")

class TripDay(Base):
    __tablename__ = "trip_days"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    day_date: Mapped[date] = mapped_column(Date, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    trip: Mapped["Trip"] = relationship(back_populates="days")
    activities: Mapped[list["Activity"]] = relationship(back_populates="trip_day", cascade="all, delete-orphan")

class Activity(Base):
    __tablename__ = "activities"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    trip_day_id: Mapped[int] = mapped_column(ForeignKey("trip_days.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    start_time: Mapped[str | None] = mapped_column(String(5), nullable=True)
    estimated_cost: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
    trip_day: Mapped["TripDay"] = relationship(back_populates="activities")
