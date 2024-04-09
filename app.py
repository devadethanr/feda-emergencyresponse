from flask import Flask, render_template, redirect, url_for, flash, request

app = Flask(__name__)

@app.route("/")
def index():
    """_summary_
    """
    return render_template('index.html')


@app.route("/auth/login")
def login():
    """_summary_
    """
    return render_template('login.html')

    
@app.route("/auth/signup")
def signup():
    """_summary_
    """
    return render_template('register.html')