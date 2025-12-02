import asyncio
from common.db.postgres import engine
from common.db.models import Base
from sqlalchemy import text # Ensure text is imported

async def create_tables():
    # Attempt connection and table creation
    try:
        async with engine.begin() as conn:
            # First, check connection sanity
            await conn.execute(text("SELECT 1")) 
            # Now, create all tables based on Base.metadata
            await conn.run_sync(Base.metadata.create_all)
        print('Database schema created successfully!')
    except Exception as e:
        print(f"Error creating tables: {e}")

if __name__ == "__main__":
    asyncio.run(create_tables())

