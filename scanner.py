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

def scan_ports_threaded(target: str, ports: range, max_workers: int = 100):
    """
    Scan multiple ports using a thread pool.
    """
    open_ports = []
    start_time = time.time()

    # scan = partial(scan_port, target)

    # Start a scan for every port and keep track of which port belongs to which scan
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(scan_port, target, port): port for port in ports}

        # Get each scan result as they finish and then check if the result is valid
        # if yes add to open port list 
        for future in as_completed(futures):
            port = futures[future]
            try:
                if future.result():
                    open_ports.append(port)

            # Fail safe for if an erorr occurs to not abort the scan
            except:
                pass

    # Check how long the san took
    elapsed = time.time() - start_time
    print(f"\nScan completed in {elapsed:.2f} seconds")
    return open_ports
