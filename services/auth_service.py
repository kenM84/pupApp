from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pupApp.models.user import User, Base
from pupApp.services.keyvault_service import KeyVaultService


class AuthService:
    def __init__(self):
        self.engine = None
        self.Session = None
        self._initialized = False

    def _ensure_initialized(self):
        """Ensure database is initialized, with lazy initialization"""
        if not self._initialized:
            self._initialize_database()

    def _initialize_database(self):
        from flask import current_app
        """Initialize database connection and create tables"""
        try:
            # Get database connection string from environment or use default
            keyvault_service = KeyVaultService()
            database_server = keyvault_service.get_secret("sqlDBServer")
            database_name = keyvault_service.get_secret("sqlDBName")
            database_username = keyvault_service.get_secret("appDBUname")
            database_password = keyvault_service.get_secret("AppDBPassword")

            print(f'''database credentials received: {database_server}, '''
                  f'''{database_username}, {database_password}''')

            # Construct Azure SQL connection string for pymssql
            # Format: mssql+pymssql://username:password@server:port/database
            database_url = (
                f"mssql+pymssql://{database_username}:{database_password}@"
                f"{database_server}:1433/{database_name}"
            )

            print(f"Using pymssql connection: {database_url}")

            self.engine = create_engine(
                database_url,
                pool_pre_ping=True,  # Verify connections before use
                pool_recycle=300,    # Recycle connections every 5 minutes
                echo=False           # Set to True for SQL debugging
            )
            self.Session = sessionmaker(bind=self.engine)

            # Create tables if they don't exist
            Base.metadata.create_all(self.engine)
            current_app.logger.info("Database initialized successfully")
            self._initialized = True
        except Exception as e:
            current_app.logger.error(f"Database initialization failed: {e}")
            raise

    def create_user(self, username, email, password):
        from flask import current_app
        """Create a new user"""
        self._ensure_initialized()
        session = self.Session()
        try:
            # Check if user already exists
            existing_user = session.query(User).filter(
                (User.username == username) | (User.email == email)
            ).first()

            if existing_user:
                return None, "Username or email already exists"

            # Create new user
            user = User(username=username, email=email, password=password)
            session.add(user)
            session.commit()

            return user, "User created successfully"
        except Exception as e:
            session.rollback()
            current_app.logger.error(f"Error creating user: {e}")
            return None, f"Error creating user: {e}"
        finally:
            session.close()

    def authenticate_user(self, username, password):
        """Authenticate user with username and password"""
        self._ensure_initialized()
        session = self.Session()
        try:
            user = session.query(User).filter(
                User.username == username).first()

            if user and user.check_password(password) and user.is_active:
                print(f"User authenticated: {user.username}")
                # Update last login
                user.last_login = datetime.utcnow()
                session.commit()

                # Force load all attributes before expunging to prevent
                # lazy loading issues
                _ = (user.id, user.username, user.email, user.is_active,
                     user.created_at, user.last_login)

                # Detach the user object from the session before returning
                session.expunge(user)
                return user, "Authentication successful"
            else:
                return None, "Invalid username or password"
        except Exception as e:
            from flask import current_app
            current_app.logger.error(f"Error authenticating user: {e}")
            return None, f"Authentication error: {e}"
        finally:
            session.close()

    def get_user_by_id(self, user_id):
        from flask import current_app
        """Get user by ID"""
        self._ensure_initialized()
        session = self.Session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                # Force load all attributes before expunging to prevent
                # lazy loading issues
                _ = (user.id, user.username, user.email, user.is_active,
                     user.created_at, user.last_login)

                # Detach the user object from the session before returning
                session.expunge(user)
            return user
        except Exception as e:
            current_app.logger.error(f"Error getting user by ID: {e}")
            return None
        finally:
            session.close()

    def get_user_by_username(self, username):
        from flask import current_app
        """Get user by username"""
        self._ensure_initialized()
        session = self.Session()
        try:
            user = session.query(User).filter(
                User.username == username).first()
            if user:
                # Force load all attributes before expunging to prevent
                # lazy loading issues
                _ = (user.id, user.username, user.email, user.is_active,
                     user.created_at, user.last_login)

                # Detach the user object from the session before returning
                session.expunge(user)
            return user
        except Exception as e:
            current_app.logger.error(f"Error getting user by username: {e}")
            return None
        finally:
            session.close()
