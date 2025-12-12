from common.db.postgres import PostgresClient
from common.config import settings

def get_study_db_client() -> PostgresClient:
    db_url = settings().DATABASE_URL
    return PostgresClient(database_url=db_url)