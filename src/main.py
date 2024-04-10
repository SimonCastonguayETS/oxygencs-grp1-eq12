from signalrcore.hub_connection_builder import HubConnectionBuilder
from dotenv import load_dotenv
from pathlib import Path

import psycopg2
import logging
import requests
import json
import time
import os


class App:
    def __init__(self):
        # Comment2
        self._hub_connection = None
        self.TICKS = 10

        # Path for Docker environment
        docker_env_path = Path("/usr/src/app/config.env")

        # Path for local environment (assuming config.env is in the same directory as this script)
        local_env_path = Path("config.env")

        # Check if the Docker path exists, otherwise use the local path
        dotenv_path = docker_env_path if docker_env_path.exists() else local_env_path

        load_dotenv(dotenv_path)

        self.HOST = os.environ.get("OXYGENCS_HOST")  # TEst
        self.TOKEN = os.environ.get("OXYGENCS_TOKEN")
        self.T_MAX = os.environ.get("OXYGENCS_T_MAX", "100")
        self.T_MIN = os.environ.get("OXYGENCS_T_MIN", "1")
        self.DATABASE_URL = os.environ.get("OXYGENCS_DATABASE_URL")

        try:
            self.CONN_DB = psycopg2.connect(self.DATABASE_URL)
        except Exception as e:
            print(e)
            # To implement
            pass

    def __del__(self):
        if self._hub_connection != None:
            self._hub_connection.stop()

    def start(self):
        """Start Oxygen CS."""
        self.setup_sensor_hub()
        self._hub_connection.start()
        print("Press CTRL+C to exit.")
        while True:
            time.sleep(2)

    def setup_sensor_hub(self):
        """Configure hub connection and subscribe to sensor data events."""
        self._hub_connection = (
            HubConnectionBuilder()
            .with_url(f"{self.HOST}/SensorHub?token={self.TOKEN}")
            .configure_logging(logging.INFO)
            .with_automatic_reconnect(
                {
                    "type": "raw",
                    "keep_alive_interval": 10,
                    "reconnect_interval": 5,
                    "max_attempts": 999,
                }
            )
            .build()
        )
        self._hub_connection.on("ReceiveSensorData", self.on_sensor_data_received)
        self._hub_connection.on_open(lambda: print("||| Connection opened."))
        self._hub_connection.on_close(lambda: print("||| Connection closed."))
        self._hub_connection.on_error(
            lambda data: print(f"||| An exception was thrown closed: {data.error}")
        )

    def on_sensor_data_received(self, data):
        """Callback method to handle sensor data on reception."""
        print(data[0]["date"] + " --> " + data[0]["data"], flush=True)
        timestamp = data[0]["date"]
        temperature = float(data[0]["data"])
        self.take_action(timestamp, temperature)
        self.save_event_to_database(timestamp, temperature)

    def take_action(self, timestamp, temperature):
        """Take action to HVAC depending on current temperature."""
        if float(temperature) >= float(self.T_MAX):
            self.send_action_to_hvac(timestamp, "TurnOnAc")
            return "TurnOnAc"
        elif float(temperature) <= float(self.T_MIN):
            self.send_action_to_hvac(timestamp, "TurnOnHeater")
            return "TurnOnHeater"

    def send_action_to_hvac(self, timestamp, action):
        """Send action query to the HVAC service."""
        r = requests.get(f"{self.HOST}/api/hvac/{self.TOKEN}/{action}/{self.TICKS}")
        details = json.loads(r.text)
        print(details, flush=True)
        self.save_action_to_database(timestamp, action)

    def save_action_to_database(self, timestamp, action):
        """Save action into database."""
        try:
            # To implement
            countPreEx = self.getNumRow("HvacEvent")

            cursor = self.CONN_DB.cursor()
            timestamp = timestamp.replace("T", " ")
            insert_query = (
                f"""INSERT INTO "HvacEvent" (timestamp,event) VALUES (%s,%s)"""
            )
            record = (f"{timestamp}", f"{action}")

            cursor.execute(insert_query, record)

            self.CONN_DB.commit()
            cursor.close()

            # self.printRowCount("HvacEvent")
            countFin = self.getNumRow("HvacEvent")
            return countFin == (countPreEx + 1)

            pass
        except requests.exceptions.RequestException as e:
            print("from save_action_to_database\n")
            print(e)
            # To implement
            pass

    def save_event_to_database(self, timestamp, temperature):
        """Save sensor data into database."""
        try:
            # To implement
            countPreEx = self.getNumRow("HvacTemperature")

            cursor = self.CONN_DB.cursor()

            timestamp = timestamp.replace("T", " ")
            insert_query = (
                f"""INSERT INTO "HvacTemperature" (timestamp,temp) VALUES (%s,%s)"""
            )
            record = (f"{timestamp}", temperature)

            cursor.execute(insert_query, record)

            self.CONN_DB.commit()
            cursor.close()

            countFin = self.getNumRow("HvacTemperature")
            return countFin == (countPreEx + 1)
            pass
        except requests.exceptions.RequestException as e:
            print("from save_event_to_database\n")
            print(e)
            # To implement
            pass

    def printRowCount(self, table):
        try:
            cursor = self.CONN_DB.cursor()

            insert_query = f"""select * from "{table}";"""
            cursor.execute(insert_query)

            mobile_records = cursor.fetchall()
            count = 0
            for row in mobile_records:
                count = count + 1
            print("amount of row = ", count)

            cursor.close()
            pass
        except requests.exceptions.RequestException as e:
            print("from printRowCount\n")
            print(e)
            pass

    def getNumRow(self, table):
        try:
            cursor = self.CONN_DB.cursor()
            insert_query = f"""select * from "{table}";"""
            cursor.execute(insert_query)

            mobile_records = cursor.fetchall()
            count = 0
            for row in mobile_records:
                count = count + 1
            cursor.close()
            return count
            pass
        except requests.exceptions.RequestException as e:
            print(e)
            pass


if __name__ == "__main__":
    app = App()
    app.start()
