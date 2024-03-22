import subprocess
from datetime import datetime
import time

LOG_FILE = "logfile.log"

def get_active_connections():
    # Run a command to get the number of active connections
    cmd = "mysql -ugalle_user -pg@1alle@2 -e 'show status like \"Threads_connected\";'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    output = result.stdout.strip().split("\n")
    connections = int(output[1].split("\t")[1])
    return connections

def restart_mariadb():
    # Restart MariaDB service
    subprocess.run("sudo systemctl restart mariadb", shell=True)
    # Log restart event
    with open(LOG_FILE, "a") as logfile:
        logfile.write(f"{datetime.now()} - MariaDB server restarted\n")

def log_connection_status(connections):
    # Log connection status
    with open(LOG_FILE, "a") as logfile:
        logfile.write(f"{datetime.now()} - Active connections: {connections}\n")

def main():
    while True:
        current_time = datetime.now()
        log_connection_status(get_active_connections())
        if current_time.hour == 2:
            restart_mariadb()
            print("MariaDB server restarted at 2 am.")
        elif get_active_connections() > 300:
            restart_mariadb()
            print("MariaDB server restarted due to exceeding 300 connections.")
        # Sleep for 1 hour before checking again
        time.sleep(3600)  # 1 hour in seconds

if __name__ == "__main__":
    main()
