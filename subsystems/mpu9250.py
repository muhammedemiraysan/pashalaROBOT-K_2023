import pyfirmata
class MPU9250:
    def __init__(self, i2c_addr=0x68):
        self.i2c_addr = i2c_addr
        self.i2c = None
    def connect(self):
        from arduino import board
        # Connect to Arduino board
        boardd = board()
        board = boardd.arduinoMega

        # Define I2C object and configure it
        self.i2c = board.get_i2c_device(self.i2c_addr)
        self.i2c.write(bytes([0x6B, 0]))  # Wake up MPU9250

    def get_accel_data(self):
        if not self.i2c:
            raise Exception("MPU9250 is not connected.")

        # Read accelerometer data from MPU9250
        accel_x_msb = self.i2c.read(0x3B, 1)[0]
        accel_x_lsb = self.i2c.read(0x3C, 1)[0]
        accel_y_msb = self.i2c.read(0x3D, 1)[0]
        accel_y_lsb = self.i2c.read(0x3E, 1)[0]
        accel_z_msb = self.i2c.read(0x3F, 1)[0]
        accel_z_lsb = self.i2c.read(0x40, 1)[0]

        # Convert accelerometer data to signed integers
        accel_x = self._convert_to_int(accel_x_msb, accel_x_lsb)
        accel_y = self._convert_to_int(accel_y_msb, accel_y_lsb)
        accel_z = self._convert_to_int(accel_z_msb, accel_z_lsb)

        return accel_x, accel_y, accel_z

    @staticmethod
    def _convert_to_int(msb, lsb):
        val = (msb << 8) | lsb
        if val >= 32768:
            val = -((65535 - val) + 1)
        return val