from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from forex_api.models import order_model  # Ensure models are imported for metadata to work
from sqlalchemy import inspect
from sqlalchemy import text

DATABASE_URL = os.getenv("DATABASE_URL")

# Create the async engine
engine = create_async_engine(DATABASE_URL, future=True, echo=True)

# Session maker for async sessions
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)

# Base class for models
Base = declarative_base()

async def init_db():
    """
    Initialize the database by creating all tables asynchronously and checking their existence.
    """
    # Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
        # Now we use run_sync to inspect the schema synchronously
    await check_tables()

async def check_tables():
    """
    Check if the necessary tables exist in the database.
    """
    async with engine.connect() as conn:
        # Use the `text()` function to convert the SQL string into a valid executable SQL object
        query = text("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'orders'")
        
        # Execute the query asynchronously
        result = await conn.execute(query)
        table_exists = result.scalar()
        if table_exists == 0:
            raise Exception("Required tables are missing.")
        print("Tables exist.")
