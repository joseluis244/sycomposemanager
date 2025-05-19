import os
import subprocess
import sys, traceback, json
from compose_utils import init_compose,restart_compose,start_compose,stop_compose,up_compose
from flask import Flask, send_file, request

app = Flask(__name__)

@app.route("/")
def index():
    return send_file('src/index.html')

@app.route("/create", methods=['POST'])
def create():
    try:
        data = request.get_json()
        institution_name = data.get('institutionName')
        compose_file_path = init_compose(institution_name)
        up_compose(compose_file_path)
        return f"Institution {institution_name} initialized with compose file"
    except Exception as e:
        return str(traceback.format_exc()), 500
@app.route("/restart", methods=['POST'])
def restart():
    try:
        data = request.get_json()
        compose_file_path = data.get('composepath')
        restart_compose(compose_file_path)
        return "restart compose"
    except Exception as e:
        return str(traceback.format_exc()), 500

@app.route("/start", methods=['POST'])
def start():
    try:
        data = request.get_json()
        compose_file_path = data.get('composepath')
        start_compose(compose_file_path)
        return "start compose"
    except Exception as e:
        return str(traceback.format_exc()), 500

@app.route("/stop", methods=['POST'])
def stop():
    try:
        data = request.get_json()
        compose_file_path = data.get('composepath')
        stop_compose(compose_file_path)
        return "stop compose"
    except Exception as e:
        return str(traceback.format_exc()), 500

def main():
  app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    main()
