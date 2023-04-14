from flask import Flask, request, send_file
from scraper import get_course_equivalencies, get_ge_equivalencies, get_ges, CommunityCollege

app = Flask(__name__)


@app.route('/')
def index():
    return send_file('index.html')

@app.route('/data/course_eq')  # ?cc=DEANZA
def course_eq():
    # TODO: Eventually this will preform an sqlite select and return a json object.
    return str(get_course_equivalencies(CommunityCollege("", request.args['cc'])))


@app.route('/data/ge_eq')  # ?cc=DEANZA
def ge_eq():
    # TODO: Eventually this will preform an sqlite select and return a json object.
    return str(get_ge_equivalencies(CommunityCollege("", request.args['cc'])))


@app.route('/data/ges')
def ges():
    # TODO: Eventually this will preform an sqlite select and return a json object.
    return str(get_ges())


@app.route('/data/sjsu_courses')
def sjsu_courses():
    # TODO: Eventually this will preform an sqlite select and return a json object.
    return "Unimplemented"


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000)
