# SJSU Articulation Assistant

## Setup with Docker
Build the image using the Dockerfile
```
% docker build -t articulation_assistant .
```
Start a container with port 80 mapped to 8000
```
% docker run -p 8000:8000 articulation_assistant
```
You can access the application through `http://127.0.0.0:8000` in a browser

## Flask App Endpoints
`GET /data/ccs`
Returns a json object list of CC objects.

`GET /data/sjsu_courses`
Returns a json with a list of SJSU course objects. The course object will contain an ID that is needed to get course to course equivalencies.

`GET /data/course_eq?sjsu_course=<id>`
Returns a json object with sets of CC courses for each CC that are equivalent to the given SJSU course ID. The SJSU course ID comes from the above request. 

`GET /data/ges`
Returns a json object list of SJSU GE objects. The GE object will contain a code that is needed to get GE equivalencies.

`GET /data/ge_eq?ge_code=<code>`
Returns a json object with CC courses that fulfill the given SJSU GE. The GE code comes from the above request.