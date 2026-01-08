from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import init_db
from .routers import auth, users, ai_tools, credits

async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="AI-Pass API",
    description="Unified AI workspace and membership platform",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(ai_tools.router)
app.include_router(credits.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to AI-Pass API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}