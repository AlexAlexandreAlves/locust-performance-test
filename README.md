# Installation guide

## Create a virtual environment (optional but recommended)
`python3 -m venv {$name}`
## Activate the virtual environment
`source {$name}/bin/activate`  
## Install dependencies
`pip install -r requirements.txt`

# Install with pip
`pip install -r requirements.txt`

# Run Locust with web interface
`locust -f locustfile.py`

# Run specific test file in headless mode without inform the host
`locust -f activities_post_test.py --headless -u 10 -r 1 --run-time 15s --logfile locust.log`

# Run Locust with multiple processes (workers)
`locust -f activities_post_test.py --headless -u 10 -r 1 --run-time 15s --processes {number_of_processes}--logfile locust.log` 