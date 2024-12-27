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
step_sleep = 0.0008
step_count = 75

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

led_pwm = GPIO.PWM(led_pin, 100)
led_pwm.start(0)  

robot_ip = '192.168.0.24'
robot_port = 12000

monitor = Monitor(robot_ip_addr=robot_ip, 
                  robot_port=robot_port, 
                  datatype=DataType.JOINT_POSITION_CMD.value)  

monitor.start_monitor()
print("Monitoring is started")

def cleanup():
    led_pwm.stop() 
    GPIO.output(out1, GPIO.LOW)
    GPIO.output(out2, GPIO.LOW)
    GPIO.output(out3, GPIO.LOW)
    GPIO.output(out4, GPIO.LOW)
    GPIO.cleanup()

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

positions = {
    
    (67.694, 58.938, 41.408, -0.223, 94.43, 32.0, 0.0, 0.0):False,
    (60.145, 46.28, 113.866, -0.395, 112.733, 32.0, 0.0, 0.0):False,
    (114.549, 73.829, 125.423, -0.305, 121.51, 32.0, 0.0, 0.0):False,
    (64.328,125.222,106.26,-0.305,119.936,32.0,0.0,0.0):False,
    (106.176,77.786,79.29,-0.39,66.157,32.0,0.0,0.0):False,
    (88.09, 60.102, 39.229, -0.234, 84.219,32.0,0.0,0.0):False
    
}

try:
    while True:
        data = parse_current_feedback(monitor.receive_data())

        rounded_data = tuple(round(value, 3) for value in data)

        
        if rounded_data in positions:
            if not positions[rounded_data]:
                print(f"Position detected: {rounded_data}")
                run_step_motor()
                positions[rounded_data] = True
            
            led_pwm.ChangeDutyCycle(100)
        else:
            led_pwm.ChangeDutyCycle(0)

        time.sleep(0.01)  

except KeyboardInterrupt:
    print("\nFinished")
    cleanup()
    exit(0)


