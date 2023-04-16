from pyfirmata import Arduino, SERVO
import serial.tools.list_ports
import time
class board:
    def __init__(self) -> None:
        pass

    def find_arduino_port(self):
        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(ports):
            if 'arduino' in desc.lower():
                print("A")
                return port      
        return None
    
    def arduino_connect(self):
        from subsystems.drive import drivee
        self.drive = drivee()
        self.arduinoMega = Arduino("COM4")

    def set_arduino_pins(self):
        motorPins = self.drive.motors
        self.arduinoMega.digital[motorPins['Sol_Arka']].mode = SERVO
        self.arduinoMega.digital[motorPins['Sol_On']].mode = SERVO
        self.arduinoMega.digital[motorPins['Sag_On']].mode = SERVO
        self.arduinoMega.digital[motorPins['Sag_Arka']].mode = SERVO
        self.arduinoMega.digital[motorPins['Sol_On_UST']].mode = SERVO
        self.arduinoMega.digital[motorPins['Sag_On_UST']].mode = SERVO
        self.arduinoMega.digital[motorPins['Sol_Arka_UST']].mode = SERVO
        self.arduinoMega.digital[motorPins['Sag_Arka_UST']].mode = SERVO

    def set_pwm(self,motor,Angle):
        self.arduinoMega.digital[motor].write(1500+Angle)