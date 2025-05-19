import os
import subprocess
import sys, traceback, json
from compose_utils import init_compose
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
        init_compose(institution_name)
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

def restart_compose(compose_file_path):
    """Restarts a docker-compose file.

    Args:
        compose_file_path: The path to the docker-compose file.
    """
    if not os.path.exists(compose_file_path):
      raise FileNotFoundError(f"Docker-compose file not found: {compose_file_path}")
    subprocess.run(["docker", "compose", "-f", compose_file_path, "restart"], check=True)

def start_compose(compose_file_path):
    """Starts the services defined in a docker-compose file.

    Args:
        compose_file_path: The path to the docker-compose file.
    """
    if not os.path.exists(compose_file_path):
        raise FileNotFoundError(f"Docker-compose file not found: {compose_file_path}")
    subprocess.run(["docker", "compose", "-f", compose_file_path, "start"], check=True)

def stop_compose(compose_file_path):
    """Stops a docker-compose file.

    Args:
        compose_file_path: The path to the docker-compose file.
    """
    if not os.path.exists(compose_file_path):
        raise FileNotFoundError(f"Docker-compose file not found: {compose_file_path}")
    subprocess.run(["docker", "compose", "-f", compose_file_path, "stop"], check=True)

def main():
  app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    main()
