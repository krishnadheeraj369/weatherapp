from flask import Flask, request, render_template, redirect, url_for, flash, Blueprint
from pymongo import MongoClient
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

login_bp = Blueprint('login', __name__, template_folder='templates')



client = MongoClient('mongodb://localhost:27017/')
db = client['customerinfo'] 
collection = db["data"] 

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = collection.find_one({'username': username})
        
        if user and user['password'] == password:
            return redirect(url_for('weather'))
        else:
            flash('Invalid username or password')
            return render_template('login.html')
    
    return render_template('login.html')

@login_bp.route('/weather')
def weather():
    return render_template('weather.html')

if __name__ == '__main__':
    app.run(debug=True)
