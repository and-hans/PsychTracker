import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# Define your button pins as a tuple
button_pins = (27, 17, 4, 2, 3)

# Set up the button pins as inputs with pull-up resistors
for pin in button_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

# Add event listeners for each button using a for loop
for pin in button_pins:
    GPIO.add_event_detect(pin, GPIO.FALLING, callback=btn_callback, bouncetime=200)

try:
    print("Waiting for button presses...")
    while True:
        pass

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()