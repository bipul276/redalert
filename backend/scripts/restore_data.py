import asyncio
import sys
import os
import logging

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.services.scheduler_service import run_ingestion_cycle
from app.core.database import init_db

# Configure Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    print("🚀 Starting Manual Data Restoration...")
    
    # Ensure tables exist (just in case)
    init_db()
    
    # Run the cycle
    await run_ingestion_cycle()
    
    print("✅ Restoration Complete! Check the dashboard.")

if __name__ == "__main__":
    asyncio.run(main())
