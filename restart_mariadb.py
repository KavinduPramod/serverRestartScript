from flask import Flask
import subprocess
import time
from threading import Thread

app = Flask(__name__)

# Function to get current number of connections
def get_connection_count():
    result = subprocess.run(["mysql", "-ugalle_user", "-pg@1alle@2", "-e", 'show status like "Threads_connected";'], capture_output=True, text=True)
    output = result.stdout.strip().split('\n')
    for line in output:
        if line.startswith('Threads_connected'):
            return int(line.split()[1])

# Function to monitor connections in a background thread
def monitor_connections():
    threshold = 50
    while True:
        connections = get_connection_count()
        if connections > threshold:
            subprocess.run(['sudo', 'systemctl', 'restart', 'mariadb'])
            print(f"Restarted MariaDB. Current connections: {connections}")
        time.sleep(300)  # Sleep for 5 minutes

# Start monitoring thread when the script is executed
if __name__ == "__main__":
    monitor_thread = Thread(target=monitor_connections)
    monitor_thread.daemon = True
    monitor_thread.start()

    app.run(host='0.0.0.0', port=5000)
