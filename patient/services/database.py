import sys
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base

from config import DATABASE_URL, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

import os
print("DB_USER:", os.getenv("DB_USER"))
print("DB_PASSWORD:", os.getenv("DB_PASSWORD"))
print("DB_HOST:", os.getenv("DB_HOST"))
print("DB_PORT:", os.getenv("DB_PORT"))
print("DB_NAME:", os.getenv("DB_NAME"))


class DatabaseManager:
    def __init__(self, user, password, host, port, db_name):
        """Initialize the database manager with connection parameters."""
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db_name = db_name
        self.base = automap_base()
        self.engine = None
        self.session_factory = None

    @staticmethod
    def get_connection_string() -> str:
        """Build the database connection string."""
        return DATABASE_URL

    def connect(self, max_attempts=3, retry_delay=30) -> None:
        """Establish a connection to the database."""
        connection_string = self.get_connection_string()

        self.engine = create_engine(
            connection_string,
            pool_size=50,
            max_overflow=30,
            pool_timeout=30,
            pool_recycle=3600,
        )

        attempts = 0
        while attempts < max_attempts:
            try:
                self.base.prepare(autoload_with=self.engine)
                print("Successfully connected to the database.")
                self.session_factory = sessionmaker(
                    autocommit=False, autoflush=False, bind=self.engine
                )
                break
            except Exception as e:
                attempts += 1
                if attempts < max_attempts:
                    print(
                        f"Attempt {attempts} failed: {str(e)}. Retrying in {retry_delay} seconds..."
                    )
                    time.sleep(retry_delay)
                else:
                    print("Failed to connect to the database. Exiting.")
                    sys.exit(1)

    def get_session(self):
        """Ensure database is connected and return a session."""
        if not self.session_factory:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self.session_factory()

    def get_database_session(self):
        """Yield a database session for FastAPI's dependency injection."""
        session = self.get_session()
        try:
            yield session
        finally:
            session.close()  # Ensure proper cleanup

    def get_class(self, class_name):
        """Get the class object for defined tables"""
        return getattr(self.base.classes, class_name, None)


# Initialize the database manager
print(DATABASE_URL)
db_manager = DatabaseManager(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
