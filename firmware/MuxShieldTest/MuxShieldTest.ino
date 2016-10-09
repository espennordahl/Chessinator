//This example shows how to use the Mux Shield for digital outputs
#include <MuxShield.h>

float FIRST_REED_PIN = 50;
float LAST_REED_PIN = 51;

//Initialize the Mux Shield
MuxShield muxShield;

void setup()
{
    Serial.begin(115200);
    Serial.print("Setting up!");
    muxShield.setMode(1,DIGITAL_IN_PULLUP);  
    muxShield.setMode(2,DIGITAL_IN_PULLUP);
    muxShield.setMode(3,DIGITAL_IN_PULLUP);
    for (int i=FIRST_REED_PIN; i<=LAST_REED_PIN; i++)
    {
      pinMode(i,INPUT_PULLUP);
    }
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
    }
    sensorIndex++;
  }
    for(int i=0; i<16; i++)
  {
    reading = muxShield.digitalReadMS(2,i);
    if (reading != sensorState[sensorIndex]){
      shouldUpdate = true;
      sensorState[sensorIndex] = reading;      
    }
    sensorIndex++;
  }
  for(int i=0; i<16; i++)
  {
    reading = muxShield.digitalReadMS(3,i);
    if (reading != sensorState[sensorIndex]){
      shouldUpdate = true;
      sensorState[sensorIndex] = reading;      
    }
    sensorIndex++;
  }
  for(int i=FIRST_REED_PIN; i<=LAST_REED_PIN; ++i){
    reading = digitalRead(i);
    if (reading != sensorState[sensorIndex]){
      shouldUpdate = true;
      sensorState[sensorIndex] = reading;      
    }
    sensorIndex++;
  }
}

