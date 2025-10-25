#!/usr/bin/env python3
"""
Script to load the test users fixture and demonstrate usage.
Run this script to load the test users into your database.
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append('/Users/essayeghothmane/django-training/day03-final/d09')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'd09.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User

def load_fixture():
    """Load the test users fixture."""
    try:
        call_command('loaddata', 'fixtures/test_users.json')
        print("✅ Successfully loaded test users fixture!")
        
        # Verify the users were created
        users = User.objects.all()
        print(f"📊 Total users in database: {users.count()}")
        
        for user in users:
            print(f"👤 User: {user.username} ({user.first_name} {user.last_name}) - {user.email}")
            
    except Exception as e:
        print(f"❌ Error loading fixture: {e}")

if __name__ == "__main__":
    load_fixture()
