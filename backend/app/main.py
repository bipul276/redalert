from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_recalls import router as recalls_router
from app.api.routes_watchlists import router as watchlists_router
from app.api.routes_admin import router as admin_router
from app.core.config import settings
from app.core.database import init_db
from app.models.user import User, Watchlist # Import to register with SQLModel metadata used in init_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Product Recall Alert Hub Backend",
    version="0.1.0"
)

# CORS Configuration
origins = [
    "http://localhost:3000",  # Next.js Frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recalls_router, prefix="/api/v1/recalls", tags=["recalls"])
app.include_router(watchlists_router, prefix="/api/v1/watchlists", tags=["watchlists"])
app.include_router(admin_router, prefix="/api/v1/admin", tags=["admin"])
# Push Notifications
from app.api.routes_push import router as push_router
app.include_router(push_router, prefix="/api/v1/notifications", tags=["notifications"])

@app.on_event("startup")
def on_startup():
    init_db()
    
    # Start Scheduler
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from app.services.scheduler_service import run_ingestion_cycle
    
    scheduler = AsyncIOScheduler()
    # Run every 12 hours
    scheduler.add_job(run_ingestion_cycle, "interval", hours=12)
    scheduler.start()
    print("🕒 Scheduler started: Ingestion pipeline runs every 12 hours.")

@app.get("/")
def health_check():
    return {"status": "ok", "service": "RedAlert Backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
