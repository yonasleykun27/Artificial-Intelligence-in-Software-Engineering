#!/usr/bin/env python3
"""
Refactored SQLAlchemy ORM Database Module
Module: AI: SQL to ORM Refactoring and Security Analysis

This module refactors procedural raw SQL operations into an enterprise-grade,
object-oriented architecture using the SQLAlchemy Object-Relational Mapper (ORM).

Key Advantages:
- Declarative User model mapping Python attributes directly to table columns.
- Immune to SQL Injection through compiled Abstract Syntax Tree (AST) parameterization.
- Robust unit of work and transaction management via Scoped Session and Context Managers.
- Database engine portability (switchable between SQLite, MySQL, PostgreSQL via URI).
"""

from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime
)
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from contextlib import contextmanager

# 1. Base Class for Declarative Models
Base = declarative_base()


# 2. Declarative User Model Definition
class User(Base):
    """
    User Declarative Model.
    
    Maps Python object attributes to database columns in the 'users' table.
    Enforces data types, constraints (e.g., unique, nullable, index),
    and automatic lifecycle timestamps.
    """
    __tablename__ = 'users'

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        doc="Primary unique identifier for the user"
    )
    username = Column(
        String(50),
        nullable=False,
        unique=True,
        index=True,
        doc="Unique username handle"
    )
    email = Column(
        String(100),
        nullable=False,
        unique=True,
        doc="Unique email address"
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        doc="Timestamp when record was created"
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        doc="Timestamp when record was last updated"
    )

    def __repr__(self):
        return (
            f"<User(id={self.id}, username='{self.username}', "
            f"email='{self.email}', created_at='{self.created_at}')>"
        )


# 3. Database Engine & Session Management
class DatabaseManager:
    """Manages the SQLAlchemy Engine lifecycle and Session factory."""

    def __init__(self, connection_string="sqlite:///orm_users.db", echo=False):
        """
        Initialize database engine and session factory.
        
        Supports flexible connection URIs:
        - SQLite (Local/Testing): sqlite:///orm_users.db
        - MySQL (Production): mysql+mysqlconnector://root:pass@localhost/example_db
        - PostgreSQL: postgresql+psycopg2://user:pass@localhost/dbname
        """
        self.engine = create_engine(
            connection_string,
            echo=echo,
            pool_pre_ping=True
        )
        self.SessionFactory = sessionmaker(
            bind=self.engine,
            expire_on_commit=False
        )
        self.ScopedSession = scoped_session(self.SessionFactory)

    def init_db(self):
        """Create all registered database tables defined on Base metadata."""
        Base.metadata.create_all(self.engine)
        print("[DATABASE] Schema synchronized: 'users' table created.")

    def drop_db(self):
        """Drop all tables (primarily for clean test fixture teardown)."""
        Base.metadata.drop_all(self.engine)
        print("[DATABASE] Schema dropped.")

    @contextmanager
    def session_scope(self):
        """
        Provide a transactional scope around a series of operations.
        Guarantees automatic commit on success and rollback on failure.
        """
        session = self.ScopedSession()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


# 4. ORM Service Layer (CRUD Operations)
class UserService:
    """Encapsulates business operations and query logic using SQLAlchemy ORM."""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def create_user(self, username: str, email: str) -> User:
        """
        Create and persist a new User entity.
        
        Demonstrates Object-Centric creation: instantiation of a standard
        Python class automatically tracked and translated into an INSERT statement.
        """
        if not username or not email:
            raise ValueError("Username and email are required fields.")

        with self.db.session_scope() as session:
            try:
                new_user = User(username=username.strip(), email=email.strip())
                session.add(new_user)
                session.flush()  # Populates new_user.id prior to commit
                session.refresh(new_user)
                print(f"[ORM CREATE] Successfully persisted {new_user}")
                return new_user
            except IntegrityError as e:
                print(f"[ORM ERROR] User with username '{username}' or email '{email}' already exists.")
                raise e

    def get_user_by_username(self, username: str) -> User:
        """
        Query for a user by their unique username.
        
        SQL Injection Safe: Compiles to parameterized query 'WHERE users.username = :param_1'.
        """
        with self.db.session_scope() as session:
            user = session.query(User).filter(User.username == username).first()
            if user:
                print(f"[ORM QUERY] Found user: {user}")
            else:
                print(f"[ORM QUERY] No record found for username '{username}'.")
            return user

    def update_user_email(self, username: str, new_email: str) -> bool:
        """Update an existing user's email address via object property mutation."""
        if not username or not new_email:
            raise ValueError("Username and new email are required.")

        with self.db.session_scope() as session:
            user = session.query(User).filter(User.username == username).first()
            if not user:
                print(f"[ORM UPDATE] User '{username}' does not exist.")
                return False
            old_email = user.email
            user.email = new_email.strip()  # Direct object property mutation
            print(f"[ORM UPDATE] Updated {username}'s email: '{old_email}' -> '{new_email}'")
            return True

    def delete_user(self, username: str) -> bool:
        """Remove a user record from the database."""
        with self.db.session_scope() as session:
            user = session.query(User).filter(User.username == username).first()
            if not user:
                print(f"[ORM DELETE] Cannot delete; user '{username}' not found.")
                return False
            session.delete(user)
            print(f"[ORM DELETE] User '{username}' deleted successfully.")
            return True

    def list_users(self) -> list:
        """Retrieve all users ordered by ID."""
        with self.db.session_scope() as session:
            users = session.query(User).order_by(User.id.asc()).all()
            print(f"\n--- Registered Users Directory ({len(users)} total) ---")
            for u in users:
                print(f"  • ID: {u.id:2d} | Username: {u.username:<15} | Email: {u.email}")
            return users


# 5. Interactive Execution Demonstration
if __name__ == "__main__":
    print("=" * 70)
    print("DEMO: SQLAlchemy ORM Refactored Database Execution")
    print("=" * 70)

    # Use in-memory SQLite for instantaneous, self-contained demonstration
    db = DatabaseManager("sqlite:///demo_orm_users.db")
    db.init_db()

    service = UserService(db)

    # 1. Create Users
    print("\n--- 1. Creating Users ---")
    u1 = service.create_user("yonas_dev", "yonas@example.com")
    u2 = service.create_user("alice_engineer", "alice@enterprise.org")
    u3 = service.create_user("bob_architect", "bob@cloud.io")

    # 2. Query User
    print("\n--- 2. Querying User by Username ---")
    service.get_user_by_username("yonas_dev")

    # 3. Update User Email
    print("\n--- 3. Updating User Email ---")
    service.update_user_email("yonas_dev", "yonas.leykun@frontier.edu")

    # 4. List All Users
    print("\n--- 4. Listing Users ---")
    service.list_users()

    # 5. Safe Query Execution (SQLi Resistance Demonstration)
    print("\n--- 5. Demonstrating SQL Injection Immunity ---")
    malicious_input = "' OR '1'='1"
    print(f"Simulating attack input: {malicious_input}")
    safe_result = service.get_user_by_username(malicious_input)
    print(f"Result: {safe_result} (Safely treated as literal string; attack defeated!)")

    # 6. Delete User
    print("\n--- 6. Deleting User ---")
    service.delete_user("bob_architect")
    service.list_users()

    print("\n" + "=" * 70)
    print("All SQLAlchemy ORM operations completed successfully.")
    print("=" * 70)
