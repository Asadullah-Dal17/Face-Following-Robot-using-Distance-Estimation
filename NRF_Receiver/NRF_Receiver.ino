// Adding necessery Libraries
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
//time 
//MotorDirve Pins
//These pin For Controlling the Speed of motors
int Enable1 = 3;
int Enable2 = 5; 
int condition;
//Theses Pins are for Direction Controll of Motor

int IN1 = A0;
int IN2 = A1;
int IN3 = A2;
int IN4 = A3;
int Sp1;
int Sp2;

//RGB LED PINs
int Red =6;;// PMW pin
int Blue =9;//PMW Pins
int Green =10;//PMW Pins


unsigned long LastReceivedTime = 0;
unsigned long CurrentTime =0;
RF24 radio(7, 8);   // nRF24L01 (CE, CSN)
const byte address[6] = "00001"; // Address

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
//    Setting Pins Mode 
    
    pinMode(Enable1, OUTPUT);
    pinMode(Enable2, OUTPUT);
    
    pinMode(IN1, OUTPUT);// here I used Analog pin as Digital OUTPUT
    pinMode(IN2, OUTPUT);
    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);
//    LED PINs
    pinMode(Red, OUTPUT);
    pinMode(Green, OUTPUT);
    pinMode(Blue, OUTPUT);
    
    radio.begin(); // Stratig the radio
    // setting up Radio Perameters
    radio.openReadingPipe(0, address);
    radio.setAutoAck(false);
    radio.setDataRate(RF24_250KBPS);
    radio.setPALevel(RF24_PA_LOW);
    radio.startListening(); //  Set the module as receiver
    Serial.println("Radio is Setup for Communication");
    delay(1000);
//    calling the Forward movement fuction
//    Forward();
//    delay(1000);
//    Backward();
//    Left(150,150);
//    delay(2000);
//    Right(200,200);
//    delay(5000);
//    delay(2000);
    Stop(0,0);
    

  
}
void loop()
{
  CurrentTime = millis();
if (CurrentTime -LastReceivedTime>1000){
    Serial.println("Time OUT");
  }
if (radio.available()){
    radio.read(&data, sizeof(Data_Pack) );
//    Serial.println("== InComing Data ==");
//    Serial.print("EN1 Speed  = ");
//    Serial.println(data.EN1_Speed);
//    Serial.print("EN2 Speed = ");
////    Serial.println(data.EN2_Speed);
      Sp1 =data.EN1_Speed;
      Sp2 = data.EN2_Speed;
  Serial.println(Sp1);
  Serial.println(Sp2);
   condition = data.MovementDirection;
   Serial.println(condition);
    delay(100);
    LastReceivedTime =millis();
     switch(condition){
  case 1:
  Serial.println("Move Forward");
  Forward(Sp1,Sp2);
  break;
  case 2:
  Backward(Sp1,Sp2);
  Serial.println("Move Backward");
  break;
  case 3:
  Left(Sp1,Sp2);
  Serial.println("Move Left");
  break;
  case 4:
  Right(Sp1, Sp2);
  Serial.println("Move Right");
  break;
  default:
  Serial.print("None of Above Conditon is True:");
  Stop(0,0);
  Serial.println("Stoped");
  break;
  
  }

}
else{
  Stop(0,0);
//    Serial.println("  -- Radio is Not Available -- ");
int X =12;
}
//Serial.println("Ending");
delay(100);
// condition='1';


}


void RGB(int RED, int GREEN, int BLUE){
  analogWrite(Red, RED);
  analogWrite(Green, GREEN);
  analogWrite(Blue, BLUE);
}
//creating Fucntion for Movement of Robot

void Forward(int Speed1, int Speed2){
  analogWrite(Enable1, Speed1);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2,LOW);
  analogWrite(Enable2, Speed2);
  digitalWrite(IN3,HIGH);
  digitalWrite(IN4, LOW);
}
void Backward(int Speed1, int Speed2){
  analogWrite(Enable1, Speed1);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2,HIGH);
  analogWrite(Enable2, Speed2);
  digitalWrite(IN3,LOW);
  digitalWrite(IN4, HIGH);
}
void Left(int Speed1, int Speed2){
  analogWrite(Enable1, Speed1);
    Serial.println("Move Left");
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2,LOW);
  analogWrite(Enable2, Speed2);
  digitalWrite(IN3,LOW);
  digitalWrite(IN4, HIGH);
  
}
void Right(int Speed1, int Speed2){
  analogWrite(Enable1, Speed1);
  Serial.println("Move Right");
  digitalWrite(IN1, LOW);
  digitalWrite(IN2,HIGH);
  analogWrite(Enable2, Speed2);
  digitalWrite(IN3,HIGH);
  digitalWrite(IN4, LOW);
}
void Stop(int Speed1, int Speed2){
  analogWrite(Enable1, Speed1);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2,LOW);
  analogWrite(Enable2, Speed2);
  digitalWrite(IN3,LOW);
  digitalWrite(IN4, LOW);
}
