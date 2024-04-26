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

bool isCrumble = false;
bool isCompress = false;
bool isStretch1 = false;
bool isStretch2 = false;
bool isStretch3 = false;
bool isStretch4 = false;
bool isStretch = false;

// Define the pin number where the LED is connected
const int ledPin1 = 13;
const int ledPin2 = 12;
const int ledPin3 = 11;
const int ledPin4 = 10;
const int ledPin5 = 9;
const int ledPin6 = 8;
const int inputPin1 = 2;
const int inputPin2 = 3;
const int inputPin3 = 4;
const int inputPin4 = 5;
const int inputPin5 = 6;
const int inputPin6 = 7;

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
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  pinMode(ledPin3, OUTPUT);
  pinMode(ledPin4, OUTPUT);
  pinMode(ledPin5, OUTPUT);
  pinMode(ledPin6, OUTPUT);
  pinMode(inputPin1, INPUT);
  pinMode(inputPin2, INPUT);
  pinMode(inputPin3, INPUT);
  pinMode(inputPin4, INPUT);
  pinMode(inputPin5, INPUT);
  pinMode(inputPin6, INPUT);

  // verify connection
  Serial.println("Testing device connections...");
  Serial.println(accelgyro1.testConnection() ? "1 connection successful" : "MPU6050 1 connection failed");
  Serial.println(accelgyro2.testConnection() ? "2 connection successful" : "MPU6050 2 connection failed");
}

void loop() {
  digitalWrite(ledPin1, HIGH);
  digitalWrite(ledPin2, HIGH);
  digitalWrite(ledPin3, HIGH);
  digitalWrite(ledPin4, HIGH);
  digitalWrite(ledPin5, HIGH);
  digitalWrite(ledPin6, HIGH);
  int crumbleData = digitalRead(inputPin1);
  int compressData = digitalRead(inputPin2);
  int stretch1Data = digitalRead(inputPin3);
  int stretch2Data = digitalRead(inputPin4);
  int stretch3Data = digitalRead(inputPin5);
  int stretch4Data = digitalRead(inputPin6);

  if (crumbleData == HIGH) {
    // Serial.println("🥵");
    isCrumble = true;
  } else {
    isCrumble = false;
  }
  if (compressData == HIGH) {
    isCompress = true;
  } else {
    isCompress = false;
  }
  if (stretch1Data == HIGH) {
    // Serial.println("✅");
    isStretch1 = true;
  } else {
    isStretch1 = false;
  }
  if (stretch2Data == HIGH) {
    // Serial.println("✅✅");
    isStretch2 = true;
  } else {
    isStretch2 = false;
  }
  if (stretch3Data == HIGH) {
    // Serial.println("✅✅✅");
    isStretch3 = true;
  } else {
    isStretch3 = false;
  }
  if (stretch4Data == HIGH) {
    // Serial.println("✅✅✅✅");
    isStretch4 = true;
  } else {
    isStretch4 = false;
  }
  isStretch = (isStretch1 && isStretch2) || (isStretch3 && isStretch4);
  accelgyro1.getMotion6(&ax1, &ay1, &az1, &gx1, &gy1, &gz1);
  accelgyro2.getMotion6(&ax2, &ay2, &az2, &gx2, &gy2, &gz2);
  getOrientation(ax1, ay1, az1, gx1, gy1, gz1, 3);
  Serial.print(accel1Orientation);
  getOrientation(ax2, ay2, az2, gx2, gy2, gz2, 4);
  Serial.print(accel2Orientation);
  printData();
  Serial.println();

  delay(50);
}

void printData() {
  if (isStretch) {
    Serial.print("stretching ");
  } else {
    Serial.print("not-stretching ");
  }
  if (isCrumble) {
    Serial.print("crumble ");
  } else {
    Serial.print("not-crumble ");
  }
  if (isCompress) {
    Serial.print("compress ");
  } else {
    Serial.print("not-compress ");
  }
}

void getOrientation(int16_t ax, int16_t ay, int16_t az, int16_t gx, int16_t gy, int16_t gz, int accel) {
  if (abs(ax) > abs(ay) && abs(ax) > abs(az)) {
    if (ax > 0) {
      accel == 3 ? accel1Orientation = "3-X-up " : accel2Orientation = "4-X-up ";
    } else {
      accel == 3 ? accel1Orientation = "3-X-down " : accel2Orientation = "4-X-down ";
    }
  }
  if (abs(ay) > abs(ax) && abs(ay) > abs(az)) {
    if (ay > 0) {
      accel == 3 ? accel1Orientation = "3-Y-up " : accel2Orientation = "4-Y-up ";
    } else {
      accel == 3 ? accel1Orientation = "3-Y-down " : accel2Orientation = "4-Y-down ";
    }
  }
  if (abs(az) > abs(ax) && abs(az) > abs(ay)) {
    if (az > 0) {
      accel == 3 ? accel1Orientation = "3-Z-up " : accel2Orientation = "4-Z-up ";
    } else {
      accel == 3 ? accel1Orientation = "3-Z-down " : accel2Orientation = "4-Z-down ";
    }
  }
}
