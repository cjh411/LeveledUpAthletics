

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <Adafruit_MMA8451.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_ST7735.h> // Hardware-specific library
#include <SPI.h>


// SET PINS FOR LCD
// INITIATE LCD
  #define TFT_CS     0
  #define TFT_RST    2
  #define TFT_DC     16
  Adafruit_ST7735 tft = Adafruit_ST7735(TFT_CS,  TFT_DC, TFT_RST);


//ACCELEROMETER INIT
  Adafruit_MMA8451 mma = Adafruit_MMA8451();


//INPUTS FOR CONNECTION TO BROKER AND WIRELESS NETWORK
  const char* ssid = "Pickled Marshmellows";
  const char* password = "qtipsinear2";
  const char* mqtt_server = "192.168.1.100";
  WiFiClient espClient;
  PubSubClient client(espClient);

//VARIABLES FOR BROKER
  float start_time=millis();
  char* pubpath="/accelerometer/";
  uint8_t MAC_array[6];
  char MAC_char[18];
  int state;
  unsigned char * inst;
  unsigned char * exer;
  unsigned char * loc;
  unsigned char * score;
  unsigned char *  rep;
  unsigned char * pf;
  unsigned char * previnst;
  unsigned char * prevexer;
  unsigned char * prevloc;
  unsigned char * prevscore;
  unsigned char * prevrep;
  unsigned char * prevpf;
  int counter;
  int instupdt;
  int locupdt;
  int repupdt;
  int pfupdt;
  int exerupdt;
  int insttime;
  int cntupdt;
  int schg;
  int scoreupdt;
  byte instarr[30][200];
  int vibetime;
  int vibeupdt;
  int cnttime;
  int currinst=0;
  char cntchar[11];
  int scrnupdt;

  int buttonPin = 15;





void setup() {

    Serial.begin(115200);

  //SCREEN SETUP
    tft.initR(INITR_144GREENTAB);
    tft.fillScreen(ST7735_BLACK);
    testdrawtext("Initialized", ST7735_WHITE,0,0);

  //BROKER AND WIFI SETUP
    setup_wifi();
    client.setServer(mqtt_server, 1883);
    client.setCallback(callback);
    reconnect();

  //ACCELEROMETER SETUP
    Wire.begin(5, 4);
    if (! mma.begin()) {
      Serial.println("Couldnt start");
      while (1);
    }
    
    Serial.println("MMA8451 found!");
    mma.setRange(MMA8451_RANGE_2_G);
    mma.setDataRate(MMA8451_DATARATE_800_HZ);



  //CREATE PATH TO PUBLISH ACCELEROMETER DATA
    WiFi.macAddress(MAC_array);
    for (int i = 0; i < sizeof(MAC_array); ++i){
      sprintf(MAC_char,"%s%02x:",MAC_char,MAC_array[i]);
    }
    strcat(pubpath,MAC_char);

    client.publish("/band1/init/out","1",0);

    pinMode(buttonPin, INPUT_PULLUP);
}







void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  
}






void testdrawtext(char *text, uint16_t color, int x, int y) {
  tft.setCursor(x,y);
  tft.setTextColor(color);
  tft.setTextWrap(true);
  tft.print(text);
}





void callback(char* topic, byte* payload_sub, unsigned int length) {

  Serial.println("Incoming data : ");
  Serial.println(topic);

//COPY PACKET SO IT ISN'T OVERWRITTEN BY PUBLISHING
  byte* p = (byte*)malloc(length);
  memcpy(p,payload_sub,length);
  p[length]=0;


  // CODE TO PROCESS MOTOR DISC
 // if (topic=="[motor]"){
  if (strcmp(topic,"levelup/band/band1/vibrate")==0) {
      vibetime = p[0] + (p[1] << 8) + (p[2] << 16) + (p[3] << 24);
      vibeupdt=1;
      
  } 
  
/*Updated in this version */

  if (strcmp(topic,"levelup/band/band1/display/inst")==0){
    inst = (byte*)malloc(length);
    memcpy(inst,p,length);
    inst[length]=0;
    instupdt++;
    for(int i = 0; i < length ; i++){
      instarr[instupdt-1][i] = inst[i];
    }
  }

  if (strcmp(topic,"levelup/band/band1/display/loc")==0){
    loc = (byte*)malloc(length);
    memcpy(loc,p,length);
    loc[length]=0;
    locupdt=1;
    scrnupdt=1;
  }

  if (strcmp(topic,"levelup/band/band1/display/pf")==0){
    pf = (byte*)malloc(length);
    memcpy(pf,p,length);
    pf[length]=0;
    pfupdt=1;
    scrnupdt=1;
  }

  if (strcmp(topic,"levelup/band/band1/display/score")==0){
    score = (byte*)malloc(length);
    memcpy(score,p,length);
    score[length]=0;
    scoreupdt=1;
    scrnupdt=1;
  }

  if (strcmp(topic,"levelup/band/band1/display/counter")==0){
    memcpy(&counter,p,sizeof(p));
    cntupdt=1;
    sprintf(cntchar,"%ld", counter);
    Serial.println(counter);
    Serial.println(cntchar);
    /*updated in this version - need to cast this to an integer for counting*/
    cnttime=millis();
    scrnupdt=1;
  }

  if (strcmp(topic,"levelup/band/band1/display/exer")==0){
    exer = (byte*)malloc(length);
//    memcpy(prevexer,exer,length);
    memcpy(exer,p,length);
    exer[length]=0;
    exerupdt=1;
    scrnupdt=1;
  }
  
  if (strcmp(topic,"levelup/band/band1/display/rep")==0){
    rep = (byte*)malloc(length);
    memcpy(rep,p,length);
    rep[length]=0;
    repupdt=1;
    scrnupdt=1;
  }

  if (strcmp(topic,"levelup/band/band1/accel/start")==0){
    if ('1'==(char)p[0]){
      if(state==0){
        schg=1;
      }
      state=1;
    }
  }
  
  if (strcmp(topic,"levelup/band/band1/accel/stop")==0){
    if ('0'==(char)p[0]){
      if(state==1){
        schg=1;
      }
      
      state=0;
      rep=0;
      exer=(unsigned char *)"Identifying Exercise";
    }
  }


  free(p);

}







