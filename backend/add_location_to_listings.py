"""
Migration script to add location field to crop_listings table
Run this once to update existing database
"""

import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'instance', 'smart_farming.db')

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if column already exists
    cursor.execute("PRAGMA table_info(crop_listings)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'location' not in columns:
        # Add location column
        cursor.execute("ALTER TABLE crop_listings ADD COLUMN location VARCHAR(255)")
        conn.commit()
        print("✓ Successfully added 'location' column to crop_listings table")
    else:
        print("✓ 'location' column already exists in crop_listings table")
    
    conn.close()
    print("✓ Migration completed successfully")
    
except Exception as e:
    print(f"✗ Migration failed: {str(e)}")
