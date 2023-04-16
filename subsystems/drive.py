class drivee:
    def __init__(self):  
        self.JOYSTICK_MIN = -1.0
        self.JOYSTICK_MAX = 1.0
        self.ESC_MIN = -400
        self.ESC_MAX = 400
        self.motors = {
            'Sol_Arka': 3,
            'Sol_On': 3,
            'Sag_On': 3,
            'Sag_Arka': 3,
            'Sol_On_UST': 3,
            'Sol_Arka_UST': 3,
            'Sag_On_UST': 7,
            'Sag_Arka_UST': 3
        }

    def calibrate(self):
        from subsystems.controller import JoystickController
        from subsystems.arduino import board 
        self.boardd = board()     
        for motor in self.motors.values():
            self.boardd.arduino_connect()
            self.boardd.set_arduino_pins()
            self.boardd.set_pwm(motor, 0)
    
    def map_range(self,x,in_min, in_max, out_min, out_max):
            return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    
    def map_joystick_to_drone(self,joystick_value):
        drone_value = self.map_range(joystick_value, self.JOYSTICK_MIN, self.JOYSTICK_MAX, self.ESC_MIN, self.ESC_MAX)
        drone_value = int(round(drone_value))
        return drone_value
    
    def joystickdrive(self):
        from controller import JoystickController
        self.axis =  JoystickController.get_axes_values(self)

        y_axis = self.axis[0]
        x_axis = self.axis[1]
        z_axis = self.axis[2]

        rotation_axis = self.axis[3]
        forward_backward = self.map_joystick_to_drone(y_axis)
        left_right = self.map_joystick_to_drone(x_axis)
        up_down = self.map_joystick_to_drone(z_axis)
        rotation = self.map_joystick_to_drone(rotation_axis)

        self.boardd.set_pwm(self.motors['Sol_On'], forward_backward+left_right+rotation)
        self.boardd.set_pwm(self.motors['Sol_Arka'], forward_backward+left_right+rotation)
        self.boardd.set_pwm(self.motors['Sag_On'], forward_backward+left_right+rotation)
        self.boardd.set_pwm(self.motors['Sag_Arka'], forward_backward+left_right+rotation)
        self.boardd.set_pwm(self.motors['Sag_On_UST'], up_down)
        self.boardd.set_pwm(self.motors['Sag_Arka_UST'], up_down)
        self.boardd.set_pwm(self.motors['Sol_On_UST'], up_down)
        self.boardd.set_pwm(self.motors['Sol_Arka_UST'], up_down)