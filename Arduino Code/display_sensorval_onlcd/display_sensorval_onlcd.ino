
void loop(){
  //check for pin number 
  int chk = DHT.read11(DHT11_PIN);
    // read the input on analog pin 0:
  int sensorValue = analogRead(A0);
  //printing output values to serial monitor on port COM4 9600baud
  Serial.print("Temperature = ");
  Serial.println(DHT.temperature);
  Serial.print("Humidity = ");
  Serial.println(DHT.humidity);
  // print out the value you read:
  Serial.print("Soil Moisture Level = ");
  Serial.println(sensorValue);
  delay(500); 
  lcd.setCursor(0,0); 
  lcd.print("Temp: ");
  lcd.print(DHT.temperature);
  //char223 = degree symbol 
  lcd.print((char)223);
  lcd.print("C");
  lcd.setCursor(0,1);
  lcd.print("Humidity: ");
  lcd.print(DHT.humidity);
  lcd.print("%");
  delay(520);
}
