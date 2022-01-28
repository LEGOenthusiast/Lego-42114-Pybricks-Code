# Lego 42114 Volvo A60H
from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Port, Direction, Stop, Button, Color
from pybricks.tools import wait

# Initialize.
steer = Motor(Port.D)
drive = Motor(Port.A, Direction.COUNTERCLOCKWISE)
gearbox = Motor(Port.B, Direction.COUNTERCLOCKWISE)
hub = TechnicHub()
gear = 1
speed = 100
gearspeed = 700

# Connect to the remote.
remote = Remote()

def Cal_steer():
    steer.run_until_stalled(-200, duty_limit=90)
    steer.reset_angle(0)
    steer.run_until_stalled(200, duty_limit=90)
    angle = steer.angle()
    calib = angle/2
    print(calib)
    calib = float(calib)
    steer.run_angle(500, -calib)
    steer.reset_angle(0)
    steer.stop()

def Cal_gear():
    gearbox.run_until_stalled(-200, duty_limit=40)
    gearbox.reset_angle(0)
    gearbox.stop()

# Calibrate.
Cal_steer()
Cal_gear()

while True:
    # Check which buttons are pressed.
    pressed = remote.buttons.pressed()

    # If the left button and center button are pressed, shutdown the hub.
    if Button.LEFT in pressed and Button.CENTER in pressed:
        hub.system.shutdown()

    # If the right button and center button are pressed, recalibrate the motors.
    if Button.RIGHT in pressed and Button.CENTER in pressed:
        Cal_gear()
        Cal_steer()

    # Choose the steer angle based on the right controls.
    steer_angle = 0
    if Button.RIGHT_MINUS in pressed:
        steer_angle -= 62
    if Button.RIGHT_PLUS in pressed:
        steer_angle += 62

    # Steer to the selected angle.
    steer.run_target(500, steer_angle, wait=False)

    # Choose the drive speed based on the left controls.
    drive_speed = 0
    if Button.LEFT_PLUS in pressed:
        drive_speed += speed
    if Button.LEFT_MINUS in pressed:
        drive_speed -= speed

    # Select gear
    if Button.CENTER in pressed and gear == 4:
        gearbox.run_until_stalled(-gearspeed, duty_limit=40)
        gear = 1
    pressed = remote.buttons.pressed()
    if Button.CENTER in pressed:
        gearbox.run_target(gearspeed, 325)
        gear = 4
    if Button.RIGHT in pressed and gear == 2:
        gearbox.run_target(gearspeed, 225)
        gear = 3
    if Button.RIGHT in pressed and gear == 1:
        gearbox.run_target(gearspeed, 135)
        gear = 2
    if Button.LEFT in pressed and gear == 2:
        gearbox.run_until_stalled(-gearspeed, duty_limit=40)
        gear = 1
    if Button.LEFT in pressed and gear == 3:
        gearbox.run_target(gearspeed, 135)
        gear = 2
    if gear == 1:
        speed = 100
        remote.light.on(Color.ORANGE)
    if gear == 2:
        speed = 100
        remote.light.on(Color.YELLOW)
    if gear == 3:
        speed = 100
        remote.light.on(Color.GREEN)
    if gear == 4:
        speed = -100
        remote.light.on(Color.BLUE)

    # Apply the selected speed.
    drive.dc(drive_speed)
    wait(10)