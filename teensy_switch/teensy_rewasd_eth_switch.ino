#include <NativeEthernet.h>
#include <NativeEthernetUdp.h>

EthernetUDP Udp;
const int PORT = 9999;
uint8_t buffer[32];


// Buttons
#define BTN_A 4096
#define BTN_B 8192
#define BTN_X 16384
#define BTN_Y 32768

#define BTN_L1 256
#define BTN_R1 512
#define BTN_L2 1024
#define BTN_R2 2048

#define BTN_MINUS 1
#define BTN_PLUS  2
#define BTN_L3    4
#define BTN_R3    8




// Dpad
#define DPAD_UP         0
#define DPAD_UP_RIGHT   1
#define DPAD_RIGHT      2
#define DPAD_DOWN_RIGHT 3
#define DPAD_DOWN       4
#define DPAD_DOWN_LEFT  5
#define DPAD_LEFT       6
#define DPAD_UP_LEFT    7
#define DPAD_NEUTRAL    8

uint8_t mapStick(int16_t v) {
  return (uint32_t)(v + 32768) * 255 / 65535;
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200); // May not need this?
  Ethernet.begin();
  Udp.begin(PORT);
  // Don't forget to start the gamepad
  // Then delay it (to give time to connect)
}

void loop() {
  // put your main code here, to run repeatedly:
  int packetSize = Udp.parsePacket();
  if (packetSize == 11) {
    Udp.read(buffer, 11);

    uint16_t  buttons = buffer[0] | (buffer[1] << 8);
    uint8_t   dpad    = buffer[2];

    int16_t   lx      = buffer[3] | (buffer[4]   << 8);
    int16_t   ly      = buffer[5] | (buffer[6]   << 8);
    int16_t   rx      = buffer[7] | (buffer[8]   << 8);
    int16_t   ry      = buffer[9] | (buffer[10]  << 8);

    // Buttons
    if (buttons & BTN_A)
    {
      // Press button A
    }
    if (buttons & BTN_B)
    {
      // ...
    }
    if (buttons & BTN_X)
    {

    }
    if (buttons & BTN_Y) {
      
    }
    if (buttons & BTN_L1) {

    }
    if (buttons & BTN_R1) {

    }
    if (buttons & BTN_L2) {

    }
    if (buttons & BTN_R2) {

    }
    if (buttons & BTN_L3) {

    }
    if (buttons & BTN_R3) {

    }
    if (buttons & BTN_MINUS) {

    }
    if (buttons & BTN_PLUS) {

    }



    // DPAD
    switch (dpad) {
      case DPAD_UP: 
        break;
      case DPAD_UP_RIGHT:
        break;
      case DPAD_RIGHT:
        break;
      case DPAD_DOWN_RIGHT:
        break;
      case DPAD_DOWN:
        break;
      case DPAD_DOWN_LEFT:
        break;
      case DPAD_LEFT:
        break;
      case DPAD_UP_LEFT:
        break;
      case DPAD_NEUTRAL:
        break;
    }


    // --------------- OLD METHOD ----------------
    // float normalized_lx = (lx + 32768) / 65536;
    // float normalized_ly = (ly + 32768) / 65536;
    // float normalized_rx = (rx + 32768) / 65536;
    // float normalized_ry = (ry + 32768) / 65536;

    // Values specifically for NS gamepad between 0 and 255
    // 128 is middle value (or 0 value)
    // uint8_t switch_lx = normalized_lx * 255; 
    // uint8_t switch_ly = normalized_ly * 255;
    // uint8_t switch_rx = normalized_rx * 255;
    // uint8_t switch_ry = normalized_ry * 255;
    
    // --------------- NEW METHOD ----------------
    uint8_t switch_lx = mapStick(lx);
    uint8_t switch_ly = mapStick(ly);
    uint8_t switch_rx = mapStick(rx);
    uint8_t switch_ry = mapStick(ry);

    // --------  FOR POSSIBLE INVERSIONS  ---------
    // Uncomment out these lines
    // If the sticks go the opposite way...
    // switch_ly = 255 - switch_ly;
    // switch_ry = 255 - switch_ry;

    // Update stick values
    // (Possibly see if caching prev values is more efficient)








    // Don't forget to run NSGamepad.loop(); !!!!!!

  }
}
