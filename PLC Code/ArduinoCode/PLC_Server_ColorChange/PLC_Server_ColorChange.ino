#include <Ethernet.h>
#include <Adafruit_NeoPixel.h>

// NeoPixel Configuration
#define NEOPIXEL_PIN   49  // Pin number connected to the Neopixel-compatible LED
#define NUMPIXELS      1   // Number of Neopixels

// Ethernet Configuration
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };  // MAC address for the PLC
IPAddress ip(192, 168, 1, 100);  // Static IP address for the PLC
EthernetServer server(80);  // TCP server instance on port 80

// NeoPixel Object
Adafruit_NeoPixel pixels(NUMPIXELS, NEOPIXEL_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  // Initialize NeoPixel
  pixels.begin();
  
  // Set NeoPixel color to purple (R:150, G:0, B:150)
  pixels.setPixelColor(0, pixels.Color(150, 0, 150));
  
  // Update NeoPixel
  pixels.show();
  
  // Initialize Ethernet with static IP address
  Ethernet.begin(mac, ip);
  
  // Start TCP server
  server.begin();
}

//loops forever
void loop() {
  // Check for incoming client connections
  EthernetClient client = server.available();
  if (client) {
    // If a client is connected, handle the request
    handleClient(client);
  }
}

void handleClient(EthernetClient client) {
  // Read the request from the client (not implemented in this example)
  
  // Respond to the client with a simple message
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html");
  client.println();
  client.println("<html><body><h1>Welcome to the P1AM-200 PLC!</h1></body></html>");
  
  // Change NeoPixel color based on client request (string format)
  if (client.available()) {
    // Read NeoPixel color values as a string (for example: "150,0,150")
    String color_values = client.readStringUntil('\n');
    
    // Extract color values from the string
    int comma1 = color_values.indexOf(',');
    int comma2 = color_values.indexOf(',', comma1 + 1);
    int red = color_values.substring(0, comma1).toInt();
    int green = color_values.substring(comma1 + 1, comma2).toInt();
    int blue = color_values.substring(comma2 + 1).toInt();
    
    // Set NeoPixel color
    pixels.setPixelColor(0, pixels.Color(red, green, blue));
    pixels.show();
  }
  
  // Close the connection
  client.stop();
}
