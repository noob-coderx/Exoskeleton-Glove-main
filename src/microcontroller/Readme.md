# Raspberry Pi Pico W ADC MUX Communication

This project uses a **Raspberry Pi Pico W** to:
- Connect to a Wi-Fi network.
- Read analog values from two 16-channel multiplexers (MUX).
- Send these values over UDP to a laptop in real time.

The source code reads from either MUX1 or MUX2 using GPIO and ADC pins. It selects channels using S0-S3 pins and reads the analog voltage using onboard ADCs. It transmits each channel's analog reading over a UDP socket to a specified IP and port.

---

## Microcontroller Model

**Raspberry Pi Pico W**

---

## IDE Used

**Thonny IDE** (Recommended for MicroPython development)

---

## Upload and Run Instructions

### Prerequisites

1. Install **Thonny IDE** from: https://thonny.org  
2. Ensure **MicroPython firmware** is installed on your Raspberry Pi Pico W.
3. Connect your Pico W via USB.

###  Uploading the Code

1. Open Thonny.
2. Set the interpreter:  
   `Tools > Options > Interpreter > MicroPython (Raspberry Pi Pico)`
3. Paste the script into Thonny.
4. Replace:
   - `SSID` with your Wi-Fi network name.
   - `PASSWORD` with your Wi-Fi password.
   - `LAPTOP_IP` with your laptop’s IP address.
5. Click **Run (▶️)** to execute the script on the Pico W.


##  Notes

- The Pico W will print its IP address once connected to Wi-Fi.
- It loops over analog channels and transmits the value over UDP port `5005`.
- To receive data on the laptop, you can use a UDP socket script in Python or software like netcat.

---

Modifications:
- Configured GPIO and ADC pins for 2 MUX units.
- Implemented UDP communication for real-time analog data transfer.
- Optimized loop with delay for stable channel switching.

# ESP32-Based Servo Motor Control via UDP

This project enables real-time control of servo motors using joint angle data received over UDP. An ESP32 board connects to Wi-Fi and receives lower joint angles from a laptop. These angles are used to drive corresponding servo motors via a PCA9685 driver, enabling gesture replication or robotic hand motion.

## Features

- Wi-Fi-based UDP communication
- Real-time servo actuation
- Automatic joint calibration
- Rolling average filtering for noise reduction
- Smooth motor transitions to prevent jerks

## Hardware Required

- ESP32 Development Board  
- PCA9685 PWM Driver  
- Servo Motors  
- External 5V Power Supply  
- Connecting wires

## Communication Protocol

- **Format:** `<joint_number> <angle_value>` (e.g., `1 120`)  
- **Port:** 8888 (UDP)  
- **Sender:** Laptop or external device
