from fastapi import FastAPI
from app.api.endpoints import listings
from app.db.database import engine
from app.models.models import Base
app = FastAPI()


# Define the lifespan handler
def lifespan(app: FastAPI):
    # Startup event
    async def startup():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    # Shutdown event (if needed)
    async def shutdown():
        # Code to run during shutdown (like closing resources) can go here
        pass
    yield

# Pass the lifespan handler to the FastAPI instance
app = FastAPI(lifespan=lifespan)

# Include the listings router
app.include_router(listings.router)