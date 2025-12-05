import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    print("FATAL: DATABASE_URL environment variable is not set!")
    DATABASE_URL = "postgresql+psycopg2://user:password@localhost:5432/insightmate_db" 
print(f"DEBUG: Attempting to connect with URL: {DATABASE_URL}")

engine = create_engine(DATABASE_URL)

Base = declarative_base()

class Analysis(Base):
    __tablename__ = 'analysis'
    id = Column(Integer, primary_key=True)
    session_id = Column(String, unique=True, nullable=False)
    summary = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Analysis(session_id='{self.session_id}', created_at='{self.created_at}')>"

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_tables():
    Base.metadata.create_all(bind=engine)
    print("Database tables created or already exist.")

if __name__ == "__main__":
    create_db_tables()