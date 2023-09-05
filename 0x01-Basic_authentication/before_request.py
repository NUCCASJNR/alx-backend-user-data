from flask import Flask, request

app = Flask(__name__)

# Define a before_request function
@app.before_request
def before_request():
    # This code will run before every request

    # You can perform any necessary tasks here, such as authentication, logging, etc.
    # For example, let's log the incoming request's method and URL
    print(f"Request Method: {request.method}, Request URL: {request.url}")

# Define a route
@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
