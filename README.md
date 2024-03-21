# serverRestartScript
# Server Restart Script with Gunicorn

This guide explains how to run a Python script (`restart_mariadb.py`) on an Ubuntu server using Gunicorn. The script manages MariaDB server restarts based on certain conditions.

## Script Overview

The `restart_mariadb.py` script performs the following tasks:

- Checks the current connections to MariaDB every 5 minutes.
- Restarts the MariaDB server if the number of connections exceeds a certain threshold.
- Scheduled to restart MariaDB at 2 AM every day.

## Prerequisites

Ensure the following are installed on your Ubuntu server:
- Python 3
- pip (Python package manager)

## Installation

1. **Install Gunicorn:**
    ```bash
    sudo apt install gunicorn
    ```

2. **Install Required Python Packages:**
    ```bash
    sudo apt install python3-psutil python3-apscheduler
    ```

## Transfer Script to Server

Transfer the `serverRestartScript` folder containing the `restart_mariadb.py` script to your server using SCP or any preferred method.

## Running the Script with Gunicorn

1. **Connect to the Server:**
    ```bash
    ssh coopmis6@your_droplet_ip
    ```

2. **Navigate to the Folder:**
    ```bash
    cd /path/to/serverRestartScript
    ```

3. **Run the Script with Gunicorn:**
    ```bash
    gunicorn -w 4 -b 0.0.0.0:8000 restart_mariadb:app --daemon
    ```

    Replace `/path/to/serverRestartScript` with the actual path to your script.

## Monitoring and Managing Gunicorn

- **Monitor Gunicorn Process:**
    ```bash
    ps aux | grep gunicorn
    ```

- **Stop Gunicorn Process:**
    Identify the Gunicorn process ID (PID) from the output of the above command and use the following to stop it:
    ```bash
    kill <pid>
    ```

## About the Script

- **Script Location:** The `restart_mariadb.py` script should be located in the `serverRestartScript` folder.
- **Functionality:** Monitors MariaDB connections and restarts the server if the connection threshold is exceeded.
- **Logging:** Logs restart events and connection status to a file named `logfile.log` in the same directory.
- **Customization:** Customize the script and Gunicorn configuration according to your requirements.
- **Permissions:** Ensure proper permissions are set for the script and log file.

