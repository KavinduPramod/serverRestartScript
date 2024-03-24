# Simple MariaDB Monitoring and Restart Script with Flask

This is a simple script written in Python using Flask that monitors the number of connections to a MariaDB database and restarts MariaDB if the number of connections exceeds a specified threshold.

## Code Explanation

- **Flask App Setup**: Imports the Flask module and initializes a Flask application.

- **Function to Get Connection Count**: Defines a function (`get_connection_count()`) to retrieve the current number of connections to the MariaDB database using the `mysql` command-line tool.

- **Function to Monitor Connections**: Defines a function (`monitor_connections()`) to continuously monitor the number of connections in a background thread. If the number of connections exceeds a specified threshold, it restarts MariaDB using `sudo systemctl restart mariadb`.

- **Main Execution Block**: Starts the monitoring thread and runs the Flask application on all available interfaces (`0.0.0.0`) and port `5000`.

## Usage

- Ensure that the MariaDB username (`galle_user`) and password (`g@1alle@2`) are correctly provided in the `get_connection_count()` function.
- Adjust the `threshold` variable according to your requirements.
- Run the script and access the monitoring endpoint at `http://your_server_ip:5000/monitor`.

