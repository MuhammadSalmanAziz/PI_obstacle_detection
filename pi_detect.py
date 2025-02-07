import RPi.GPIO as GPIO
import time

# GPIO mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# Set GPIO Pins
GPIO_TRIGGER = 23
GPIO_ECHO = 24
GPIO_BUZZER = 18

# Set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_BUZZER, GPIO.OUT)

def distance():
    # Set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
    
    # Set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    
    # Save StartTime
    StartTime = time.time()
    StopTime = time.time()
    
    # Save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    
    # Save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    
    # Time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # Multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    
    return distance

def alert_user():
    GPIO.output(GPIO_BUZZER, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(GPIO_BUZZER, GPIO.LOW)
    time.sleep(0.1)

if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            if dist < 30:  # Distance threshold in cm
                alert_user()
            time.sleep(1)
            
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
