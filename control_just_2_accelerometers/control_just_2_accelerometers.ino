#include <MPU6050.h>
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
#include "Wire.h"
#endif

MPU6050 accelgyro1(0x68);
MPU6050 accelgyro2(0x69);

int16_t ax1, ay1, az1;
int16_t gx1, gy1, gz1;
int16_t ax2, ay2, az2;
int16_t gx2, gy2, gz2;

String accel1Orientation;
String accel2Orientation;

int count = 0; 

void setup() {
// join I2C bus (I2Cdev library doesn't do this automatically)
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
  Wire.begin();
#elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
  Fastwire::setup(400, true);
#endif

  Serial.begin(9600);

  // initialize device
  Serial.println("Initializing I2C devices...");
  accelgyro1.initialize();
  accelgyro2.initialize();

  // verify connection
  Serial.println("Testing device connections...");
  Serial.println(accelgyro1.testConnection() ? "1 connection successful" : "MPU6050 1 connection failed");
  Serial.println(accelgyro2.testConnection() ? "2 connection successful" : "MPU6050 2 connection failed");
}

void loop() {
  accelgyro1.getMotion6(&ax1, &ay1, &az1, &gx1, &gy1, &gz1);
  accelgyro2.getMotion6(&ax2, &ay2, &az2, &gx2, &gy2, &gz2);
  getOrientation(ax1, ay1, az1, gx1, gy1, gz1, 1);
  Serial.print(accel1Orientation);
  getOrientation(ax2, ay2, az2, gx2, gy2, gz2, 2);
  Serial.print(accel2Orientation);
  Serial.println();

  delay(50);
}

void getOrientation(int16_t ax, int16_t ay, int16_t az, int16_t gx, int16_t gy, int16_t gz, int accel) {
  if (abs(ax) > abs(ay) && abs(ax) > abs(az)) {
    if (ax > 0) {
      accel == 1 ? accel1Orientation = "1-X-up " : accel2Orientation = "2-X-up ";
    } else {
      accel == 1 ? accel1Orientation = "1-X-down " : accel2Orientation = "2-X-down ";
    }
  }
  if (abs(ay) > abs(ax) && abs(ay) > abs(az)) {
    if (ay > 0) {
      accel == 1 ? accel1Orientation = "1-Y-up " : accel2Orientation = "2-Y-up ";
    } else {
      accel == 1 ? accel1Orientation = "1-Y-down " : accel2Orientation = "2-Y-down ";
    }
  }
  if (abs(az) > abs(ax) && abs(az) > abs(ay)) {
    if (az > 0) {
      accel == 1 ? accel1Orientation = "1-Z-up " : accel2Orientation = "2-Z-up ";
    } else {
      accel == 1 ? accel1Orientation = "1-Z-down " : accel2Orientation = "2-Z-down ";
    }
  }
}