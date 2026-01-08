from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import init_db, engine, Base
from .routers import auth, users, ai_tools, credits
import logging
from asyncio import to_thread

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def lifespan(app: FastAPI):
    logger.info("Starting up application...")
    try:
        await to_thread(Base.metadata.create_all, bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
    yield

app = FastAPI(
    title="AI-Pass API",
    description="Unified AI workspace and membership platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(ai_tools.router)
app.include_router(credits.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to AI-Pass API",
        "status": "online",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}