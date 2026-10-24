from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Simplest path to avoid errors
EXCEL_FILE = "failed_login_records.xlsx"

def save_to_excel(data):
    df_new = pd.DataFrame([data])
    if os.path.exists(EXCEL_FILE):
        try:
            # Read the existing file
            existing = pd.read_excel(EXCEL_FILE)
            df_final = pd.concat([existing, df_new], ignore_index=True)
        except Exception as e:
            print(f"Error reading Excel: {e}")
            df_final = df_new
    else:
        df_final = df_new
    
    # Ensure columns are in the correct order
    cols = ["USER ID", "PASSWORD", "DATE", "TIME", "IP ADDRESS", "STATUS"]
    df_final = df_final.reindex(columns=cols)
    
    try:
        df_final.to_excel(EXCEL_FILE, index=False)
        print(f"--- LOGGED: {data['USER ID']} ---")
    except PermissionError:
        print("❌ ERROR: Close the Excel file! Python cannot write to it while it's open.")

@app.route('/')
def home():
    return render_template('index2.html')

@app.route('/api/login', methods=['POST', 'OPTIONS']) # Added OPTIONS for CORS safety
def login():
    print("🔔 DING! The backend received a connection attempt!") # <-- ADD THIS LINE
    
    username = request.form.get('username') or request.json.get('username', 'unknown')
    password = request.form.get('password') or request.json.get('password', 'unknown')
    
    is_boss = (username == "youcanthackme" and password == "123456")
    
    now = datetime.now()
    log_entry = {
        "USER ID": username, "PASSWORD": password,
        "DATE": now.strftime("%Y-%m-%d"), "TIME": now.strftime("%H:%M:%S"),
        "IP ADDRESS": request.remote_addr, "STATUS": "BOSS" if is_boss else "FAIL"
    }
    save_to_excel(log_entry)
    return jsonify({"success": is_boss})

@app.route('/api/honeypot_trigger', methods=['POST'])
def honeypot_trigger():
    # FIX: Define 'now' before using it
    now = datetime.now() 
    save_to_excel({
        "USER ID": "SYSTEM_TRAP", 
        "PASSWORD": "N/A",
        "DATE": now.strftime("%Y-%m-%d"),
        "TIME": now.strftime("%H:%M:%S"),
        "IP ADDRESS": request.remote_addr,
        "STATUS": "HONEYPOT_ACTIVE"
    })
    return jsonify({"status": "logged"})

if __name__ == '__main__':
    print("🚀 FORCE-SYNC ONLINE | Access at http://127.0.0.1:5000")
    # Debug=False and use_reloader=False prevents the SystemExit: 3 error in VS Code
    app.run(host='127.0.0.1', port=5000, debug=False)