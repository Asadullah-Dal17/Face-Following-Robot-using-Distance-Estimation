// Adding necessery Libraries
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(7, 8);   // nRF24L01 (CE, CSN)
const byte address[6] = "00001"; // Address
int MovDir;
int Speed1;
int Speed2;
// creating Structure Data 
struct Data_Pack {
//    byte IN1;
//    byte IN2;
//    byte IN3;
//    byte IN4;
    byte EN1_Speed;
    byte EN2_Speed;
    byte MovementDirection;
    //LED Values
    byte R;
    byte G;
    byte B;
    

};
Data_Pack data; // Creating Variables with above structure
void setup()
{
    Serial.begin(9600);
    radio.begin(); // Stratig the radio
    // setting up Radio Perameters
    radio.openWritingPipe(address);
    radio.setAutoAck(false);
    radio.setDataRate(RF24_250KBPS);
    radio.setPALevel(RF24_PA_LOW);
    
}
void loop()
{
 if (Serial.available()>0){

  if (Serial.read()=='D')
      {
    data.MovementDirection= Serial.parseInt();
      }
    if (Serial.read()=='A')
    {
    data.EN1_Speed = Serial.parseInt();   
    }
  
    if (Serial.read()=='B')
    {
  data.EN2_Speed = Serial.parseInt();
    }
    radio.write(&data, sizeof(Data_Pack));
    delay(20);
 }

//    data.text = 225;
//    data.Value =20;
//    Serial.println(data.text);
    
    

Serial.println("data Send: ");
}
