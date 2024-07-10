int relayPin_1 = 2; 
int relayPin_2 = 3; 
int relayPin_3 = 4; 
int relayPin_4 = 5; 

char inputString[8]; // Array to hold the input string
bool stringComplete = false; // Flag to indicate when the input string is complete

void setup() {
  pinMode(relayPin_1, OUTPUT);
  digitalWrite(relayPin_1, HIGH); // Start with the relay off

  pinMode(relayPin_2, OUTPUT);
  digitalWrite(relayPin_2, HIGH); // Start with the relay off

  pinMode(relayPin_3, OUTPUT);
  digitalWrite(relayPin_3, HIGH); // Start with the relay off

  pinMode(relayPin_4, OUTPUT);
  digitalWrite(relayPin_4, HIGH); // Start with the relay off
    
  Serial.begin(9600); // Initialize serial communication
  inputString[0] = '\0'; // Initialize inputString to an empty string

}

void loop() {
  
  // while(!Serial.available()); // wait till data to be filled in serial buffer
  // String incommingStr = Serial.readStringUntil('\n'); // read the complete string


  if (stringComplete) {
    int cmd_id;
    int relay_no, arg;

    // Parse the input string
    sscanf(inputString, "%d:%d:%d", &cmd_id, &relay_no, &arg);

    Serial.print("**********\n");
    Serial.print("VALUES OUTSIDE THE FUNCTION: \n");
    Serial.print(cmd_id);
    Serial.print(relay_no);
    Serial.print(", ");
    Serial.println(arg);
    Serial.print("VALUES INSIDE THE FUNCTION: \n");

    // Call functions based on the cmd_id
    if (cmd_id == 1) {
      toggle(relay_no, arg);
    }
    else if (cmd_id == 2) {
      timer_toggle(relay_no, arg);
    }
    else {
      Serial.println("Unknown command");
    }

    // Clear the input string and reset the flag
    inputString[0] = '\0';
    stringComplete = false;
    }

    
  // Read serial input
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    strncat(inputString, &inChar, 1);
    if (inChar == '\n') {
      stringComplete = true;
    }
  }

}

  // Example toggle
  void toggle(int relay_no, int arg) {
    Serial.print("*toggle* called with values: ");
    Serial.print(relay_no);
    Serial.print(", ");
    Serial.println(arg);
    if (relay_no == 1){
      if (arg == 1) {
        digitalWrite(relayPin_1, HIGH); // Turn relay 1 on
        } 
      else if (arg == 0) {
          digitalWrite(relayPin_1, LOW); // Turn relay 1 off
        }
      else {
      Serial.println("Unknown command");
      }
    }
    else if (relay_no == 2){
      if (arg == 1) {
        digitalWrite(relayPin_2, HIGH); 
      } 
      else if (arg == 0) {
        digitalWrite(relayPin_2, LOW); 
      }
      else {
      Serial.println("Unknown command");
      }
    }
    else if (relay_no == 3){
      if (arg == 1) {
        digitalWrite(relayPin_3, HIGH); 
      } 
      else if (arg == 0) {
        digitalWrite(relayPin_3, LOW); 
      }
    else {
      Serial.println("Unknown command");
      }
    }
    else if (relay_no == 4){
      if (arg == 1) {
        digitalWrite(relayPin_4, HIGH); 
      } 
      else if (arg == 0) {
        digitalWrite(relayPin_4, LOW);
      }
      else {
      Serial.println("Unknown command");
      }
    }
    else {
      Serial.println("Unknown command");
    }
  }


void timer_toggle(int relay_no, int arg) {
  // arg is the time interval
  Serial.print("timer_toggle called with values: ");
  Serial.print(relay_no);
  Serial.print(", ");
  Serial.println(arg);

  if (arg <= 10000) {
    if (relay_no == 1){
      digitalWrite(relayPin_1, LOW); 
      delay(arg);
      digitalWrite(relayPin_1, HIGH);
    }
    else if (relay_no == 2){
      digitalWrite(relayPin_2, LOW); 
      delay(arg);
      digitalWrite(relayPin_2, HIGH); 
    }

    else if (relay_no == 3){
      digitalWrite(relayPin_3, LOW); 
      delay(arg);
      digitalWrite(relayPin_3, HIGH); 
    }  
    else if (relay_no == 4){
      digitalWrite(relayPin_4, LOW);
      delay(arg);
      digitalWrite(relayPin_4, HIGH); 
    }
  }   
  else {
    Serial.println("time too long");
  }
}
