#include <ArduinoBLE.h>

long previousMillis = 0;
int interval = 0;
int ledState = LOW;
int ledPin = 13;
int motorPin = 3;

BLEService ledService("180A"); // BLE LED Service

// BLE LED Switch Characteristic - custom 128-bit UUID, read and writable by central
BLEByteCharacteristic switchCharacteristic("2A57", BLERead | BLEWrite);

void setup() {
  Serial.begin(9600);
  //while (!Serial);

  // set built in LED pin to output mode
  // pinMode(LED_BUILTIN, OUTPUT);
  pinMode(ledPin, OUTPUT);
  pinMode(motorPin, OUTPUT);

  // begin initialization
  if (!BLE.begin()) {
    Serial.println("starting BLE failed!");

    while (1);
  }

  // set advertised local name and service UUID:
  BLE.setLocalName("Nano 33 IoT");
  BLE.setAdvertisedService(ledService);

  // add the characteristic to the service
  ledService.addCharacteristic(switchCharacteristic);

  // add service
  BLE.addService(ledService);

  // set the initial value for the characteristic:
  switchCharacteristic.writeValue(0);

  // start advertising
  BLE.advertise();

  Serial.println("BLE LED Peripheral");
}

void loop() {
  // listen for BLE peripherals to connect:
  BLEDevice central = BLE.central();

  // if a central is connected to peripheral:
  if (central) {
    Serial.print("Connected to central: ");
    // print the central's MAC address:
    Serial.println(central.address());

    // while the central is still connected to peripheral:
    while (central.connected()) {
      // if the remote device wrote to the characteristic,
      // use the value to control the LED:
      if (switchCharacteristic.written()) {
        switch (switchCharacteristic.value()) {   // any value other than 0
          case 01:
            Serial.println("Reminder on");
            for (int i = 0; i < 20; i++) {
              Serial.println("LED high");
              Serial.println("Motor high");
              digitalWrite(ledPin, HIGH);    
              digitalWrite(motorPin, HIGH);
              delay(500);
              Serial.println("LED low");
              Serial.println("Motor low");
              digitalWrite(ledPin, LOW);    
              digitalWrite(motorPin, LOW);
              delay(500);
              
            }           // will turn the LED on
            break;
          default:
            Serial.println("LED low");
            Serial.println("Motor low");
            digitalWrite(ledPin, LOW);    
            digitalWrite(motorPin, LOW);
            break;
        }
      }
    }

    // when the central disconnects, print it out:
    Serial.print(F("Disconnected from central: "));
    Serial.println(central.address());
    digitalWrite(LED_BUILTIN, LOW);         // will turn the LED off
  }
}
