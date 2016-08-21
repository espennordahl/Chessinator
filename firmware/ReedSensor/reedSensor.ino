//This example shows how to use the Mux Shield for digital outputs
#include <MuxShield.h>

//Initialize the Mux Shield
MuxShield muxShield;

void setup()
{
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
  }
}

void postUpdate()
{
  Serial.print("updated sensor data");
  for (int i=0; i<64; i++)
  {
    Serial.print(sensorState[i]);
  }
  Serial.print("ok");
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
      sensorState[sensorIndex] = digitalRead(i);      
    }
    sensorIndex++;
  }
}

