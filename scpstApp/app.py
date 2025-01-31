# External imports
from flask import Flask, jsonify, request, render_template, session, redirect, url_for
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from time import sleep
from flask_login import login_required, LoginManager, login_user, logout_user, current_user
from datetime import datetime

# Local imports
from imageAPI import cropImage, ocrImage
from bucketAPI import download_from_bucket, get_blob_url
from firestoreAPI import *
from User import User
from licenseGetter import get_license_plate


# Global variables
global imagePath
imagePath = "static/images/fromthepi.png"

global coordinates
coordinates = None

global croppedImagePath
croppedImagePath = "static/cropped/cropped.png"

global bucketImagePath
bucketImagePath = "fromthepi.jpg"

# Flask app setup
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login page if not logged in

@login_manager.user_loader
def load_user(user_id):
    user = getUserByEmail(user_id)
    if user:
        return User.from_dict(user)
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        email = data.get('email')
        password = data.get('password')
        user = getUserByEmail(email)
        print("user var: ", user)
        if user and user.get('password') == password:
            login_user(User.from_dict(user))
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    user = current_user
    return render_template('index.html', user=user)

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.json
        user = getMostRecentUser()
        userData = {
            'email': data.get('email'),
            'password': data.get('password'),
            'name': data.get('name'),
            'license_plate': user.get('license_plate'),
            'credit_card': data.get('credit_card'),
            'last_entry': user.get('last_entry'),
            'last_exit': user.get('last_exit'),
            'photo': user.get('photo')
        }
        print(userData)
        updateUserByLicensePlate(userData.get('license_plate'), userData)
        return jsonify({"message": "Signup successful"}), 200
    return render_template('signup.html')

# Call this function to load the license localization model
@app.route('/model')
def model():
    global imagePath
    download_from_bucket(bucketImagePath, imagePath)
    return render_template('model.html', image=imagePath)

# Call this function to run the license localization model
@app.route('/runModel')
def run_model():
    # try:
        # Set up Firefox options for headless mode
        chrome_options = webdriver.FirefoxOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # Set up the Firefox driver
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=chrome_options)

        # Open the testing page
        driver.get('http://localhost:5000/model')

        sleep(7)

        # Close the browser
        driver.quit()

        global coordinates

        if coordinates is None:
            return jsonify({"message": "Model page opened successfully", "coordinates": "None", "licensePlate": "None"}), 200
        else:
            
            global imagePath
            print("Processing Image")
            cropImage(imagePath, coordinates)
            print("Cropped Image")
            text = ocrImage(croppedImagePath)
            print("Text: ", text)
            licensePlate = get_license_plate(text)
            print("licensePlate: ", licensePlate)
            user = getUserByLicensePlate(licensePlate)
            print("user var: ", user)
            if user is None:
                user  = {
                    'email': 'blank',
                    'name': 'blank',
                    'license_plate': licensePlate,
                    'password': 'blank',
                    'credit_card': 'blank',
                    'last_entry': datetime.now(),
                    'last_exit': 'blank',
                    'photo': get_blob_url(bucketImagePath)
                }
                addUser(user)
            else:
                if user['last_exit'] != 'blank':
                    user['last_entry'] = datetime.now()
                    user['last_exit'] = 'blank'
                else:
                    user['last_exit'] = datetime.now()
                updateUser(user)
            
            return jsonify({"message": "Model page opened successfully", "coordinates": coordinates, "licensePlate": text}), 200
    # except Exception as e:
    #     return jsonify({"error": str(e)}), 501

# Called by model.js when license plate is localized
@app.route('/detect', methods=['POST'])
def detect():
    global coordinates
    data = request.json
    coordinates = data
    print(coordinates)
    return jsonify({'message': 'Detection successful'}), 200


# Get the user list
@app.route('/users')
def get_users():
    users = getUsers()
    return jsonify(users), 200

if __name__ == '__main__':
    app.run(debug=True)