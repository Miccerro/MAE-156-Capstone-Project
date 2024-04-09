#include <Adafruit_NeoPixel.h>

#define NEOPIXEL_PIN   49  // Pin number connected to the Neopixel-compatible LED
#define NUMPIXELS      1   // Number of Neopixels

// Create a NeoPixel object
Adafruit_NeoPixel pixels(NUMPIXELS, NEOPIXEL_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  pixels.begin(); // Initialize the NeoPixel object
}

void loop() {
  // Set the color of the Neopixel-compatible LED to purple (R:150, G:0, B:150)
  pixels.setPixelColor(0, pixels.Color(150, 0, 150));
  
  // Update the Neopixel-compatible LED
  pixels.show();
  
  // Delay for a short duration
  delay(1000);
}
