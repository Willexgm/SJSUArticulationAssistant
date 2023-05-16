import config
import database
from app import app
import requests
import threading
import json


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

    database.insert_into_CC(Name="San Joaquin Delta College", URL="SJDCCourseCatalogLink")
    database.insert_into_CCCourses(CCID=2, Prefix="MATH", Number=230, Title="SJDCTestCourse")
    database.insert_into_SJSUCourses(Prefix="MATH", Number=130, Title="SJSUSJDCTestCourse")
    database.insert_into_SJSUGenEd(Code="TM", Name="Test GE Math Name")
    database.insert_into_CToCEq(SJSUCourseID=2, CCCourseID=2, SetID=3)
    database.insert_into_GEEq(Code="TM", CCCourseID=2, SetID=3)

    database.insert_into_CC(Name="De Anza Ciy College", URL="DACCCourseCatalogLink")
    database.insert_into_CCCourses(CCID=3, Prefix="ENG", Number=440, Title="DACCTestCourse")
    database.insert_into_SJSUCourses(Prefix="ENG", Number=340, Title="SJSUDACCTestCourse")
    database.insert_into_SJSUGenEd(Code="TE", Name="Test GE English Name")
    database.insert_into_CToCEq(SJSUCourseID=3, CCCourseID=3, SetID=3)
    database.insert_into_GEEq(Code="TE", CCCourseID=3, SetID=3)

    database.insert_into_CC(Name="San Jose City College", URL="SJCCCourseCatalogLink")
    database.insert_into_CCCourses(CCID=4, Prefix="Hist", Number=550, Title="SJCCTestCourse")
    database.insert_into_SJSUCourses(Prefix="Hist", Number=450, Title="SJSUSJCCCTestCourse")
    database.insert_into_SJSUGenEd(Code="TH", Name="Test GE History Name")
    database.insert_into_CToCEq(SJSUCourseID=4, CCCourseID=4, SetID=3)
    database.insert_into_GEEq(Code="TH", CCCourseID=4, SetID=3)

    # Run the webserver in its own thread, so we can make requests to it.
    thread = threading.Thread(target=app.run, kwargs={'host': "0.0.0.0", 'port': 8000})
    thread.start()

    # Print out the json responses for each endpoint. We will manually make sure that it matches what we expect.
    print("Community Colleges\n", json.dumps(requests.get("http://127.0.0.1:8000/data/ccs").json(), indent=2))
    print("\nSJSU Courses\n", json.dumps(requests.get("http://127.0.0.1:8000/data/sjsu_courses").json(), indent=2))
    print("\nGEs\n", json.dumps(requests.get("http://127.0.0.1:8000/data/ges").json(), indent=2))
    print("\nCourse Equivalency\n", json.dumps(requests.get("http://127.0.0.1:8000/data/course_eq?sjsu_course=1").json(), indent=2))
    print("\nGE Equivalency", json.dumps(requests.get("http://127.0.0.1:8000/data/ge_eq?ge_code=TC").json(), indent=2))
