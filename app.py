from flask import Flask, render_template, redirect, url_for, flash, request
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from bson.objectid import ObjectId
import bcrypt

app = Flask(__name__)
app.secret_key = 'c2637193455ab2085abf115e32195523a38116ffe57f1a9761fe4e1315f95f21'
app.config['TESTING'] = False
app.config["MONGO_URI"] = "mongodb+srv://fedauser:fedauser@fedacluster.aemzpay.mongodb.net/fedadb"
mongo = PyMongo(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    """_summary_

    Args:
        UserMixin (_type_): _description_
    """
    def __init__(self, user_id, email, password, name):
        self.id = user_id
        self.email = email
        self.password = password
        self.name = name

    @staticmethod
    def get(user_id):
        """_summary_

        Args:
            user_id (_type_): _description_

        Returns:
            _type_: _description_
        """
        user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return User(user_data["_id"], 
                        user_data["email"], user_data["password"], user_data["name"])
        return None

    @staticmethod
    def create(name, email, password):
        """_summary_

        Args:
            name (_type_): _description_
            email (_type_): _description_
            password (_type_): _description_

        Returns:
            _type_: _description_
        """
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = {"name": name, "email": email, "password": hashed_password.decode('utf-8')}
        inserted_id = mongo.db.users.insert_one(user).inserted_id
        return User(inserted_id, email, hashed_password.decode('utf-8'), name)

@login_manager.user_loader
def load_user(user_id):
    """_summary_

    Args:
        user_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    return User.get(user_id)

@app.route("/")
def index():
    """_summary_"""
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """_summary_

    Returns:
        _type_: _description_
    """
    return render_template('dashboard.html', name=current_user.name)

@app.route('/logout')
@login_required
def logout():
    """_summary_

    Returns:
        _type_: _description_
    """
    logout_user()
    return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    """_summary_

    Returns:
        _type_: _description_
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        user = mongo.db.users.find_one({"email": email})

        if user and bcrypt.checkpw(password, user["password"].encode('utf-8')):
            user_obj = User(user["_id"], user["email"], user["password"], user["name"])
            login_user(user_obj)
            if current_user.is_authenticated:
                next_url = request.args.get('next')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect(url_for('dashboard'))
        else:
            return render_template('auth/login.html', error='Invalid email or password')
    return render_template('auth/login.html')


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    """_summary_

    Returns:
        _type_: _description_
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        user = mongo.db.users.find_one({"email": email})
        if user:
            return render_template('auth/signup.html', error='Email already exists')
        else:
            User.create(name, email, password)
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('auth/signup.html')
