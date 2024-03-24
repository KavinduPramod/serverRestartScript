from flask import Flask
import subprocess
import time
from threading import Thread, Event
import schedule
from datetime import datetime
import pymysql

app = Flask(__name__)
restart_event = Event()


# Function to get current number of connections
def get_connection_count():
    result = subprocess.run(["mysql", "-ugalle_user", "-pg@1alle@2", "-e", 'show status like "Threads_connected";'],
                            capture_output=True, text=True)
    output = result.stdout.strip().split('\n')
    for line in output:
        if line.startswith('Threads_connected'):
            return int(line.split()[1])


# Function to monitor connections in a background thread
def monitor_connections():
    threshold = 800
    while True:
        connections = get_connection_count()
        if connections > threshold:
            restart_event.set()  # Set the restart event
            print("Restart flag set. Waiting for ongoing transactions to complete.")
        time.sleep(300)  # Sleep for 5 minutes


# Function to restart MariaDB at 2 am every day
def restart_mariadb():
    restart_event.set()  # Set the restart event
    print("Restart flag set. Waiting for ongoing transactions to complete.")
    while True:
        # Check if there are ongoing transactions
        if not are_transactions_ongoing():
            break
        time.sleep(10)  # Wait for 10 seconds before checking again
    subprocess.run(['sudo', 'systemctl', 'restart', 'mariadb'])
    with open('logfile.log', 'a') as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] Restarted MariaDB at 2 am.\n")


# Function to check if there are ongoing transactions
def are_transactions_ongoing():
    try:
        connection = pymysql.connect(host='localhost',
                                     user='galle_user',
                                     password='g@1alle@2',
                                     database='information_schema',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            # Check if there are any active transactions
            cursor.execute("SELECT * FROM information_schema.innodb_trx")
            transactions = cursor.fetchall()
            if transactions:
                # Active transactions found
                return True
            else:
                return False
    except Exception as e:
        print(f"Error checking transactions: {e}")
        return True  # Return True to be safe

    finally:
        if connection:
            connection.close()


# Start monitoring thread when the script is executed
if __name__ == "__main__":
    monitor_thread = Thread(target=monitor_connections)
    monitor_thread.daemon = True
    monitor_thread.start()

    with open('logfile.log', 'a') as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] Started the script. \n")

    # Schedule MariaDB restart at 2 am
    schedule.every().day.at("02:00").do(restart_mariadb)

    # Run Flask app
    app.run(host='0.0.0.0', port=5000)

