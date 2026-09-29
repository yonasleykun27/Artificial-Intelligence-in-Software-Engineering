#!/usr/bin/env python3
"""
Initial Procedural Database Script (Raw SQL / MySQL Connector)
Module: AI: SQL to ORM Refactoring and Security Analysis

This script demonstrates procedural database interaction using mysql-connector-python.
It showcases standard CRUD operations, connection management, and highlights the
vulnerabilities and maintainability bottlenecks associated with manual SQL string management.
"""

import mysql.connector
from mysql.connector import Error


def get_connection():
    """Establish and return a database connection."""
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="yourpassword",
            database="example_db"
        )
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None


def create_user(db_cursor, username, email):
    """Create a new user safely using parameterized queries."""
    if not username or not email:
        print("Username and email are required.")
        return
    sql = "INSERT INTO users (username, email) VALUES (%s, %s)"
    try:
        db_cursor.execute(sql, (username, email))
        print(f"User '{username}' created successfully.")
    except Error as e:
        print(f"Error creating user: {e}")


def get_user_by_username(db_cursor, username):
    """Retrieve a single user record by username."""
    if not username:
        print("Username is required.")
        return None
    sql = "SELECT id, username, email, created_at FROM users WHERE username = %s"
    try:
        db_cursor.execute(sql, (username,))
        user = db_cursor.fetchone()
        if user:
            print(f"Found user: ID={user[0]}, Username={user[1]}, Email={user[2]}")
            return user
        print(f"User '{username}' not found.")
        return None
    except Error as e:
        print(f"Error fetching user: {e}")
        return None


def update_user_email(db_cursor, username, new_email):
    """Update an existing user's email address."""
    if not username or not new_email:
        print("Username and new email are required.")
        return
    sql = "UPDATE users SET email = %s WHERE username = %s"
    try:
        db_cursor.execute(sql, (new_email, username))
        if db_cursor.rowcount > 0:
            print(f"Updated email for user '{username}' to '{new_email}'.")
        else:
            print(f"No user found with username '{username}'.")
    except Error as e:
        print(f"Error updating user email: {e}")


def delete_user(db_cursor, username):
    """Delete a user record by username."""
    if not username:
        print("Username is required.")
        return
    sql = "DELETE FROM users WHERE username = %s"
    try:
        db_cursor.execute(sql, (username,))
        if db_cursor.rowcount > 0:
            print(f"User '{username}' deleted successfully.")
        else:
            print(f"No user found with username '{username}'.")
    except Error as e:
        print(f"Error deleting user: {e}")


def list_users(db_cursor):
    """List all registered users."""
    sql = "SELECT id, username, email, created_at FROM users ORDER BY id ASC"
    try:
        db_cursor.execute(sql)
        users = db_cursor.fetchall()
        print(f"\n--- User Directory ({len(users)} users) ---")
        for u in users:
            print(f"[{u[0]}] {u[1]} <{u[2]}> (Created: {u[3]})")
        return users
    except Error as e:
        print(f"Error listing users: {e}")
        return []


# ==============================================================================
# SECURITY VULNERABILITY DEMONSTRATION (RAW SQL STRING FORMATTING)
# ==============================================================================
def insecure_search_user(db_cursor, user_input):
    """
    WARNING: Highly insecure function demonstrating SQL Injection (SQLi).
    When developers format raw SQL strings directly with user-supplied input,
    attackers can manipulate query syntax, bypass authentication, or drop tables.
    
    Example Attack Input:
        user_input = "' OR '1'='1"  --> Dumps all users
        user_input = "'; DROP TABLE users; --" --> Destroys table
    """
    # BAD PRACTICE: String concatenation / f-string formatting into SQL
    vulnerable_sql = f"SELECT * FROM users WHERE username = '{user_input}'"
    print(f"\n[INSECURE QUERY EXECUTED]: {vulnerable_sql}")
    try:
        db_cursor.execute(vulnerable_sql)
        return db_cursor.fetchall()
    except Error as e:
        print(f"Database error during insecure query: {e}")
        return []


if __name__ == "__main__":
    print("Initial procedural script loaded. Connect to MySQL to run live queries.")
