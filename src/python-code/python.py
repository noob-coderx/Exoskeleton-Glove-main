import socket #this is for UDP communication
from collections import defaultdict, deque #this is for storing sensor data and calculating moving average

RPI_PORT = 5005 # Port for Raspberry Pi to send data
UNITY_PORT = 12345 # Port for Unity to receive data
UNITY_IP = "127.0.0.1" # IP address of the Unity application (localhost in this case)
# Create a UDP socket for receiving data from Raspberry Pi

recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create a UDP socket for receiving data from Raspberry Pi
recv_sock.bind(("0.0.0.0", RPI_PORT)) # Bind to all interfaces on the specified port

send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create a UDP socket for sending data to Unity

# Maintain a deque for each sensor ID
sensor_data = defaultdict(lambda: deque(maxlen=2)) # Use deque with a maxlen of 2 to keep the last two values for moving average
# This will help in calculating the moving average

print(f"Listening for Raspberry Pi data on port {RPI_PORT}...")  # Print a message indicating that the server is listening for data
# Loop to receive data from Raspberry Pi and forward it to Unity

while True: # Infinite loop to keep the server running and listening for data
    # Receive data from Raspberry Pi        
    data, addr = recv_sock.recvfrom(1024)
    message = data.decode().strip() # Decode the received data and strip any whitespace  

    try:  # Try to process the message
        sensor_id_str, value_str = message.split()  # Split the message into sensor ID and value
        sensor_id = int(sensor_id_str) # Convert sensor ID to integer
        value = int(value_str) # Convert value to integers

        # Update moving average buffer
        sensor_data[sensor_id].append(value) # Append the new value to the deque for the sensor ID
        # Check if we have enough data to compute the moving average

        average_value = sum(sensor_data[sensor_id]) // len(sensor_data[sensor_id]) # Calculate the moving average

        averaged_message = f"{sensor_id} {average_value}" # Create the averaged message to send to Unity
        send_sock.sendto(averaged_message.encode(), (UNITY_IP, UNITY_PORT)) # Send the averaged message to Unity
        print(f"Forwarded to Unity (avg): {averaged_message}") # Print the forwarded message for debugging

    except ValueError:  # Handle the case where the message format is incorrect
        print(f"Invalid message received: {message}")   # Print an error message if the message format is incorrect
