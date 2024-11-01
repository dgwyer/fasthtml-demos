from fastlite import database
import os

# Before running the migration script:
# - Set app into maintenance mode?
# - Backup the database
# - Run during low traffic periods if possible

# use 'unset MAINTENANCE_MODE' to disable maintenance mode via the terminal, and 'export MAINTENANCE_MODE=true' to enable it

"""
Try this workflow to set maintenance mode:

# config.py
import os

MAINTENANCE_MODE = os.getenv('MAINTENANCE_MODE', '0') == '1'

# app.py
from config import MAINTENANCE_MODE

@app.before_request
def check_maintenance():
    if MAINTENANCE_MODE and not request.path.startswith('/maintenance'):
        return render_template('maintenance.html'), 503

# migrate.py
os.environ['MAINTENANCE_MODE'] = '1'
try:
    migrate()
finally:
    os.environ['MAINTENANCE_MODE'] = '0'
"""

MAINTENANCE_MODE = False

def set_mm():
    env_key = 'MAINTENANCE_MODE'
    mm = 'false'
    try:
        print(f"Test environ key: {env_key}")
        mm = os.environ[env_key]
    except KeyError:
        print(f"{env_key} not found in environment variables")
    if mm == 'true':
        print(f"Maintenance mode is enabled: {mm}")
    else:
        print(f"Maintenance mode is disabled: {mm}")

def migrate():
    db = database('data/main.db')
    
    print("Migrating users table: adding email column...")
    
    try:
        # Start transaction
        db.execute("BEGIN TRANSACTION;")
        
        # 1. Create new table with desired schema
        db.execute("""
        CREATE TABLE users_new (
            id INTEGER PRIMARY KEY,
            name TEXT,
            pwd TEXT,
            email TEXT UNIQUE DEFAULT NULL
        );
        """)
        
        # 2. Copy data from old table to new table
        print("Copying data to new table...")
        db.execute("""
        INSERT INTO users_new (id, name, pwd)
        SELECT id, name, pwd FROM users;
        """)
        
        # Verify data was copied
        count_old = db.q("SELECT COUNT(*) as count FROM users")[0]['count']
        count_new = db.q("SELECT COUNT(*) as count FROM users_new")[0]['count']
        print(f"Copied {count_new} of {count_old} records")
        
        if count_old != count_new:
            raise Exception("Data copy mismatch!")
            
        # 3. Drop old table
        print("Dropping old table...")
        db.execute("DROP TABLE users;")
        
        # 4. Rename new table to original name
        print("Renaming new table...")
        db.execute("ALTER TABLE users_new RENAME TO users;")
        
        # Commit transaction
        db.execute("COMMIT;")
        print("Migration complete")
        
    except Exception as e:
        # If anything goes wrong, rollback
        db.execute("ROLLBACK;")
        print(f"Migration failed: {str(e)}")
        raise

if __name__ == "__main__":
    migrate()