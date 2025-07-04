#include <LedControl.h>

// DataIn (DIN) on pin 11, CLK on pin 13, CS (LOAD) on pin 10, 1 device
LedControl lc = LedControl(11, 13, 10, 1);

void setup() {
  Serial.begin(9600);
  lc.shutdown(0, false);   // Wake up the MAX7219
  lc.setIntensity(0, 8);   // Set brightness (0–15)
  lc.clearDisplay(0);      // Clear the display
}

void loop() {
  // Wait until we have 8 bytes (one per row)
  if (Serial.available() >= 8) {
    for (int i = 0; i < 8; i++) {
      byte row = Serial.read();        // Read one byte (a row of 8 pixels)
      lc.setRow(0, i, row);            // Display the row on the matrix
    }

    // Optional: clear any extra bytes to avoid desync
    while (Serial.available() > 0) Serial.read();
  }
}
