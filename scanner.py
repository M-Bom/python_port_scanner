import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
import time

def scan_port(target: str, port: int, timeout: float = 1.0):
    """
    Scan a single port on the target host.
    
    Returns True if the port is open, False otherwise.
    """
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Set a timeout to prevent exit if host or ports are unreachable
    sock.settimeout(timeout)

    # Attempt to connect to the target port
    # if connection succesful return 0
    try:
        result = sock.connect_ex((target, port))
        return result == 0
    # If the connection is fails return false
    except:
        return False
    # Close TCP socket
    finally:
        sock.close()
