import os
import psutil
import subprocess
import datetime
import logging
from apscheduler.schedulers.background import BackgroundScheduler

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Configure logging
log_file = os.path.join(script_dir, 'logfile.log')
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def restart_mariadb(reason):
    subprocess.run(['sudo', 'systemctl', 'restart', 'mariadb'])
    logging.info(f'Restarted MariaDB: {reason}')

def check_connections_threshold():
    # Get current connections to MariaDB
    connections = psutil.net_connections()
    mariadb_connections = [conn for conn in connections if '3306' in conn.laddr]

    # Check if the number of connections exceeds the threshold (e.g., 800)
    if len(mariadb_connections) > 800:
        restart_mariadb('Max connections reached')

if __name__ == "__main__":
    # Configure scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(restart_mariadb, 'cron', hour=2, args=['Scheduled restart'])  # Schedule restart_mariadb() to run at 2 AM every day
    scheduler.add_job(check_connections_threshold, 'cron', minute='*/5')  # Check connections every 5 minutes
    scheduler.start()

    # Logging only scheduler start and job addition information
    logging.info('Scheduler started')
    logging.info('Added job "restart_mariadb" to job store "default"')
    logging.info('Added job "check_connections_threshold" to job store "default"')

    # Wait indefinitely
    while True:
        pass
