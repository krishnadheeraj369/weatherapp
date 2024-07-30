from flask import Flask,Blueprint, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

signup_bp = Blueprint('signup', __name__,template_folder='templates')




client = MongoClient('mongodb://localhost:27017/')
db = client['customerinfo']
collection = db["data"]  

@signup_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        user = collection.find_one({"username": username})
        if user:
            flash('Username already exists')
            return redirect(url_for('signup'))

        collection.insert_one({
            'username': username,
            'email': email,
            'password': password
        })
        return redirect(url_for('signup.signup_successful'))
    
    return render_template('signup.html')

@signup_bp.route('/signup_successful')
def signup_successful():
    return render_template('signup_successful.html')

