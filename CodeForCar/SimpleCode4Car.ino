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

// For TA, when the car go straight, it's 95
uint8_t steering = 95;
uint8_t throtting = 0;
// parameter for differential speed
uint8_t para = 100;
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

  digitalWrite(AIN1, LOW);
  digitalWrite(BIN2, LOW);

  //processing different data with specific prefix
  // Such X90 means send info to servo with 90
  // Such R90 means send info to motor with 90
  if (inputString[0] == 'X')
  {
    oled.drawstring(0, 0, (char *)inputString.c_str());
    steering = inputString.substring(1).toInt();
  }
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
    throtting = inputString.substring(1).toInt();
  }

  //hot fix for parameter
  if (inputString[0] == 'Q')
  {
    oled.drawstring(15, 1, (char *)inputString.c_str());
    para = inputString.substring(1).toInt();
  }
  oled.display();
  // For TA, when the car go straight, it's 95
  float diff = 95 - steering;
  diff /= para;
  diff + 1.0;
  myservo.write(steering);
  analogWrite(BIN1, throtting * ( 1.0 + diff));
  analogWrite(AIN2, throtting * (1.0 - diff));
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
