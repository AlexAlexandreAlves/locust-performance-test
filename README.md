# Locust Performance Testing

This project uses Locust to perform load testing on web applications. Locust is an easy-to-use and highly scalable load testing tool.

## Table of Contents
- [Intallation Guide](#installation-guide)
- [Executing Locust Tests](#executing-locust-tests)
- [Execution Throught Docker](#execution-throught-docker)
- [Main Commands](#main-commands)

## Intallation Guide

#### Create a virtual environment
```bash
python3 -m venv <environment_name>
```

#### Activate the virtual environment
```bash
source <environment_name>/bin/activate
```

#### Install dependencies
```bash
pip install -r requirements.txt
```

## Executing Locust Tests

#### Execute Locust with web interface
```bash
locust -f <locustfile.py>
```

#### Execute a specific test in headless mode
- Wheater execute the test out of the "tests" folder:

```bash
locust -f <environment_name>/tests/activities_post_test.py --headless -u 10 -r 1 --run-time 15s --logfile locust.log
```

#### Execute with multiple processes
- Wheater execute the test inside the "tests" folder:
```bash
locust -f activities_post_test.py --headless -u 10 -r 1 --run-time 15s --processes {number_of_processes} --logfile locust.log
```

## Execution Throught Docker

#### Build the Docker image
```bash
docker build -t locust-test .
```

#### Run the Docker container
```bash
docker run --rm -it -p 8089:8089 locust-test
```

## Main Commands
- Create a virtual environment: python3 -m venv `environment_name`
- Activate the virtual environment: source `environment_name`/bin/activate
- Install dependencies: pip install -r requirements.txt
- Execute Locust with web interface: locust -f `locustfile.py`
- Execute a specific test in headless mode:
  locust -f `environment_name`/tests/activities_post_test.py --headless -u 10 -r 1 --run-time 15s --logfile locust.log
- Execute with multiple processes:
  locust -f activities_post_test.py --headless -u 10 -r 1 --run-time 15s --processes `number_of_processes` --logfile locust.log
- Build Docker image: docker build -t locust-test .
- Execute Docker container: docker run --rm -it -p 8089:8089 locust-test

## Contributing
Contributions are welcome! Feel free to open issues or pull requests.

## License
This project is licensed under the MIT License.
