import sys
import time
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base

from config import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT


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

    def get_connection_string(self) -> str:
        """Build the database connection string."""
        return f"postgresql://{quote_plus(self.user)}:{quote_plus(self.password)}@{self.host}:{self.port}/{self.db_name}"

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
        """Create and return a new database session."""
        if not self.session_factory:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self.session_factory()


# Initialize the database manager
db_manager = DatabaseManager(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

# Connect to the database
db_manager.connect()

# Access ORM classes
Patients = db_manager.base.classes.patients
ContactDetails = db_manager.base.classes.contact_details

