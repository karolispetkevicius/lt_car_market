from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# Add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict origins if necessary, e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers (e.g., Authorization)
)

# Include the listings router
app.include_router(listings.router)