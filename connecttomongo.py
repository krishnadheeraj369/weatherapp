from flask import Flask, request, jsonify, send_from_directory, render_template, url_for, redirect, session
import pymongo
import requests
from flask_cors import CORS
import os
from custdata import signup_bp
from logincheck import login_bp
import secrets


app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(24)


app.register_blueprint(signup_bp, url_prefix='/')
app.register_blueprint(login_bp, url_prefix='/')


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["jsonimport"]  
collection = db["data"]  

api_key = "3e956df397219806539b86ca86ff7c6b"

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('weather'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        return redirect(url_for('signup_successful'))
    return render_template('signup.html')

@app.route('/signup_successful')
def signup_successful():
    return render_template('signup_successful.html')

@app.route('/weather')
def weather():
    return render_template('weather.html')

@app.route('/logout')
def logout():
    # Clear session data
    session.clear()
    # Redirect to login page
    return redirect(url_for('login'))


@app.route('/search_zip', methods=['GET'])
def search_zip():
    search_zip_code = request.args.get('zip_code')
    if not search_zip_code:
        return jsonify({'error': 'Zip code not provided'}), 400
    

    city = collection.find_one({"zip_code": int(search_zip_code)})
    if city:
        url = f"http://api.openweathermap.org/data/2.5/forecast?zip={search_zip_code},us&appid={api_key}"
        response = requests.get(url)
        weather_data = response.json()
        return jsonify({
            "zip_code": search_zip_code,
            "county": city["county"],
            "state": city["state"],
            "city": city["city"],
            "weather" : weather_data
        }), 200
    else:
        return jsonify({"Error" : "Zip code not found, use post method if you wish to insert a new record "})
    
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    app.run(debug=True)
