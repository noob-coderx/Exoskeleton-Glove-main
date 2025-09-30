import network  # This is the library for network connections
import socket   # This is the library for UDP communication
import time    # This is the library for time-related functions
from machine import Pin, ADC    # This is the library for GPIO and ADC functions
SSID = "SSID" # Replace with your Wi-Fi SSID
PASSWORD ="password"    # Replace with your Wi-Fi password
wlan = network.WLAN(network.STA_IF)   # Create a WLAN object for station mode
wlan.active(True)    # Activate the WLAN interface
wlan.connect(SSID, PASSWORD)   # Connect to the Wi-Fi network
while not wlan.isconnected():    # Wait for the connection to be established
    print("Connecting to Wi-Fi...")    # Print a message while connecting
    time.sleep(1)    # Sleep for 1 second to avoid busy waiting
print("Connected! Pico W IP:", wlan.ifconfig()[0])   # Print the IP address of the Pico W
# Set up UDP communication
LAPTOP_IP = "192.168.239.106" # Replace with your laptop's IP address   
UDP_PORT = 5005  # Port for Raspberry Pi to send data
# Create a UDP socket for sending data to the laptop
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # Create a UDP socket for sending data to the laptop
m2_s0 = Pin(2, Pin.OUT) # Pin for MUX 2 S0
m2_s1 = Pin(3, Pin.OUT) # Pin for MUX 2 S1
m2_s2 = Pin(4, Pin.OUT) # Pin for MUX 2 S2
m2_s3 = Pin(5, Pin.OUT)     # Pin for MUX 2 S3
m1_s3 = Pin(18, Pin.OUT) # Pin for MUX 1 S3
m1_s2 = Pin(19, Pin.OUT)    # Pin for MUX 1 S2
m1_s1 = Pin(20, Pin.OUT)    # Pin for MUX 1 S1
m1_s0 = Pin(21, Pin.OUT)        # Pin for MUX 1 S0
mux1 = ADC(Pin(27)) # ADC for MUX 1
mux2 = ADC(Pin(28)) # ADC for MUX 2
number2 = 4 # Start with the first channel of MUX 1
# Function to set the MUX channel
try:              # Infinite loop to keep the program running
    while True:  # Loop to continuously read data from the MUX and send it to the laptop
        if number2 <= 16 :  # Check if the channel number is less than or equal to 16
            number = number2    # Calculating binary of number2
            s3 = number//8     # Calculate the value for S3
            number = number % 8   # Update the number for the next calculation
            s2 = number//4     # Calculate the value for S2
            number = number % 4     # Update the number for the next calculation
            s1 = number//2   # Calculate the value for S1
            s0 = number%2  # Calculate the value for S0
            m1_s0.value(s0) # Set the value for S0 of MUX 1
            m1_s1.value(s1) # Set the value for S1 of MUX 1
            m1_s2.value(s2) # Set the value for S2 of MUX 1 
            m1_s3.value(s3) # Set the value for S3 of MUX 1
            time.sleep(0.01) # Sleep for 10 milliseconds to allow the MUX to switch channels
            analog_value = mux1.read_u16() # Read the analog value from MUX 1
            message = f"{number2 - 4} " +f"{analog_value}" # Create the message to send to the laptop
            sock.sendto(message.encode(), (LAPTOP_IP, UDP_PORT)) # Send the message to the laptop
            print(f"Sent: {message}") # Print the sent message for debugging
        else : # If the channel number is greater than 16, switch to MUX 2
            number = number2 - 12 # Calculate the channel number for MUX 2
            s3 = number//8   # Calculate the value for S3
            number = number % 8  # Update the number for the next calculation
            s2 = number//4 # Calculate the value for S2
            number = number % 4     # Update the number for the next calculation
            s1 = number//2 # Calculate the value for S1
            s0 = number%2 # Calculate the value for S0
            m2_s0.value(s0) # Set the value for S0 of MUX 2
            m2_s1.value(s1)     # Set the value for S1 of MUX 2
            m2_s2.value(s2)     # Set the value for S2 of MUX 2
            m2_s3.value(s3 )     # Set the value for S3 of MUX 2
            time.sleep(0.01) # Sleep for 10 milliseconds to allow the MUX to switch channels
            analog_value = mux2.read_u16() # Read the analog value from MUX 2
            message = f"{number2 - 4} " +f"{analog_value}" # Create the message to send to the laptop
            sock.sendto(message.encode(), (LAPTOP_IP, UDP_PORT)) # Send the message to the laptop
            print(f"Sent: {message}") # Print the sent message for debugging
        if(number2 == 15): # If the channel number is 15, switch to MUX 2
          number2 = 4 # Reset the channel number to 4
        else: # If the channel number is not 15, increment it by 1
          number2 = number2 + 1 # Increment the channel number by 1
except KeyboardInterrupt:    # Handle keyboard interrupt (Ctrl+C) to stop the program gracefully
    print("Stopping...") # Print a message indicating that the program is stopping