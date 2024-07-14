//Loading libraries
#include "DHT.h"
#include <SoftwareSerial.h>
#include <LiquidCrystal.h>
//defining nodemcu pins
SoftwareSerial nodemcu(11,10);

#define echoPin 9 // attach pin D9 Arduino to pin Echo of HC-SR04
#define trigPin 13 //attach pin D10 Arduino to pin Trig of HC-SR04
#define DHTPIN 2     // what pin we're connected to on the Temp and Humidity Sensor
#define DHTTYPE DHT11   // DHT 11 
DHT dht(DHTPIN, DHTTYPE);
//defining LiquidCrystalDisplay Pins as variables to move cursor and print characters
const int rs = 8, en = 7, d4 = 3, d5 = 4, d6 = 5, d7 = 6;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

boolean tflag = false; // temperature flag. 
// stops repetition
int relay = 13; 
int sdata1 = 0; // humidity
int sdata2 = 0; // temperature

// defines variables
long duration; // variable for the duration of sound wave travel
int distance; // variable for the distance measurement

String cdata; // complete data, consisting of sensors values

void setup()
{
Serial.begin(9600); 
nodemcu.begin(9600);
dht.begin();
lcd.begin(16, 2);

pinMode(4, OUTPUT); // dht11 vcc pin is connected with pin 4 (power pin/5v/3.3v)
digitalWrite(4, HIGH); 
pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
pinMode(echoPin, INPUT); // Sets the echoPin as an INPUT
}

void loop()
{
    // Wait a few seconds between measurements.
  delay(2000);
  int sensorValue = analogRead(A0);
  // Sensor readings may also be up to 2 seconds (due to old sensor)
  int h = dht.readHumidity();
  // Read temperature as Celsius
  int t = dht.readTemperature();
  // Read temperature as Fahrenheit
  int f = dht.readTemperature(true);
  
  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Compute heat index
  // Must send in temp in Fahrenheit!
  int hi = dht.computeHeatIndex(f, h);
    sdata1 = h;
    sdata2 = t; 
   cdata = cdata + sdata1+","+sdata2; // comma will be used a delimeter
   //printing values into nodemcu serial monitor
   nodemcu.println(cdata);
   cdata = ""; 
  nodemcu.println(sensorValue);
  delay(500);
  //printing same values on the LCD
 lcd.setCursor(0,0); 
  lcd.print("Temp: ");
  lcd.print(t);
  //char223 = degree symbol 
  lcd.print((char)223);
  lcd.print("C");
  lcd.setCursor(0,1);
  lcd.print("Humidity: ");
  lcd.print(h);
  lcd.print("%");
  delay(520);
   // Clears the trigPin condition
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
  // Displays the distance on the Serial Monitor
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");
  //Displays Soil Moisture Level in Serial Monitor
  Serial.print("Soil Moisture Level = ");
  Serial.println(sensorValue);
  //Displays Temperature in Degree's C in Serial Monitor
  Serial.print("Temperature = ");
  Serial.print(t);
  Serial.print("°");
  Serial.println("C");
  //Displays Humidity Level
  Serial.print("Humidity = ");
  Serial.print(h);
  Serial.println("%");

}
