"""
Database utility module for SmartDairy
Handles all database operations including auto-creation of database and tables
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Tuple, Optional

DB_PATH = "smartdairy.db"

def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database and create tables if they don't exist"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create customers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            price_per_ltr REAL NOT NULL,
            mobile_number TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Add mobile_number column if it doesn't exist (for existing databases)
    try:
        cursor.execute("ALTER TABLE customers ADD COLUMN mobile_number TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Create entries table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            entry_date DATE NOT NULL,
            quantity REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            UNIQUE(customer_id, entry_date)
        )
    """)
    
    conn.commit()
    conn.close()
    print(f"Database initialized: {DB_PATH}")

# Customer operations
def add_customer(name: str, price_per_ltr: float, mobile_number: str = None) -> bool:
    """Add a new customer"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO customers (name, price_per_ltr, mobile_number) VALUES (?, ?, ?)",
            (name, price_per_ltr, mobile_number)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def get_all_customers() -> List[dict]:
    """Get all customers"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers ORDER BY name")
    customers = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return customers

def get_customer_by_id(customer_id: int) -> Optional[dict]:
    """Get customer by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def update_customer(customer_id: int, name: str, price_per_ltr: float, mobile_number: str = None) -> bool:
    """Update customer details"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE customers SET name = ?, price_per_ltr = ?, mobile_number = ? WHERE id = ?",
            (name, price_per_ltr, mobile_number, customer_id)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def delete_customer(customer_id: int) -> bool:
    """Delete a customer"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
        conn.commit()
        conn.close()
        return True
    except:
        return False

# Entry operations
def add_entry(customer_id: int, entry_date: str, quantity: float) -> bool:
    """Add a new milk entry"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO entries (customer_id, entry_date, quantity) VALUES (?, ?, ?)",
            (customer_id, entry_date, quantity)
        )
        conn.commit()
        conn.close()
        return True
    except:
        return False

def get_entries(start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[dict]:
    """Get all entries with optional date filtering"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT e.*, c.name as customer_name, c.price_per_ltr 
        FROM entries e
        JOIN customers c ON e.customer_id = c.id
    """
    params = []
    
    if start_date and end_date:
        query += " WHERE e.entry_date BETWEEN ? AND ?"
        params = [start_date, end_date]
    elif start_date:
        query += " WHERE e.entry_date >= ?"
        params = [start_date]
    elif end_date:
        query += " WHERE e.entry_date <= ?"
        params = [end_date]
    
    query += " ORDER BY e.entry_date DESC, c.name"
    
    cursor.execute(query, params)
    entries = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return entries

def get_monthly_entries(year: int, month: int) -> List[dict]:
    """Get entries for a specific month"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT e.*, c.name as customer_name, c.price_per_ltr, c.mobile_number 
        FROM entries e
        JOIN customers c ON e.customer_id = c.id
        WHERE strftime('%Y', e.entry_date) = ? AND strftime('%m', e.entry_date) = ?
        ORDER BY e.entry_date, c.name
    """
    
    cursor.execute(query, (str(year), f"{month:02d}"))
    entries = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return entries

def get_customer_entries_for_forecast(customer_id: int, days: int = 30) -> List[Tuple[str, float]]:
    """Get recent entries for a customer for forecasting"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT entry_date, quantity 
        FROM entries 
        WHERE customer_id = ? 
        ORDER BY entry_date DESC 
        LIMIT ?
    """
    
    cursor.execute(query, (customer_id, days))
    results = [(row[0], row[1]) for row in cursor.fetchall()]
    conn.close()
    return results

# Initialize database on import
if not os.path.exists(DB_PATH):
    init_database()
else:
    # Ensure tables exist even if DB exists
    init_database()

