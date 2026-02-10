byte ledState = LOW;

void setup() {

  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);

  digitalWrite(LED_BUILTIN, ledState);
  Serial.println(F("LED is OFF"));

  Serial.println(F("System is ready. Send ON or OFF."));

}

void loop() {

  if (Serial.available() > 0) {
    
    String msg = Serial.readStringUntil('\n');
    msg.trim();

    if (msg == "ON") {
    
      ledState = HIGH;
      digitalWrite(LED_BUILTIN, ledState);
      Serial.println(F("LED is ON"));
    
    }

    else if (msg == "OFF") {
      
      ledState = LOW;
      digitalWrite(LED_BUILTIN, ledState);
      Serial.println(F("LED is OFF"));
    
    }

    else if (msg.length() > 0) {
      
      Serial.print(F("Unknown command: "));
      Serial.println(msg);
      
      for (int i = 0; i < 5; i++){
        digitalWrite(LED_BUILTIN, HIGH);
        delay(100);
        digitalWrite(LED_BUILTIN, LOW);
        delay(100);
      }

      digitalWrite(LED_BUILTIN, ledState);
    }
  
  }

}
