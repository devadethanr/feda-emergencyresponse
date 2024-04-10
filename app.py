from flask import Flask, render_template, redirect, url_for, flash, request
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from bson.objectid import ObjectId
import bcrypt

app = Flask(__name__)
app.secret_key = 'c2637193455ab2085abf115e32195523a38116ffe57f1a9761fe4e1315f95f21'
app.config['TESTING'] = False
app.config["MONGO_URI"] = "mongodb://localhost:27017/test"
mongo = PyMongo(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, user_id, email, password):
        self.id = user_id
        self.email = email
        self.password = password

    @staticmethod
    def get(user_id):
        user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return User(user_data["_id"], user_data["email"], user_data["password"])
        return None

    @staticmethod
    def create(name, email, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = {"name": name, "email": email, "password": hashed_password.decode('utf-8')}
        inserted_id = mongo.db.users.insert_one(user).inserted_id
        return User(inserted_id, email, hashed_password.decode('utf-8'))

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/")
def index():
    """_summary_"""
    return render_template('dashboard.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

<<<<<<< Updated upstream
<<<<<<< Updated upstream
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
=======
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/signin", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        user = mongo.db.users.find_one({"email": email})

        if user and bcrypt.checkpw(password, user["password"].encode('utf-8')):
            user_obj = User(user["_id"], user["email"], user["password"])
            login_user(user_obj)
            if current_user.is_authenticated:
                next_url = request.args.get('next')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid email or password')
    return render_template('login.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
=======
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/signin", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        user = mongo.db.users.find_one({"email": email})

        if user and bcrypt.checkpw(password, user["password"].encode('utf-8')):
            user_obj = User(user["_id"], user["email"], user["password"])
            login_user(user_obj)
            if current_user.is_authenticated:
                next_url = request.args.get('next')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid email or password')
    return render_template('login.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
>>>>>>> Stashed changes
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        user = mongo.db.users.find_one({"email": email})
        if user:
            return render_template('register.html', error='Email already exists')
        else:
            User.create(name, email, password)
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
<<<<<<< Updated upstream
    return render_template('register.html')
>>>>>>> Stashed changes
=======
    return render_template('register.html')
>>>>>>> Stashed changes
