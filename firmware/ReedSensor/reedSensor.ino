//This example shows how to use the Mux Shield for digital outputs
#include <MuxShield.h>

//Initialize the Mux Shield
MuxShield muxShield;

float FIRST_REED_PIN = 50;
float LAST_REED_PIN = 51;

void setup()
{
    Serial.begin(115200);
    Serial.print("Setting up!\n");
    muxShield.setMode(1,DIGITAL_IN_PULLUP);  
    muxShield.setMode(2,DIGITAL_IN_PULLUP);
    muxShield.setMode(3,DIGITAL_IN_PULLUP);
    for (int i=FIRST_REED_PIN; i<=LAST_REED_PIN; i++)
    {
      pinMode(i,INPUT_PULLUP);
    }
    Serial.print("Done!\n");
}

bool shouldUpdate = false;
int sensorState[] = { 0,0,0,0,0,0,0,0,
                      0,0,0,0,0,0,0,0,
                      0,0,0,0,0,0,0,0,
                      0,0,0,0,0,0,0,0,
                      0,0,0,0,0,0,0,0,
                      0,0,0,0,0,0,0,0,
                      0,0,0,0,0,0,0,0,
                      0,0,0,0,0,0,0,0};

char* names[] = {       "a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8",
                        "b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8",
                        "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8",
                        "d1", "d2", "d3", "d4", "d5", "d6", "d7", "d8",
                        "e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8",
                        "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8",
                        "g1", "g2", "g3", "g4", "g5", "g6", "g7", "g8",
                        "h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8"};

void loop()
{
  checkState();
  if(shouldUpdate == true)
  {
    postUpdate();
    shouldUpdate = false;
  }
}

void postUpdate()
{
  Serial.print("\n updated sensor data \n");
  for (int i=0; i<64; i++)
  {
    Serial.print(sensorState[i]);
  }
  Serial.print("\n ok \n");
}

void checkState()
{
  int sensorIndex = 0;
  int reading = 0;
  for(int i=0; i<16; i++)
  {
    reading = muxShield.digitalReadMS(1,i);
    if (reading != sensorState[sensorIndex]){
      shouldUpdate = true;
      sensorState[sensorIndex] = reading;      
      Serial.print("Detected change in\n");
      Serial.print(names[sensorIndex]);
      Serial.print("\n");
    }
    sensorIndex++;
  }
    for(int i=0; i<16; i++)
  {
    reading = muxShield.digitalReadMS(2,i);
    if (reading != sensorState[sensorIndex]){
      shouldUpdate = true;
      sensorState[sensorIndex] = reading;
      Serial.print("Detected change in\n");
      Serial.print(names[sensorIndex]);
      Serial.print("\n");
    }
    sensorIndex++;
  }
  for(int i=0; i<16; i++)
  {
    reading = muxShield.digitalReadMS(3,i);
    if (reading != sensorState[sensorIndex]){
      shouldUpdate = true;
      sensorState[sensorIndex] = reading;      
      Serial.print("Detected change in\n");
      Serial.print(names[sensorIndex]);
      Serial.print("\n");
    }
    sensorIndex++;
  }
  for(int i=FIRST_REED_PIN; i<=LAST_REED_PIN; ++i){
    reading = digitalRead(i);
    if (reading != sensorState[sensorIndex]){
      shouldUpdate = true;
      sensorState[sensorIndex] = digitalRead(i);      
      Serial.print("Detected change in\n");
      Serial.print(names[sensorIndex]);
      Serial.print("\n");
    }
    sensorIndex++;
  }
}

