import subprocess
import os

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
    env_content = env_content.replace("{{pacs_name}}", pacs_count)
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

if __name__ == '__main__':
    # Example usage:
    init_compose("MyAwesomeInstitution")