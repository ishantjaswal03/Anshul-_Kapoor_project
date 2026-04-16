from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
from functools import wraps
from flask_cors import CORS
import pandas as pd
import json
import secrets
import os
from predictive_model import PredictiveMaintenanceModel

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Allow CORS for Next.js app (usually running on port 3000)
CORS(app)

# Initialize ML Model
model = PredictiveMaintenanceModel()
model.load_model()

# Helper Functions
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

USER_DB_FILE = 'users.json'

def save_users(users):
    with open(USER_DB_FILE, 'w') as f:
        json.dump(users, f)

def load_users():
    if not os.path.exists(USER_DB_FILE):
        save_users({"admin": {"password": "adminpassword", "plan": "free"}})
        
    with open(USER_DB_FILE, 'r') as f:
        users = json.load(f)
        
    return users

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.is_json:
            data = request.json
            username = data.get('username')
            password = data.get('password')
        else:
            username = request.form.get('username')
            password = request.form.get('password')
            
        users = load_users()
        
        if username in users and users[username]["password"] == password:
            session['logged_in'] = True
            session['username'] = username
            if request.is_json:
                return jsonify({"status": "success", "redirect": url_for('index')})
            return redirect(url_for('index'))
            
        else:
            if request.is_json:
                return jsonify({"status": "error", "message": "Invalid Credentials"}), 401
            flash('Invalid Credentials', 'error')
            
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"status": "error", "message": "Username and password required"}), 400
        
    users = load_users()
    if username in users:
        return jsonify({"status": "error", "message": "User already exists"}), 400
        
    users[username] = {"password": password, "plan": "free"}
    save_users(users)
    
    session['logged_in'] = True
    session['username'] = username
    return jsonify({"status": "success", "redirect": url_for('index')})

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    users = load_users()
    plan = users.get(session['username'], {}).get('plan', 'free')
    return render_template('index.html', plan=plan)

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    try:
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400
            
        processed_data = {
            "machine_id": str(data.get("machine_id", "M001")),
            "temperature": float(data.get("temperature", 70.0)),
            "vibration": float(data.get("vibration", 2.0)),
            "pressure": float(data.get("pressure", 100.0)),
            "rpm": float(data.get("rpm", 1500.0)),
            "power_consumption": float(data.get("power_consumption", 50.0)),
            "cycle_count": int(data.get("cycle_count", 3000)),
            "operating_hours": int(data.get("operating_hours", 1000))
        }

        df = pd.DataFrame([processed_data])
        fail, prob, anomaly = model.predict(df)
        
        return jsonify({
            "status": "success",
            "failure_likely": bool(fail[0] == 1),
            "failure_probability": float(prob[0]),
            "anomaly_detected": bool(anomaly[0] == -1)
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/train', methods=['POST'])
@login_required
def train():
    try:
        model.train()
        return jsonify({"status": "success", "message": "Model retrained successfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
