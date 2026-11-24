from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from ..database import get_db
from .. import models, schemas

router = APIRouter()

# 1. Create a destination
@router.post("/destinations", response_model=schemas.DestinationOut, status_code=status.HTTP_201_CREATED, tags=["Destinations"])
def create_destination(payload: schemas.DestinationCreate, db: Session = Depends(get_db)):
    item = models.Destination(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# 2. List destinations
@router.get("/destinations", response_model=list[schemas.DestinationOut], tags=["Destinations"])
def list_destinations(db: Session = Depends(get_db)):
    return db.scalars(select(models.Destination).order_by(models.Destination.city)).all()

# 3. Create a user
@router.post("/users", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.scalar(select(models.User).where(models.User.email == payload.email))
    if existing:
        raise HTTPException(status_code=409, detail="A user with this email already exists")
    item = models.User(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# 4. Create a trip
@router.post("/trips", response_model=schemas.TripOut, status_code=status.HTTP_201_CREATED, tags=["Trips"])
def create_trip(payload: schemas.TripCreate, db: Session = Depends(get_db)):
    if not db.get(models.User, payload.user_id):
        raise HTTPException(status_code=404, detail="User not found")
    if not db.get(models.Destination, payload.destination_id):
        raise HTTPException(status_code=404, detail="Destination not found")
    item = models.Trip(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# 5. List trips
@router.get("/trips", response_model=list[schemas.TripOut], tags=["Trips"])
def list_trips(db: Session = Depends(get_db)):
    return db.scalars(select(models.Trip).order_by(models.Trip.start_date)).all()

# 6. Get one trip
@router.get("/trips/{trip_id}", response_model=schemas.TripOut, tags=["Trips"])
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    item = db.get(models.Trip, trip_id)
    if not item:
        raise HTTPException(status_code=404, detail="Trip not found")
    return item

# 7. Update a trip
@router.put("/trips/{trip_id}", response_model=schemas.TripOut, tags=["Trips"])
def update_trip(trip_id: int, payload: schemas.TripUpdate, db: Session = Depends(get_db)):
    item = db.get(models.Trip, trip_id)
    if not item:
        raise HTTPException(status_code=404, detail="Trip not found")
    changes = payload.model_dump(exclude_unset=True)
    start = changes.get("start_date", item.start_date)
    end = changes.get("end_date", item.end_date)
    if end < start:
        raise HTTPException(status_code=422, detail="end_date must be on or after start_date")
    for key, value in changes.items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

# 8. Delete a trip
@router.delete("/trips/{trip_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Trips"])
def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    item = db.get(models.Trip, trip_id)
    if not item:
        raise HTTPException(status_code=404, detail="Trip not found")
    db.delete(item)
    db.commit()
    return None

# 9. Add a day to a trip
@router.post("/trip-days", response_model=schemas.TripDayOut, status_code=status.HTTP_201_CREATED, tags=["Itinerary"])
def create_trip_day(payload: schemas.TripDayCreate, db: Session = Depends(get_db)):
    trip = db.get(models.Trip, payload.trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    if not (trip.start_date <= payload.day_date <= trip.end_date):
        raise HTTPException(status_code=422, detail="Day must fall within the trip date range")
    item = models.TripDay(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# 10. Add an activity
@router.post("/activities", response_model=schemas.ActivityOut, status_code=status.HTTP_201_CREATED, tags=["Itinerary"])
def create_activity(payload: schemas.ActivityCreate, db: Session = Depends(get_db)):
    if not db.get(models.TripDay, payload.trip_day_id):
        raise HTTPException(status_code=404, detail="Trip day not found")
    item = models.Activity(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# Extra read endpoint: full itinerary
@router.get("/trips/{trip_id}/itinerary", response_model=schemas.ItineraryOut, tags=["Itinerary"])
def get_itinerary(trip_id: int, db: Session = Depends(get_db)):
    trip = db.scalar(
        select(models.Trip)
        .options(
            selectinload(models.Trip.destination),
            selectinload(models.Trip.days).selectinload(models.TripDay.activities),
        )
        .where(models.Trip.id == trip_id)
    )
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    days = sorted(trip.days, key=lambda day: day.day_date)
    for day in days:
        day.activities.sort(key=lambda activity: activity.start_time or "99:99")
    return {"trip": trip, "destination": trip.destination, "days": days}