void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP8266Client")) {
      client.subscribe("levelup/band/band1/#");
    } else {
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}




void instdisp(){
  
    tft.fillScreen(ST7735_BLACK);
    tft.setTextSize(1);
    testdrawtext((char *)instarr[currinst], ST7735_WHITE,0,0);
    insttime=millis();
    for(int i = 0; i < 200 ; i++){
      instarr[currinst][i] = '\0';
    }
    currinst++;
    schg=1;
}






void schgdisp(){
  
  if (state==0){
    
    tft.fillScreen(ST7735_BLACK);
    tft.setTextSize(2);
    
    testdrawtext((char *)score, ST7735_WHITE,0,0);
    testdrawtext((char *)cntchar, ST7735_WHITE,50,0);
    testdrawtext((char *)loc, ST7735_WHITE,0,25);
    
    scoreupdt=0;
    cntupdt=0;
    locupdt=0;
  }

  if (state==1){
    
    tft.fillScreen(ST7735_BLACK);
    tft.setTextSize(2);
    
    testdrawtext((char *)score, ST7735_WHITE,0,0);
    testdrawtext((char *)cntchar, ST7735_WHITE,50,0);
    testdrawtext((char *)exer, ST7735_WHITE,0,25);
    testdrawtext((char *)rep, ST7735_WHITE,0,50);
    
    scoreupdt=0;
    cntupdt=0;
    exerupdt=0;
    repupdt=0;
  }
  
  schg=0;
  scrnupdt=0;
  
}






void scrnproc(){

  if (exerupdt==1){
  
      tft.fillRect(0,25,50, 128, ST7735_BLACK);
      
      tft.setTextSize(2);
      testdrawtext((char *)exer, ST7735_WHITE,0,25);
      
      scrnupdt=0;
      exerupdt=0;
  }
}






void loop() {
  
  gameloop();
  
}







void gameloop(){
  
//For loop timing
  start_time=millis();

//connect to broker and look for messages
  if (!client.connected()) {  
    reconnect();   
  }
  
  client.loop();

//
    //Calculate delay time and delay
    int d=50-(millis()-start_time);
    Serial.println(d);
    
    if (d < 0) {
      
    }
    
    else {
      delay(d);
    }
      
        //CHECK STATE AND STREAM IF NECESSARY
      stream();
  }  







void stream(){

//get accelerometer readings
  mma.read();
  sensors_event_t event;
  mma.getEvent(&event);
  float o = mma.getOrientation();
  String repin=String(digitalRead(buttonPin));
  char rep[repin.length()+1];
//convert readings and publish
  char x[10];
  char y[10];
  char z[10];
  char gyro[4];
  String ms = String(millis());
  char ts[ms.length()+1];
  char out[sizeof(x)+sizeof(y)+sizeof(z)+sizeof(gyro)+sizeof(repin)+sizeof(ts)];
  repin.toCharArray(rep,repin.length()+1);
  ms.toCharArray(ts, ms.length()+1);
  memset(out,0,sizeof(out));
  dtostrf(event.acceleration.x,8,5,x);
  dtostrf(event.acceleration.y,8,5,y);
  dtostrf(event.acceleration.z,8,5,z);
  dtostrf(o,3,1,gyro);
  strcat(out,x);
  strcat(out,",");
  strcat(out,y);
  strcat(out,",");
  strcat(out,z);
  strcat(out,",");
  strcat(out,gyro);
  strcat(out,",");
  strcat(out,rep);
  strcat(out,",");
  strcat(out, ts);

    // CODE TO PROCESS SCREEN MESSAGES
  ////////////////////
  //ISSUE 3 HERE
  ///////////////////
  //When I put the name of the publish path in the "client.publish("/accelerometer/band1")" explicity, it publishes correctly.
  //When I put the name of the publish path in a variable called pubpath, defined above and run "client.publish(pubpath,out,0)", the band crashes
  //I've tried it even without the MAC id, which has colons in it and using the variable reference still causes it to crash
  //Again, assuming it's because of data type
  client.publish("levelup/accel/band1",out,0);

}





