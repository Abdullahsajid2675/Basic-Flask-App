#!/usr/bin/env python3
"""
Database initialization script for Flask Security Demo
This script creates all database tables and optionally creates a demo user
"""

from app import app, db, User
import sys

def init_database():
    """Initialize the database with all tables"""
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Check if we should create a demo user
            if len(sys.argv) > 1 and sys.argv[1] == '--demo-user':
                create_demo_user()
                
        except Exception as e:
            print(f"❌ Error creating database: {e}")
            return False
    
    return True

def create_demo_user():
    """Create a demo user for testing"""
    try:
        # Check if demo user already exists
        existing_user = User.query.filter_by(username='demo').first()
        if existing_user:
            print("ℹ️  Demo user already exists")
            return
        
        # Create demo user with secure password
        demo_user = User(
            username='demo',
            email='demo@example.com'
        )
        demo_user.set_password('SecurePass123!')
        
        db.session.add(demo_user)
        db.session.commit()
        
        print("✅ Demo user created successfully!")
        print("   Username: demo")
        print("   Password: SecurePass123!")
        
    except Exception as e:
        print(f"❌ Error creating demo user: {e}")
        db.session.rollback()

if __name__ == '__main__':
    print("🔧 Initializing Flask Security Demo Database...")
    if init_database():
        print("🎉 Database initialization completed!")
    else:
        print("💥 Database initialization failed!")
        sys.exit(1)