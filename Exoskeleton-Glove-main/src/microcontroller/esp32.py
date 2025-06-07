import socket
import network
from machine import I2C, Pin
from time import sleep_ms
from pca9685 import PCA9685

# ============================
# WiFi Setup
# ============================

# Connect to a WiFi network using SSID and password
ssid = 'Prajwal'
password = 'nicemice'
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

# Wait until connected
if not sta_if.isconnected():
    sta_if.connect(ssid, password)
    while not sta_if.isconnected():
        pass

print('Connected, IP:', sta_if.ifconfig()[0])

# ============================
# I2C and PCA9685 Setup
# ============================

# Initialize I2C on pins 21 (SDA) and 22 (SCL)
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

# Initialize PCA9685 PWM controller
pca = PCA9685(i2c)
pca.freq(50)  # Set frequency for servo motors (usually 50Hz)

# ============================
# Servo Control Function
# ============================

# Convert angle to PWM duty and set servo position
def set_servo_angle(channel, angle):
    min_pulse = 1000  # microseconds
    max_pulse = 2000
    pulse = int(min_pulse + (max_pulse - min_pulse) * angle / 180)
    duty = int(pulse * 4096 / 20000)  # Convert pulse width to duty cycle
    pca.duty(channel, duty)

# Smoothly move servo from current to target angle in steps
def smooth_step(channel, current, target, step):
    while current != target:
        if current < target:
            current += step
            current = min(current, target)
        elif current > target:
            current -= step
            current = max(current, target)
        set_servo_angle(channel, current)
        sleep_ms(20)  # Small delay between steps
    return current

# ============================
# Rolling Average Function
# ============================

# Maintain a rolling average over a fixed number of values
def update_rolling_average(buffer, new_val, size=10):
    buffer.append(new_val)
    if len(buffer) > size:
        buffer.pop(0)
    return sum(buffer) / len(buffer)

# ============================
# Joint Configuration
# ============================

# Define joint configurations with control channels, angles, and movement parameters
joints = {
    11: {'name': 'thumb',  'channel': 0, 'threshold': 45, 'min': -40,   'max': 60,  'step': 10},
    1:  {'name': 'index',  'channel': 2, 'threshold': 45, 'min': 25,    'max': -120, 'step': -14},
    4:  {'name': 'middle', 'channel': 4, 'threshold': 45, 'min': 300,   'max': 120, 'step': -18},
    7:  {'name': 'ring',   'channel': 6, 'threshold': 45, 'min': 130,   'max': 300, 'step': 17},
    10: {'name': 'pinky',  'channel': 8, 'threshold': 45, 'min': 220,   'max': -100, 'step': -32}
}

# ============================
# State Tracking for Each Joint
# ============================

# Maintain calibration data, recent values, and current position for each joint
joint_data = {
    j: {
        'init_vals': [],          # First 10 values for calibration
        'initial_avg': None,      # Average value used as baseline
        'recent_vals': [],        # Last N values for rolling average
        'moving_avg': None,       # Current rolling average
        'current_angle': joints[j]['min']  # Start at min position
    } for j in joints
}

# ============================
# Startup Movement Demo
# ============================

print("Running startup finger test...")
for j in joints:
    channel = joints[j]['channel']
    min_angle = joints[j]['min']
    max_angle = joints[j]['max']
    step = joints[j]['step']
    
    # Move finger to max and back to min position
    print(f"{joints[j]['name']} going to MAX...")
    smooth_step(channel, min_angle, max_angle, step)
    sleep_ms(500)
    
    print(f"{joints[j]['name']} returning to MIN...")
    smooth_step(channel, max_angle, min_angle, step)
    
    joint_data[j]['current_angle'] = min_angle
    sleep_ms(200)

print("Demo complete. Starting calibration and control...")

# ============================
# UDP Server Setup
# ============================

# Listen for UDP messages on port 8888
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(('0.0.0.0', 8888))
print("UDP Server listening on port 8888...")

# ============================
# Main Loop: Calibration + Control
# ============================

while True:
    data, addr = udp.recvfrom(1024)  # Receive UDP packet
    msg = data.decode().strip()
    print(f"Received: {msg}")

    try:
        # Parse the incoming message
        joint_str, angle_str = msg.split(" ")
        joint = int(joint_str)
        received_angle = int(angle_str)

        # Process only if it's a valid joint
        if joint in joints:
            jd = joint_data[joint]     # Joint-specific data
            ji = joints[joint]         # Joint config

            # Extract relevant joint properties
            channel = ji['channel']
            threshold = ji['threshold']
            name = ji['name']
            min_angle = ji['min']
            max_angle = ji['max']
            step = ji['step']

            # === Calibration Phase ===
            if jd['initial_avg'] is None:
                jd['init_vals'].append(received_angle)
                print(f"[{name}] Calibrating: {len(jd['init_vals'])}/10")
                
                # Once 10 values are received, set calibration average
                if len(jd['init_vals']) == 10:
                    jd['initial_avg'] = sum(jd['init_vals']) / 10
                    print(f"[{name}] Calibration done. Initial Avg: {jd['initial_avg']:.2f}")
                    
                    # Return joint to starting position
                    jd['current_angle'] = smooth_step(channel, jd['current_angle'], min_angle, step)
            else:
                # === Post-Calibration: Rolling Average Movement Control ===
                moving_avg = update_rolling_average(jd['recent_vals'], received_angle, size=10)
                jd['moving_avg'] = moving_avg

                # Calculate deviation from baseline
                diff = moving_avg - jd['initial_avg']
                print(f"[{name}] Δ = {diff:.2f} (MovingAvg: {moving_avg:.2f}, CalibAvg: {jd['initial_avg']:.2f})")

                # If change exceeds threshold, move the joint
                if abs(diff) > threshold:
                    target = max_angle if diff > 0 else min_angle
                    if jd['current_angle'] != target:
                        jd['current_angle'] = smooth_step(channel, jd['current_angle'], target, step)
                        print(f"[{name}] Moving to {jd['current_angle']}")
                    else:
                        print(f"[{name}] Already at target.")
                else:
                    print(f"[{name}] Within threshold. No move.")
        else:
            print("Unknown joint number.")

    except Exception as e:
        print("Invalid message format or error:", e)
