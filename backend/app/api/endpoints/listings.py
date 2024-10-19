from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.models import CarListing, CarListingFilter, CarListingResponse
from typing import List, Optional

router = APIRouter()

# Fetch all car listings with optional filters
@router.get("/listings", response_model=List[CarListingResponse])
async def get_listings(
    brand: Optional[List[str]] = Query(None),  # Define brand parameter directly
    model: Optional[str] = None,
    year: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    order_by : Optional[str] = Query("id"),
    order_direction: Optional[str] = Query("asc"),
    db: AsyncSession = Depends(get_db)
):
    print(f"Brand filters: {brand}")
    query = select(CarListing)

    # Apply filters to the query dynamically
    if brand:
        query = query.where(CarListing.brand.in_(brand))
    if model:
        query = query.where(CarListing.model == model)
    if year:
        query = query.where(CarListing.year == year)
    if min_price:
        query = query.where(CarListing.price >= min_price)
    if max_price:
        query = query.where(CarListing.price <= max_price)

    if order_by:
        if order_direction == "desc":
            query = query.order_by(getattr(CarListing, order_by).desc())
        else:
            query = query.order_by(getattr(CarListing, order_by))
            
    result = await db.execute(query)
    listings = result.scalars().all()

    return listings