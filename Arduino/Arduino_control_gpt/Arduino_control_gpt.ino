int relayPin_2 = 2; // Pin connected to the relay
int relayPin_3 = 3; // Pin connected to the relay
int relayPin_4 = 4; // Pin connected to the relay
int relayPin_5 = 5; // Pin connected to the relay





void setup() {
  pinMode(relayPin_2, OUTPUT);
  digitalWrite(relayPin_2, HIGH); // Start with the relay off

  pinMode(relayPin_3, OUTPUT);
  digitalWrite(relayPin_3, HIGH); // Start with the relay off

  pinMode(relayPin_4, OUTPUT);
  digitalWrite(relayPin_4, HIGH); // Start with the relay off

  pinMode(relayPin_5, OUTPUT);
  digitalWrite(relayPin_5, HIGH); // Start with the relay off
  
  Serial.begin(9600); // Begin serial communication at a baud rate of 9600
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    if (command == "2.1") {
      digitalWrite(relayPin_2, HIGH); // Turn relay 2 on
    } 
    else if (command == "2.0") {
      digitalWrite(relayPin_2, LOW); // Turn relay 2 off
    }
    else if (command == "3.1") {
      digitalWrite(relayPin_3, HIGH); // Turn relay 3 on
    }
    else if (command == "3.0") {
      digitalWrite(relayPin_3, LOW); // Turn relay 3 off
    }
    else if (command == "4.1") {
      digitalWrite(relayPin_4, HIGH); // Turn relay 4 on
    }
    else if (command == "4.0") {
      digitalWrite(relayPin_4, LOW); // Turn relay 4 off
    }
    else if (command == "5.1") {
      digitalWrite(relayPin_5, HIGH); // Turn relay 5 on
    }
    else if (command == "5.0") {
      digitalWrite(relayPin_5, LOW); // Turn relay 5 off
  }
  }
}
