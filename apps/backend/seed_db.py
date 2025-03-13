#!/usr/bin/env python
"""
Seed script for the Capstone database.
This script populates the database with sample data for development and testing.
"""

import sys
from pathlib import Path

# Add the parent directory (apps) to Python path
root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))

from backend.src.seed import seed_database

if __name__ == "__main__":
    print("Seeding the database with sample data...")
    seed_database()
    print("Database seeding completed successfully!")
