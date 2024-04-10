import pytest
from datetime import datetime
from src.main import *
import psycopg2

#def test_event():
    #app = App()
    #app.DATABASE_URL = 'postgresql://user01eq12:5sLE9lGcyg3WV0h3@157.230.69.113:5432/db01eq12'
    #app.CONN_DB = psycopg2.connect(app.DATABASE_URL)

    #assert app.save_action_to_database(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "TurnOnAc")
    #app.CONN_DB.close()

#def test_temp():
    #app = App()
    #app.DATABASE_URL = 'postgresql://user01eq12:5sLE9lGcyg3WV0h3@157.230.69.113:5432/db01eq12'
    #app.CONN_DB = psycopg2.connect(app.DATABASE_URL)

    #assert app.save_event_to_database(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '596')
    #app.CONN_DB.close()
    

def test_ActiveHeater():
    app = App()
    app.DATABASE_URL = 'postgresql://user01eq12:5sLE9lGcyg3WV0h3@157.230.69.113:5432/db01eq12'
    app.CONN_DB = psycopg2.connect(app.DATABASE_URL)

    app.T_MAX = '200'   # juste pour etre sure
    app.T_MIN = '100'
    assert app.take_action(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '5') == "TurnOnHeater"
    app.CONN_DB.close()

def test_ActiveAC():
    app = App()
    app.DATABASE_URL = 'postgresql://user01eq12:5sLE9lGcyg3WV0h3@157.230.69.113:5432/db01eq12'
    app.CONN_DB = psycopg2.connect(app.DATABASE_URL)

    app.T_MAX = '100'
    app.T_MIN = '0' # juste pour etre sure
    assert app.take_action(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '200') == "TurnOnAc"
    app.CONN_DB.close()