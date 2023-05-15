import config
import database
from app import app
import requests
import threading


if __name__ == '__main__':
    # Ensure that we are in TEST mode.
    if config.RUN_MODE != "TEST":
        raise Exception("Configuration not in \"TEST\" mode.")

    # Initialize the test db.
    database.init_database()

    # Insert test data into the database.
    database.insert_into_CC(Name="Test College", URL="TESTC")
    # TODO: Insert more data into the db to allow us to fully test each of the flask data endpoints

    # Run the webserver in its own thread, so we can make requests to it.
    threading.Thread(target=app.run, kwargs={'host': "0.0.0.0", 'port': 8000}).start()

    # Print out the json response. We will manually make sure that it matches what we expect.
    print(requests.get("http://127.0.0.1:8000/data/ccs").json())
    # TODO: Print out the json responses for each of the other flask endpoints.
