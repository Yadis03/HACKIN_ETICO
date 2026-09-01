import psutil


def get_active_ports():
    """
    Retrieves active network connections and displays the ports
    currently in use along with their associated processes.
    """

    print("=" * 70)
    print("ACTIVE PORTS AND ASSOCIATED PROCESSES")
    print("=" * 70)

    # Get all network connections available on the system
    connections = psutil.net_connections(kind="inet")

    # Store displayed ports to prevent duplicate entries
    displayed_ports = set()

    for connection in connections:

        # Verify that the connection has a local address
        if not connection.laddr:
            continue

        # Get the local port currently being used
        local_port = connection.laddr.port

        # Create a unique identifier to avoid duplicate results
        port_key = (local_port, connection.pid)

        if port_key in displayed_ports:
            continue

        displayed_ports.add(port_key)

        # Determine the network protocol
        if connection.type == 1:
            protocol = "TCP"
        elif connection.type == 2:
            protocol = "UDP"
        else:
            protocol = "UNKNOWN"

        # Set a default process name
        process_name = "Unknown"

        # Retrieve process information when a PID is available
        if connection.pid:
            try:
                process = psutil.Process(connection.pid)
                process_name = process.name()
            except psutil.NoSuchProcess:
                process_name = "Process no longer exists"
            except psutil.AccessDenied:
                process_name = "Access denied"

        # Display the connection information
        print(f"\nPort: {local_port}")
        print(f"Protocol: {protocol}")
        print(f"PID: {connection.pid}")
        print(f"Process: {process_name}")
        print(f"Status: {connection.status}")


if __name__ == "__main__":
    """
    Program entry point.
    Executes the function that scans active ports and processes.
    """
    get_active_ports()