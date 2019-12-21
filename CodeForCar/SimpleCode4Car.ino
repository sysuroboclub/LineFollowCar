#include <Servo.h>
#include <SSD1306.h>
#define OLED_DC 10
#define OLED_CLK 19
#define OLED_MOSI 13
#define OLED_RESET 12
SSD1306 oled(OLED_MOSI, OLED_CLK, OLED_DC, OLED_RESET, 0);
Servo myservo;
String inputString = "";
String inputStringBuffer = "";
#define AIN1 11
#define AIN2 5
#define BIN1 6
#define BIN2 3
void setup()
{
  oled.ssd1306_init(SSD1306_SWITCHCAPVCC);
  oled.clear(); // clears the screen and buffer
  Serial.begin(115200);
  myservo.attach(9);
  pinMode(AIN1, OUTPUT);
  pinMode(AIN2, OUTPUT);
  pinMode(BIN1, OUTPUT);
  pinMode(BIN2, OUTPUT);
}

void loop()
{
  // read from port 0, send to port 1:
  oled.clear();
  uint8_t deg = 0;

  digitalWrite(AIN1, LOW);
  digitalWrite(BIN2, LOW);

  if (inputString[0] == 'X')
  {
    oled.drawstring(0, 0, (char *)inputString.c_str());
    deg = inputString.substring(1).toInt();
    myservo.write(deg);
  }
  uint8_t speed = 0;
  if (inputString[0] == 'Y')
  {
    oled.drawstring(5, 0, (char *)inputString.c_str());
    
  }
  if (inputString[0] == 'L')
  {
    oled.drawstring(10, 0, (char *)inputString.c_str());
  }
  if (inputString[0] == 'R')
  {
    oled.drawstring(15, 0, (char *)inputString.c_str());
    speed = inputString.substring(1).toInt();
    analogWrite(BIN1, speed);
    analogWrite(AIN2, speed);
  }
  oled.display();
}
void serialEvent()
{
  while (Serial.available())
  {
    char inChar = (char)Serial.read();
    if (inChar == '\n' || inChar == '\r')
    {
      inputString = inputStringBuffer;
      inputStringBuffer = "";
      break;
    }
    inputStringBuffer += inChar;
  }
}
