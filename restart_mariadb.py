from flask import Flask
import subprocess
import time
from threading import Thread
import schedule
import datetime

app = Flask(__name__)

# Function to get current number of connections
def get_connection_count():
    result = subprocess.run(["mysql", "-uuser", "-p123", "-e", 'show status like "Threads_connected";'], capture_output=True, text=True)
    output = result.stdout.strip().split('\n')
    for line in output:
        if line.startswith('Threads_connected'):
            return int(line.split()[1])

# Function to backup the database
def backup_database():
    backup_file = f"backup_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.sql"
    subprocess.run(["mysqldump", "-uuser", "-p123", "userdb", f"> {backup_file}"], shell=True)
    print(f"Database backed up to {backup_file}")

# Function to monitor connections in a background thread
def monitor_connections():
    threshold = 50
    while True:
        connections = get_connection_count()
        if connections > threshold:
            backup_database()  # Backup the database before restarting
            subprocess.run(['sudo', 'systemctl', 'restart', 'mariadb'])
            print(f"Restarted MariaDB. Current connections: {connections}")
        time.sleep(300)  # Sleep for 5 minutes

# Function to restart MariaDB at 2 AM every day
def restart_mariadb():
    backup_database()  # Backup the database before restarting
    subprocess.run(['sudo', 'systemctl', 'restart', 'mariadb'])
    print("Restarted MariaDB at 2 AM.")

# Start monitoring thread when the script is executed
if __name__ == "__main__":
    monitor_thread = Thread(target=monitor_connections)
    monitor_thread.daemon = True
    monitor_thread.start()

    # Schedule MariaDB restart at 2 AM daily
    schedule.every().day.at("17:05").do(restart_mariadb)

    # Flask app run
    app.run(host='0.0.0.0', port=5000)
