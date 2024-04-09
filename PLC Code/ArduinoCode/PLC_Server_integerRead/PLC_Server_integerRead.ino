#include <Ethernet.h>

// Define MAC address and IP address
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
IPAddress ip(192, 168, 1, 100);

// Define port for server
unsigned int port = 80;
int calc = 0;

// Create a TCP server
EthernetServer server(port);

void setup() {
  // Initialize Ethernet
  Ethernet.begin(mac, ip);
  server.begin();
}

void loop() {
  // Check for client connection
  EthernetClient client = server.available();
  if (client) {
    Serial.print("YOURE CONNECTED");
    // Wait for data from client
    while (client.connected()) {
      if (client.available()) {
        // Read bytes from client into buffer
        char buffer[128]; // Buffer to hold received data
        int bytesRead = client.readBytes(buffer, sizeof(buffer));

        int readData = (int)buffer[bytesRead - 1];

        // Print only the last byte after processing all bytes
        if (bytesRead > 0) {
          Serial.print("Received integer data: ");
          Serial.println(readData); // Print last byte as integer value
        }

        
        calc = readData*2;
        Serial.println(calc);


      }
    }
    // Close client connection
    client.stop();
  }
}
