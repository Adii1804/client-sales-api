#!/usr/bin/env python3
"""Test database connection to local MySQL server"""

import sys

print("Testing MySQL connection...")
print("=" * 60)

try:
    import pymysql
    print("✅ pymysql module imported")
except ImportError:
    print("❌ pymysql not installed. Run: pip install pymysql")
    sys.exit(1)

# Connection parameters (from Azure App Service config)
DB_CONFIG = {
    'host': '192.168.151.36',
    'port': 59041,
    'user': 'crm_user',
    'password': 'Vrl@55555',
    'database': 'CRM_Dev'
}

print(f"\nAttempting connection to:")
print(f"  Host: {DB_CONFIG['host']}")
print(f"  Port: {DB_CONFIG['port']}")
print(f"  Database: {DB_CONFIG['database']}")
print(f"  User: {DB_CONFIG['user']}")
print("=" * 60)

try:
    # Attempt connection
    conn = pymysql.connect(**DB_CONFIG)
    print("\n✅ CONNECTION SUCCESSFUL!")
    
    # Test query
    cursor = conn.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()[0]
    print(f"✅ MySQL Version: {version}")
    
    # Check if view exists
    cursor.execute("SHOW TABLES LIKE 'vw_LastYearSales'")
    view_exists = cursor.fetchone()
    if view_exists:
        print(f"✅ View 'vw_LastYearSales' exists")
        
        # Get view structure
        cursor.execute("DESCRIBE vw_LastYearSales")
        columns = cursor.fetchall()
        print(f"\n📋 View columns:")
        for col in columns:
            print(f"   - {col[0]} ({col[1]})")
    else:
        print(f"❌ View 'vw_LastYearSales' NOT FOUND")
        print("\n📋 Available tables:")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        for table in tables:
            print(f"   - {table[0]}")
    
    cursor.close()
    conn.close()
    print("\n✅ Connection closed successfully")
    
except pymysql.err.OperationalError as e:
    print(f"\n❌ CONNECTION FAILED!")
    print(f"   Error Code: {e.args[0]}")
    print(f"   Error Message: {e.args[1]}")
    print("\n🔧 Possible issues:")
    print("   1. MySQL server not running")
    print("   2. MySQL not listening on 192.168.151.36:59041")
    print("   3. Firewall blocking connection")
    print("   4. User 'crm_user' doesn't have permission from this host")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ UNEXPECTED ERROR: {type(e).__name__}")
    print(f"   {str(e)}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
