from sqlmodel import SQLModel
from app.core.database import engine
# Import all models to ensure metadata is registered
from app.models.recall import Recall, RecallSource, RawRecall
from app.models.user import User, Watchlist

def main():
    print("Creating tables in database...")
    SQLModel.metadata.create_all(engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    main()
