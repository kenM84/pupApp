#!/usr/bin/env python3
"""
Database initialization script for RUSH PUP! application.
Run this script to create the database tables and optionally create an admin user.
"""

from services.auth_service import AuthService


def init_database():
    """Initialize the database and create tables"""
    try:
        # Initialize auth service which will create tables
        auth_service = AuthService()
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Initializing RUSH PUP! Database...")

    if not init_database():
        raise Exception("Database initialization failed")

    print("\n✨ Database initialization complete!")n