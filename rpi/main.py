import RPi.GPIO as GPIO
import glob
import time
from time import sleep

GPIO.setmode(GPIO.BCM)

# Define your button pins as a tuple
button_pins = (27, 17, 4, 2, 3)
sensor_pin = 22
sleep_time = 10 # HOW MANY SECONDS TO READ THE DATA FOR 

# Set up the button pins as inputs with pull-up resistors
for pin in button_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Wait for initialization")

base_dir = '/sys/bus/w1/devices/'
while True:
    try:
        device_folder = glob.glob(base_dir + '28*')[0]
        break
    except IndexError:
        sleep(0.5)
        continue
device_file = device_folder + '/w1_slave'

# The function to read currently measurement at the sensor will be defined.
def input_temp():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

input_temp()

def temp_answer():
    lines = input_temp()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = input_temp()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
    return temp_c

def btn_callback(channel):
    if channel == button_pins[0]:
        print("Happy button pressed")
    elif channel == button_pins[1]:
        print("Neutral button pressed")
    elif channel == button_pins[2]:
        print("Sad button pressed")
    elif channel == button_pins[3]:
        print("Focus button pressed")
    elif channel == button_pins[4]:
        print("Distract button pressed")
    
    print(f"Pinch the temperature sensor for {sleep_time} seconds")
    try:
        for _ in range(sleep_time):
            print(f"Temperature: {temp_answer()}")
            time.sleep(1)

        print("Reading is done, you can release the temperature sensor")

    except KeyboardInterrupt:
        pass

def btn_callback_raise():
    pass

# Add event listeners for each button using a for loop
for pin in button_pins:
    print(pin)
    GPIO.add_event_detect(pin, GPIO.FALLING, callback=btn_callback, bouncetime=200)
    # GPIO.add_event_detect(pin, GPIO.RISING, callback=btn_callback_raise, bouncetime=200)

try:
    print("Waiting for button presses...")
    while True:
        pass

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
