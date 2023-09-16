// Initialize pin readout
const int buttons[] = {2, 3, 4, 5, 6};
const int numButtons = sizeof(buttons) / sizeof(buttons[0]);

// Store the previous state of each button
int prevStates[numButtons] = {LOW};

void setup() {
  for (int i = 0; i < numButtons; i++) {
    pinMode(buttons[i], INPUT);
  }
  
  Serial.begin(9600); // Initialize serial communication
}

void loop() {
  for (int i = 0; i < numButtons; i++) {
    int state = digitalRead(buttons[i]);

    // Check if the button state has changed from LOW to HIGH
    if (state == HIGH && prevStates[i] == LOW) {
      Serial.print("Button ");
      Serial.print(i + 1);
      Serial.println(" pressed");
    }

    // Update the previous state for the next loop iteration
    prevStates[i] = state;
  }
}