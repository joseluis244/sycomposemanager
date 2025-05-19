import socket

def is_port_free(port):
    """Checks if a given port is free."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return True
        except OSError:
            return False

def port_analizer():
    """
    Analyzes and finds free ports for predefined services.

    Returns:
        dict: A dictionary containing the free ports for DICOM, MYSQL, HTTP, MONGO, and APP.
    """
    DICOM_PORT = 3101
    MYSQL_PORT = 3306
    HTTP_PORT = 8042
    MONGO_PORT = 27017
    APP_PORT = 4000

    ports = {
        "DICOM_PORT": DICOM_PORT,
        "MYSQL_PORT": MYSQL_PORT,
        "HTTP_PORT": HTTP_PORT,
        "MONGO_PORT": MONGO_PORT,
        "APP_PORT": APP_PORT
    }

    free_ports = {}

    for name, port in ports.items():
        current_port = port
        while not is_port_free(current_port):
            current_port += 1
        free_ports[name] = current_port

    return free_ports

if __name__ == '__main__':
    free_ports = port_analizer()
    print("Free ports found:")
    for name, port in free_ports.items():
        print(f"{name}: {port}")