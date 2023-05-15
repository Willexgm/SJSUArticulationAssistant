import config
from flask import Flask, request, send_file, g
import sqlite3
import database

app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(config.DB_NAME)
    return db


@app.route('/')
def index():
    return send_file('index.html')


@app.route('/data/course_eq')  # ?sjsu_course=<id>
def course_eq():
    database.set_connection(get_db())

    j = {}
    for set_id, CPrefix, CNumber, CTitle, CCName in database.join_from_CToCEq(request.args['sjsu_course']):
        if CCName not in j:
            j[CCName] = {}
        if set_id not in j[CCName]:
            j[CCName][set_id] = []
        j[CCName][set_id].append({"prefix": CPrefix, "number": CNumber, "title": CTitle})

    return j


@app.route('/data/ge_eq')  # ?ge_code=<id>
def ge_eq():
    database.set_connection(get_db())

    j = {}
    for CPrefix, CNumber, CTitle, CCName in database.join_from_GEEq(request.args['ge_code']):
        if CCName not in j:
            j[CCName] = []
        j[CCName].append({"prefix": CPrefix, "number": CNumber, "title": CTitle})

    return j


@app.route('/data/ccs')
def ccs():
    database.set_connection(get_db())
    j = [{"name": x[1], "url": x[2]} for x in database.select_all_from_CC()]
    return j


@app.route('/data/ges')
def ges():
    database.set_connection(get_db())
    j = [{"code":x[0], "name":x[1]} for x in database.select_all_from_SJSUGenEd()]
    return j


@app.route('/data/sjsu_courses')
def sjsu_courses():
    database.set_connection(get_db())
    j = [{"id": x[0], "prefix": x[1], "number": x[2], "title": x[3]} for x in database.select_all_from_SJSUCourses()]
    return j


@app.teardown_appcontext
def close_connection(e):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
