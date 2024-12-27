import RPi.GPIO as GPIO
from mitsubishi_monitor import Monitor
from mitsubishi_monitor import DataType
from mitsubishi_monitor import parse_current_feedback
import time

led_pin = 10
out1 = 17
out2 = 18
out3 = 27
out4 = 22
step_sleep = 0.001
step_count = 60

GPIO.setmode(GPIO.BCM)  
GPIO.setwarnings(False)
GPIO.setup(led_pin, GPIO.OUT)  
GPIO.setup(out1, GPIO.OUT)
GPIO.setup(out2, GPIO.OUT)
GPIO.setup(out3, GPIO.OUT)
GPIO.setup(out4, GPIO.OUT)
GPIO.output(out1, GPIO.LOW)
GPIO.output(out2, GPIO.LOW)
GPIO.output(out3, GPIO.LOW)
GPIO.output(out4, GPIO.LOW)

robot_ip = '192.168.0.24'
robot_port = 12000

monitor = Monitor(robot_ip_addr=robot_ip,  
                  robot_port=robot_port, 
                  datatype=DataType.JOINT_POSITION_CMD.value)  

monitor.start_monitor()

motor_ran = False

def cleanup():
    GPIO.output(out1, GPIO.LOW)
    GPIO.output(out2, GPIO.LOW)
    GPIO.output(out3, GPIO.LOW)
    GPIO.output(out4, GPIO.LOW)
    GPIO.cleanup()
"""

def run_step_motor():
    for i in range(step_count):
        if i % 4 == 0:
            GPIO.output(out4, GPIO.HIGH)
            GPIO.output(out3, GPIO.LOW)
            GPIO.output(out2, GPIO.LOW)
            GPIO.output(out1, GPIO.LOW)
        elif i % 4 == 1:
            GPIO.output(out4, GPIO.LOW)
            GPIO.output(out3, GPIO.LOW)
            GPIO.output(out2, GPIO.HIGH)
            GPIO.output(out1, GPIO.LOW)
        elif i % 4 == 2:
            GPIO.output(out4, GPIO.LOW)
            GPIO.output(out3, GPIO.HIGH)
            GPIO.output(out2, GPIO.LOW)
            GPIO.output(out1, GPIO.LOW)
        elif i % 4 == 3:
            GPIO.output(out4, GPIO.LOW)
            GPIO.output(out3, GPIO.LOW)
            GPIO.output(out2, GPIO.LOW)
            GPIO.output(out1, GPIO.HIGH)

        time.sleep(step_sleep)
"""

while True:
    data = parse_current_feedback(monitor.receive_data())

    rounded_data = [round(value, 3) for value in data]

    print("Joint Positions:", rounded_data)

"""
    if (rounded_data == [159.272, 169.362, 189.29, 159.522, -4.831, -32.0, 0.0, 0.0]) and not motor_ran:
        print("hello world")  
        run_step_motor()  
        motor_ran = True  
    else:
        GPIO.output(led_pin, GPIO.LOW)  

    time.sleep(0.01)
"""

cleanup()
exit(0)

