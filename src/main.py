from signalrcore.hub_connection_builder import HubConnectionBuilder

import psycopg2
import logging
import requests
import json
import time


class App:
    def __init__(self):
        self._hub_connection = None
        self.TICKS = 10

        # To be configured by your team
        self.HOST = 'http://159.203.50.162'  # Setup your host here
        self.TOKEN = 'd6d30081b5c69ca5f983'  # Setup your token here
        self.T_MAX = '30'  # Setup your max temperature here
        self.T_MIN = '5'  # Setup your min temperature here
        self.DATABASE_URL = 'postgresql://user01eq12:5sLE9lGcyg3WV0h3@157.230.69.113:5432/db01eq12'  # Setup your database here


        self.CONN_DB = psycopg2.connect(self.DATABASE_URL)

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
        elif float(temperature) <= float(self.T_MIN):
            self.send_action_to_hvac(timestamp, "TurnOnHeater")

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
            cursor = self.CONN_DB.cursor()
            timestamp = timestamp.replace('T', ' ')
            insert_query = f'''INSERT INTO "HvacEvent" (timestamp,event) VALUES (%s,%s)'''
            record = (f'{timestamp}',f'{action}')

            cursor.execute(insert_query, record)

            self.CONN_DB.commit()
            cursor.close()

            self.printRowCount("HvacEvent")
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
            cursor = self.CONN_DB.cursor()

            timestamp = timestamp.replace('T', ' ')
            insert_query = f'''INSERT INTO "HvacTemperature" (timestamp,temp) VALUES (%s,%s)'''
            record = (f'{timestamp}',temperature)

            cursor.execute(insert_query, record)

            self.CONN_DB.commit()
            cursor.close()

            self.printRowCount("HvacTemperature")
            pass
        except requests.exceptions.RequestException as e:
            print("from save_event_to_database\n")
            print(e)
            # To implement
            pass
    
    def printRowCount(self, table):
        try:
            cursor = self.CONN_DB.cursor()
            insert_query = f'''select * from "{table}";'''
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
            # To implement
            pass

if __name__ == "__main__":
    app = App()
    app.start()
