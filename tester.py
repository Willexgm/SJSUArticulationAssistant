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

    # Insert test data into the database for each of the tables.
    database.insert_into_CC(Name="Test College", URL="TESTC")
    database.insert_into_CCCourses(CCID=1, Prefix="Test Prefix", Number=222, Title="Test CC Course")
    database.insert_into_SJSUCourses(Prefix="Test Prefix", Number=111, Title="Test SJSU Course")
    database.insert_into_SJSUGenEd(Code="TC", Name="Test GE Name")
    database.insert_into_CToCEq(SJSUCourseID=1, CCCourseID=1, SetID=3)
    database.insert_into_GEEq(Code="TC", CCCourseID=1, SetID=3)

    # Run the webserver in its own thread, so we can make requests to it.
    thread = threading.Thread(target=app.run, kwargs={'host': "0.0.0.0", 'port': 8000})
    thread.start()

    # Print out the json responses for each endpoint. We will manually make sure that it matches what we expect.
    print(requests.get("http://127.0.0.1:8000/data/ccs").json())
    print(requests.get("http://127.0.0.1:8000/data/sjsu_courses").json())
    print(requests.get("http://127.0.0.1:8000/data/ges").json())
    print(requests.get("http://127.0.0.1:8000/data/course_eq?sjsu_course=1").json())
    print(requests.get("http://127.0.0.1:8000/data/ge_eq?ge_code=TC").json())
