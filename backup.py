import os
import shutil
import datetime
import schedule
import time

def backup_database():
    """Create a backup of the database file"""
    # Define paths
    base_dir = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, 'data')
    backup_dir = os.path.join(base_dir, 'backups')
    
    # Create backup directory if it doesn't exist
    os.makedirs(backup_dir, exist_ok=True)
    
    # Generate timestamp for the backup filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Source and destination paths
    source = os.path.join(data_dir, 'dogs.db')
    destination = os.path.join(backup_dir, f'dogs_{timestamp}.db')
    
    # Copy the database file
    if os.path.exists(source):
        shutil.copy2(source, destination)
        print(f"Backup created: {destination}")
        
        # Keep only the last 10 backups
        backups = sorted([os.path.join(backup_dir, f) for f in os.listdir(backup_dir)])
        if len(backups) > 10:
            for old_backup in backups[:-10]:
                os.remove(old_backup)
                print(f"Removed old backup: {old_backup}")

# Schedule backups
schedule.every().day.at("00:00").do(backup_database)
# Also backup when the script starts
backup_database()

# Run the scheduler
if __name__ == "__main__":
    print("Backup scheduler started. Press Ctrl+C to exit.")
    while True:
        schedule.run_pending()
        time.sleep(60) 