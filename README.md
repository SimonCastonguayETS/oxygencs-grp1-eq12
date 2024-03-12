# LOG-680 : Template for Oxygen-CS

This Python application continuously monitors a sensor hub and manages HVAC (Heating, Ventilation, and Air Conditioning) system actions based on received sensor data.

It leverages `signalrcore` to maintain a real-time connection to the sensor hub and utilizes `requests` to send GET requests to a remote HVAC control endpoint.

This application uses `pipenv`, a tool that aims to bring the best of all packaging worlds to the Python world.

## Requierements

- Python 3.12+
- pip

## Getting Started
Creation and action of the virtual environnement

```bash
py -m venv .venv
.venv\Scripts\activate
```

Install the project's dependencies :

```bash
pip install -r requirements.txt
```

## Setup

You need to setup the following variables inside the App class:

- HOST: The host of the sensor hub and HVAC system.
- TOKEN: The token for authenticating requests.
- T_MAX: The maximum allowed temperature.
- T_MIN: The minimum allowed temperature.
- DATABASE_URL: The database connection URL.

## Running the Program

After setup, you can start the program with the following command:

```bash
pipenv run start
```

## Running the test

After setup, you can start the test with the following command:

```bash
pytest test/test.py
```

## Logging

The application logs important events such as connection open/close and error events to help in troubleshooting.

## To Implement

There are placeholders in the code for sending events to a database and handling request exceptions. These sections should be completed as per the requirements of your specific application.

## License

MIT

## Contact

For more information, please feel free to contact the repository owner.
