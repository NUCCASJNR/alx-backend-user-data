#!/usr/bin/env python3


from flask import (Flask, make_response,
                   render_template, request, redirect, url_for)

app = Flask(__name__)

user_logs = {
    "user@1": "user1pwd",
    "user@2": "user2pwd"
}


@app.route('/cookie')
def cookie():
    res = make_response("<h1>cookie is set</h1>")
    res.set_cookie('foo', 'bar')
    return res


@app.route('/error')
def error():
    """Error"""
    return "<p><strong>Enter correct login details</strong></p>"


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/success', methods=['POST'])
def success():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['pass']

    if email in user_logs and user_logs[email] == password:
        resp = make_response(render_template('success.html'))
        resp.set_cookie('pwd', password)
        return resp
    else:
        return redirect(url_for('error'))


@app.route('/viewprofile')
def profile():
    email = request.cookies.get('pwd')
    resp = make_response(render_template('profile.html',name = email))
    return resp


if __name__ == '__main__':
    app.run(debug=True)
