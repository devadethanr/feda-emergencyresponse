from flask import Flask, render_template, redirect, url_for, flash, request

app = Flask(__name__)

@app.route("/")
def index():
    """_summary_
    """
    return render_template('index.html')


@app.route("/signin")
def login():
    """_summary_
    """
    return render_template('auth/signin.html')

@app.route("/signup")
def signup():
    """_summary_
    """
    return render_template('auth/signup.html')
