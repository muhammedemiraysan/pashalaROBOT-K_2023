#include <Wire.h>
#include "DHT.h"

#define GY521_ADDRESS 0x68
#define DHTPIN 2
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

float alpha = 0.5;  // Complementary filter constant

int16_t ax, ay, az, gx, gy, gz;
float accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  Wire.beginTransmission(GY521_ADDRESS);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);
  dht.begin();
}

void loop() {
  // Read temperature and humidity from DHT sensor
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  float f = dht.readTemperature(true);

  // Read accelerometer and gyroscope values from MPU-6050
  Wire.beginTransmission(GY521_ADDRESS);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(GY521_ADDRESS, 14, true);

  ax = Wire.read() << 8 | Wire.read();
  ay = Wire.read() << 8 | Wire.read();
  az = Wire.read() << 8 | Wire.read();
  gx = Wire.read() << 8 | Wire.read();
  gy = Wire.read() << 8 | Wire.read();
  gz = Wire.read() << 8 | Wire.read();

  accel_x = ax / 16384.0;
  accel_y = ay / 16384.0;
  accel_z = az / 16384.0;
  gyro_x = gx / 131.0;
  gyro_y = gy / 131.0;
  gyro_z = gz / 131.0;

  // Complementary filter to combine accelerometer and gyroscope readings
  float roll = atan2(accel_y, sqrt(accel_x * accel_x + accel_z * accel_z));
  float pitch = atan2(-accel_x, sqrt(accel_y * accel_y + accel_z * accel_z));
  float gyro_roll = gyro_x * 0.0000611;
  float gyro_pitch = gyro_y * 0.0000611;
  float gyro_yaw = gyro_z * 0.0000611;
  roll = alpha * (roll + gyro_roll * 0.01) + (1 - alpha) * roll;
  pitch = alpha * (pitch + gyro_pitch * 0.01) + (1 - alpha) * pitch;

  // Send sensor readings in a single string separated by commas
  Serial.print(h);
  Serial.print(",");
  Serial.print(t);
  Serial.print(",");
  Serial.print(roll);
  Serial.print(",");
  Serial.print(pitch);
  
}
