import asyncio
import sys
import os
import logging

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.core.database import init_db
from app.services.scheduler_service import run_ingestion_cycle

logging.basicConfig(level=logging.INFO)

async def main():
    print("🚀 Triggering Manual Ingestion Cycle...")
    # Ensure DB is init
    init_db()
    
    # Run the service
    await run_ingestion_cycle()
    print("✅ Manual Ingestion Complete.")

if __name__ == "__main__":
    asyncio.run(main())
