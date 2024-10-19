from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional, List
from fastapi import Query

Base = declarative_base()


class CarListing(Base):
    '''
    SQLAlchemy model for database representation.
    Defines how data is stored in PostgreSQL database.
    '''
    __tablename__ = "car_listings"
    
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=True)
    year = Column(Integer, nullable=True)
    fuel_type = Column(String, nullable=True)
    mileage = Column(Integer, nullable=True)
    gearbox = Column(String, nullable=True)
    url = Column(String, unique=True, nullable=False)


class CarListingResponse(BaseModel):
    '''
    Pydantic model for response (data sent to the user).
    Serializes the data from database into a JSON response
    '''
    id: int
    brand: str
    model: str
    title: str
    price: Optional[float] = None
    year: Optional[int] = None  
    fuel_type: Optional[str] = None
    mileage: Optional[int] = None
    gearbox: Optional[str] = None
    url: str

    class Config:
        from_attributes = True  # Use this for Pydantic v2


class CarListingFilter(BaseModel):
    '''
    Filter model to validate the filtering paramaters that users send in their requests.
    '''
    brand: Optional[List[str]] = None
    model: Optional[str] = None
    year: Optional[int] = None
    min_price: Optional[float] = None  # Changed to float for consistency
    max_price: Optional[float] = None
