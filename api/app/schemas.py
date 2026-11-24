from datetime import date
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class DestinationCreate(BaseModel):
    city: str = Field(min_length=1, max_length=100)
    country: str = Field(min_length=1, max_length=100)
    description: str | None = None

class DestinationOut(ORMModel):
    id: int
    city: str
    country: str
    description: str | None

class UserCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=120)
    email: EmailStr

class UserOut(ORMModel):
    id: int
    full_name: str
    email: EmailStr

class TripCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    start_date: date
    end_date: date
    budget: Decimal | None = Field(default=None, ge=0)
    user_id: int
    destination_id: int

    @model_validator(mode="after")
    def check_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")
        return self

class TripUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    start_date: date | None = None
    end_date: date | None = None
    budget: Decimal | None = Field(default=None, ge=0)

class TripOut(ORMModel):
    id: int
    title: str
    start_date: date
    end_date: date
    budget: Decimal | None
    user_id: int
    destination_id: int

class TripDayCreate(BaseModel):
    trip_id: int
    day_date: date
    notes: str | None = None

class TripDayOut(ORMModel):
    id: int
    trip_id: int
    day_date: date
    notes: str | None

class ActivityCreate(BaseModel):
    trip_day_id: int
    name: str = Field(min_length=1, max_length=150)
    start_time: str | None = Field(default=None, pattern=r"^([01]\d|2[0-3]):[0-5]\d$")
    estimated_cost: Decimal | None = Field(default=None, ge=0)
    details: str | None = None

class ActivityOut(ORMModel):
    id: int
    trip_day_id: int
    name: str
    start_time: str | None
    estimated_cost: Decimal | None
    details: str | None

class ItineraryActivity(ORMModel):
    id: int
    name: str
    start_time: str | None
    estimated_cost: Decimal | None
    details: str | None

class ItineraryDay(ORMModel):
    id: int
    day_date: date
    notes: str | None
    activities: list[ItineraryActivity]

class ItineraryOut(BaseModel):
    trip: TripOut
    destination: DestinationOut
    days: list[ItineraryDay]
