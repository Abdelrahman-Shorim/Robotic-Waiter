import socket

# ESP-WROOM-32 IP address and port
host = '192.168.76.6'  # Replace with the actual IP address of your ESP-WROOM-32
port = 80

# Function to send data to the ESP-WROOM-32 server
def send_data(data):
    try:
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the ESP-WROOM-32 server
        client_socket.connect((host, port))

        # Send data to the server
        client_socket.sendall(data.encode() + b'\n')

        # Receive response from the server
        response = client_socket.recv(1024)
        print("Response from ESP-WROOM-32:", response.decode())

        # Close the connection
        client_socket.close()
    except Exception as e:
        print(f"Failed to send/receive data: {e}")

# Main function
if __name__ == "__main__":
    while True:
        # Get input data from the user
        data_to_send = input("Enter data to send: ")

        # Send data to the ESP-WROOM-32 server and receive response
        send_data(data_to_send)