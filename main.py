import time
class Main:
    def __init__(self):
        pass
    
    def robot_init(self):
        from subsystems.controller import JoystickController
        from subsystems.drive import drivee
        from subsystems.camera import cam
        from subsystems.mpu9250 import MPU9250
        from subsystems.pid import PIDController
        from subsystems.autonomus import autonomus
        self.drive = drivee()
        self.controller = JoystickController()
        self.cam = cam()
        self.mpu9250 = MPU9250()
        self.autonomous = autonomus()
        self.pid = PIDController(1,1,1,1)

        self.drive.calibrate()
        
    def robot_periodic(self):
        #self.drive.joystickdrive()
        self.cam.ShowCamera()

if __name__ == "__main__":
    main = Main()
    main.robot_init()
    while True:
        main.robot_periodic()
        time.sleep(0.02) # Add a small delay to reduce CPU usage