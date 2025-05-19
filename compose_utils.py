import subprocess
import os

from port_utils import port_analizer
def init_compose(institution_name: str):
    """
    Initializes directories and configuration for a new institution.

    Args:
        institution_name: The name of the institution to be used in the compose file.
    """
    # Check and create /MedicareSoft/ directory if it doesn't exist
    medicaresoft_dir = "/MedicareSoft"
    if not os.path.exists(medicaresoft_dir):
        os.makedirs(medicaresoft_dir)

    # Count the number of directories inside /MedicareSoft/
    medicaresoft_subdirs = [name for name in os.listdir(medicaresoft_dir) if os.path.isdir(os.path.join(medicaresoft_dir, name))]
    pacs_count = f"Pacs{len(medicaresoft_subdirs) + 1}"

    # Analyze and get free ports
    free_ports = port_analizer()

    # Create required directories
    # Create the specific MedicareSoft directory for the new institution
    medicaresoft_institution_dir = os.path.join(medicaresoft_dir, pacs_count)
    os.makedirs(medicaresoft_institution_dir, exist_ok=True)
    compose_target_path = os.path.join(medicaresoft_institution_dir, "compose.yml")
    compose_template_path = "./template/template.yml"

    # Copy and modify the .env file
    env_template_path = "./template/env"
    env_target_path = os.path.join(medicaresoft_institution_dir, ".env")
    with open(env_template_path, 'r') as f:
        env_content = f.read()
    env_content = env_content.replace("{{pacs_name}}", pacs_count) # Keep this line if you still want pacs_count in the .env file
    env_content = env_content.replace("{{DICOM_PORT}}", str(free_ports['DICOM_PORT']))
    env_content = env_content.replace("{{MYSQL_PORT}}", str(free_ports['MYSQL_PORT']))
    env_content = env_content.replace("{{HTTP_PORT}}", str(free_ports['HTTP_PORT']))
    env_content = env_content.replace("{{MONGO_PORT}}", str(free_ports['MONGO_PORT']))
    env_content = env_content.replace("{{APP_PORT}}", str(free_ports['APP_PORT']))
    os.makedirs(f"/Symphony/{pacs_count}/DCM", exist_ok=True)
    os.makedirs(f"/Symphony/{pacs_count}/INF", exist_ok=True)
    os.makedirs(f"/Symphony/{pacs_count}/MYSQL", exist_ok=True)
    os.makedirs(f"/Symphony/{pacs_count}/MONGO", exist_ok=True)
    os.makedirs(f"/MedicareSoft/{pacs_count}/App", exist_ok=True)
    print(f"Directories created for institution: {pacs_count}") # Changed from institution_name

    with open(compose_template_path, 'r') as f:
        compose_content = f.read()
    with open(env_target_path, 'w') as f:
        f.write(env_content)

    # You might want to run docker-compose up -d here, but the prompt asked
    # to just initialize the file. If you need to run it, uncomment the following:
    # try:
    #     subprocess.run(["docker-compose", "-f", compose_file_path, "up", "-d"], check=True)
    #     print("Docker Compose project started.")
    # except subprocess.CalledProcessError as e:
    #     print(f"Error starting Docker Compose project: {e}")
    with open(compose_target_path, "w") as f:
        f.write(compose_content)
    print(f"compose.yml file created for institution: {pacs_count}")
    return compose_target_path

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

def up_compose(compose_file_path):
    """up a docker-compose file.

    Args:
        compose_file_path: The path to the docker-compose file.
    """
    if not os.path.exists(compose_file_path):
        raise FileNotFoundError(f"Docker-compose file not found: {compose_file_path}")
    subprocess.run(["docker", "compose", "-f", compose_file_path, "up","-d"], check=True)


if __name__ == '__main__':
    # Example usage:
    init_compose("MyAwesomeInstitution")