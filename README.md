# SJSU Articulation Assistant

### Setup with Docker
Build the image using the Dockerfile
```
% docker build -t articulation_assistant .
```
Start a container with port 80 mapped to 8000
```
% docker run -p 80:8000 articulation_assistant
```
You can access the application through `http://127.0.0.0` in a browser
