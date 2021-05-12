/*
If you are using device first time i.e. if device is not set yet, put pin 16(D0) to HIGH to configure esp8266 and after configure set the pin to LOW.
If you want to reset the device using pin, make HIGH pin 5(D1) for 5 sec. else keep it LOW. 
In hotspot mode SSID is "Robato" and password is "12345678". Local ip to connect web page is 192.168.4.1
To control appliance publish msg on topic RoomName/DeviceName and Msg format will be 
{"Username":"abcd", "AccessKey":"xyz", "Location":"xyz", "Appliance":"ApplianceName", "state”:"0/1.."}
For example: {"Username":"abcd", "AccessKey":"xyz", "Location":"xyz", "Appliance":"Fan2", "state”:"0"}
Device will send acknowledgement on topic status/RoomName/DeviceName.
To turn off all appliance attached with a device, Msg format will be {"Username":"abcd", "AccessKey":"xyz", "Location":"xyz", "Appliance":"ALL", "state":"0"}
To reset the device by using msg, Msg format will be {"Username":"abcd", "AccessKey":"xyz", "Location":"xyz", "Appliance":"device", "state":"0"}
*/

#include <FS.h>   
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ESP8266WebServer.h>
#include <ArduinoJson.h> 
#include <PubSubClient.h>
 
//Variables
int i = 0;
int statusCode;
const char* ssid = "text";
const char* passphrase = "text";
String st;
String content;

// Gateway details
char wifi_ssid[32] = "wifi_ssid";
char wifi_pass[32] = "wifi_pass";
char mqtt_server[40];
char mqtt_username[34] = "username";
char mqtt_password[40] = "qpassword";
char device_name[20] = "device_name";
char room_name[20] = "Room_name";
char Location[32] = "Location";

 char* passo = "pass123val";

// Pin details configuration

//Connect appliances on these pins
unsigned int plug1 = 12;  //D6
unsigned int plug2 = 13;  //D7
unsigned int plug3 = 14;  //D5
unsigned int plug4 = 15;  //D8

// plug states
char plug1_state[4] = "0";
char plug2_state[4] = "0";
char plug3_state[4] = "0";
char plug4_state[4] = "0";

// Appliances
char Appliance1[20] = "App1";
char Appliance2[20] = "App2";
char Appliance3[20] = "App3";
char Appliance4[20] = "App4";

//Function Decalration
bool testWifi(void);
void launchWeb(void);
void setupAP(void);

//initial pin state
char* init_state = "0";
char* init_pin = "ALL";

String topic_input = "";

char pin_state[8] = "0";
char Appliance[8] = "0";
char pub_client[20] = "client";

String creat_pub_topic = "";

char data[150]= "data";

char Access_key[32]="abcd";
char user_loc[32] = "Loc";
bool shouldSaveConfig = false;
 
//Establishing Local server at port 80 whenever required
ESP8266WebServer server(80);
WiFiClient espClient3;
PubSubClient client(espClient3);


// Function to execute prev state of plugs
void prev_state(unsigned int plugs, char* plugstate){
  Serial.print("Prev state of plug is: ");
  Serial.println(plugstate);
analogWrite(plugs, atoi(plugstate)*100);
}

// Setup function
void setup()
{
  Serial.begin(115200);
Serial.println("delay start");
 delay(5000);
 
   //Initialising if(DEBUG)Serial Monitor
  Serial.println();
  delay(1000);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(16, INPUT);
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
  pinMode(14, OUTPUT);
  pinMode(15, OUTPUT);

Serial.println("Starting up the device");

 ////Uncomment it only if you want to delete config file from EEPROM (Factory rest)
   //SPIFFS.format();
   if (SPIFFS.begin()) {
   if(digitalRead(16)==0){

    Serial.println("mounted file system");
    if (SPIFFS.exists("/config.json")) {
      
      //file exists, reading and loading
      Serial.println("reading config file");
      File configFile = SPIFFS.open("/config.json", "r");
      if (configFile) {
        Serial.println("opened config file");
        
  // Creating a json document to deserialize the saved data
        const size_t capacity = JSON_OBJECT_SIZE(16)+400;  
        DynamicJsonDocument json_read(capacity);
        //jsonBuff.to<JsonArray>();
        DeserializationError err = deserializeJson(json_read, configFile);
      if (err) {
        // if json document does not open, give the error.
        Serial.print(F("deserializeJson() failed with code "));
        Serial.println(err.c_str());
      }
      
      else {
Serial.println("Getting prev saved data and copying it to variables");

Serial.println("Copying ssid");
          strcpy(wifi_ssid, json_read["qsid"]);        // Copying wifi ssid
          Serial.println("Copying password");
          strcpy(wifi_pass, json_read["qpass"]);       // Copying wifi password
          Serial.println("Copying gateway address");
          strcpy(mqtt_server, json_read["GatewayAdd"]);       // Copying mqtt_server 
          Serial.println("Copying username");
          strcpy(mqtt_username, json_read["Username"]);   // Copying mqtt_username
          Serial.println("Copying userpass");
          strcpy(mqtt_password, json_read["Userpass"]);  // Copying mqtt_password
          Serial.println("Copying location");
          strcpy(Location, json_read["Location"]);     //Copying device location
          Serial.println("Copying room name");
          strcpy(room_name, json_read["Room"]);       // Copying room name
          Serial.println("Copying device name");
          strcpy(device_name, json_read["Device"]);    // Copying device name
          
Serial.println("Copying appliances");                  //Copying appliance name
          strcpy(Appliance1, json_read["Appliance1"]);
          strcpy(Appliance2, json_read["Appliance2"]);
          strcpy(Appliance3, json_read["Appliance3"]);
          strcpy(Appliance4, json_read["Appliance4"]);
 
Serial.println("Copying plug states");
// Copying states of the plugs i.e. ON or OFF.
          strcpy(plug1_state, json_read["plug1_state"]);     // copying state of plug 1
          strcpy(plug2_state, json_read["plug2_state"]);     // copying state of plug 2
          strcpy(plug3_state, json_read["plug3_state"]);     // copying state of plug 3
          strcpy(plug4_state, json_read["plug4_state"]);     // copying state of plug 4

// Calling previous state of plugs

 Serial.println("Calling prev_state");
          delay(1000);
          prev_state(plug1, plug1_state);
          delay(200);
          prev_state(plug2, plug2_state);
          delay(200);
          prev_state(plug3, plug3_state);
          delay(200);
          prev_state(plug4, plug4_state);
          Serial.println("copied all the data");
          delay(3000);
 }
        }
        configFile.close();      // closing config file.
      
    
   

//********************************************************************************

// If pin 16 is low start wi-fi and connect to mqtt broker
 
  WiFi.begin(wifi_ssid, wifi_pass);
  testWifi();
  
    Serial.println("Succesfully Connected!!!");
    WiFi.softAPdisconnect (true);
     Serial.println("local ip");
  Serial.println(WiFi.localIP());
  client.setServer(mqtt_server,1884);
  client.setCallback(callback);
    return;
   }
   else{
    Serial.println("No Config.json file exist in memory please connect pin 16 (D0) to 3V3 and press reset button to configure the Device");
   }
   }  

// Else if pin 16 is high, go into hotspot mode
  else if(digitalRead(16)==1)
  {
    SPIFFS.format();
    Serial.println("Turning the HotSpot On");
    launchWeb();
    setupAP();// Setup HotSpot
  }
 
  Serial.println();
  Serial.println("Waiting.");
  
  while ((WiFi.status() != WL_CONNECTED))
  {
    Serial.print(".");
    delay(100);
    server.handleClient();
  }
 
}
else {
    Serial.println("failed to mount FS");
  }
}

//*****************************************************************************
void loop() {

  if (!client.connected()) {
    reconnect();
  }
 client.loop(); 

}

//*****************************************************************************
 
 
//-------- Fuctions used for WiFi credentials saving and connecting to it which you do not need to change 
bool testWifi(void){
  int c = 0;
  Serial.println("Waiting for Wifi to connect");
  while ( c < 20 ) {
    if (WiFi.status() == WL_CONNECTED)
    {
      return true;
    }
    delay(500);
    Serial.print("*");
    c++;
  }
  Serial.println("");
  Serial.println("Connect timed out, opening AP");
  return false;
}

//***********************************************************************************
//Function to launch web server
void launchWeb(){
  Serial.println("");
  if (WiFi.status() == WL_CONNECTED)
    Serial.println("WiFi connected");
  Serial.print("Local IP: ");
  Serial.println(WiFi.localIP());
  Serial.print("SoftAP IP: ");
  Serial.println(WiFi.softAPIP());
  createWebServer();
  // Start the server
  server.begin();
  Serial.println("Server started");
}

//*********************************************************************************
//Function to set up AP
void setupAP(void){
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);
  int n = WiFi.scanNetworks();
  Serial.println("scan done");
  if (n == 0)
    Serial.println("no networks found");
  else
  {
    Serial.print(n);
    Serial.println(" networks found");
    for (int i = 0; i < n; ++i)
    {
      // Print SSID and RSSI for each network found
      Serial.print(i + 1);
      Serial.print(": ");
      Serial.print(WiFi.SSID(i));
      Serial.print(" (");
      Serial.print(WiFi.RSSI(i));
      Serial.print(")");
      Serial.println((WiFi.encryptionType(i) == ENC_TYPE_NONE) ? " " : "*");
      delay(10);
    }
  }
  Serial.println("");
  st = "<ol>";
  for (int i = 0; i < n; ++i)
  {
    // Print SSID and RSSI for each network found
    st += "<li>";
    st += WiFi.SSID(i);
    st += " (";
    st += WiFi.RSSI(i);
 
    st += ")";
    st += (WiFi.encryptionType(i) == ENC_TYPE_NONE) ? " " : "*";
    st += "</li>";
  }
  st += "</ol>";
  delay(100);

 // Set wifi hotspot ssid and password WiFi.softAP("SSID", "Password");
  WiFi.softAP("Robato", "12345678");
  Serial.println("softap");
  launchWeb();
  Serial.println("over");
}

//************************************************************************************
void createWebServer(){
 
    server.on("/", []() {
 
      IPAddress ip = WiFi.softAPIP();
      String ipStr = String(ip[0]) + '.' + String(ip[1]) + '.' + String(ip[2]) + '.' + String(ip[3]);
      content = "<!DOCTYPE HTML>\r\n<html>Hello from Robato Systems ";
      content += "<form action=\"/scan\" method=\"POST\"><input type=\"submit\" value=\"scan\"></form>";
      content += ipStr;
      content += "<p>";
      content += st;
      
      content += "</p><form method='get' action='setting'><label>SSID: </label>";
      content += "<select name='ssid' length=32>";
      int n = WiFi.scanNetworks();
      for (int i = 0; i < n; ++i){
        content += "<option value='"+ WiFi.SSID(i) +"'>"+ WiFi.SSID(i) +"</option>"  ;
      }
      content += "</select><br>";
      content += "<label for='password'>Password:</label><br>";
      content += "<input name='password' length=64 value='";
      content += String(wifi_pass); 
      content += "'><br>";
      
// Creating option room and giving options to select
      content += "<label for='Room'>Choose Room:</label><br>";
      content += "<select name='Room' length=32>";
      content += "<option value='Kitchen'>Kitchen</option>";
      content += "<option value='Bedroom'>Bedroom</option>";
      content += "<option value='Hall'>Hall</option>";
      content += "<option value='Lobby'>Lobby</option>";
      content += "<option value='GuestRoom'>GuestRoom</option>";
      content += "<option value='Bathroom'>Bathroom</option>";
      content += "</select><br>";

// Creating option Device and giving options to select
      content += "<label for='Device'>Choose Device:</label><br>";
      content += "<select name='Device' length=32>";
      content += "<option value='Device1'>Device1</option>";
      content += "<option value='Device2'>Device2</option>";
      content += "<option value='Device3'>Device3</option>";
      content += "<option value='Device4'>Device4</option>";
      content += "<option value='Device5'>Device5</option>";
      content += "<option value='Device6'>Device6</option>";
      content += "</select><br>";
      
//Creating box to take input Location
      content += "<label for='Location'>Location:</label><br>";
      content += "<input name='Location' length=64 value='";
      content += String(Location); 
      content += "'><br>";
      
//Creating box to take input Gateway address i.e. raspberry pi ip address
      content += "<label for='GatewayAdd'>Gateway Address:</label><br>";
      content += "<input name='GatewayAdd' length=64 value='";
      content += String(mqtt_server); 
      content += "'><br>";

//Creating box to take input mqtt username
      content += "<label for='Username'>Username:</label><br>";
      content += "<input name='Username' length=64 value='";
      content += String(mqtt_username); 
      content += "'><br>";
     
//Creating box to take input mqtt password
      content += "<label for='Userpass'>User password:</label><br>";
      content += "<input name='Userpass' length=64 value='";
      content += String(mqtt_password); 
      content += "'><br>";
      
// Creating option Appliance1 and giving options to select
      content += "<label for='Appliance1'>Choose Appliance1:</label><br>";
      content += "<select name='Appliance1' length=32>";
      content += "<option value='Light1'>Light1</option>";
      content += "<option value='Light2'>Light2</option>";
      content += "<option value='Light3'>Light3</option>";
      content += "<option value='Light4'>Light4</option>";
      content += "<option value='Light5'>Light5</option>";
      content += "<option value='Light6'>Light6</option>";
      content += "<option value='Light7'>Light7</option>";
      content += "<option value='Light8'>Light8</option>";
      content += "<option value='Light9'>Light9</option>";
      content += "<option value='Light10'>Light10</option>";
      content += "<option value='Light11'>Light11</option>";
      content += "<option value='Light12'>Light12</option>";
      content += "<option value='Light13'>Light13</option>";
      content += "<option value='Light14'>Light14</option>";
      content += "<option value='Light15'>Light15</option>";
      
      content += "<option value='Fan1'>Fan1</option>";
      content += "<option value='Fan2'>Fan2</option>";
      content += "<option value='Fan3'>Fan3</option>";
      content += "<option value='Fan4'>Fan4</option>";
      content += "<option value='Fan5'>Fan5</option>";
      content += "<option value='Fan6'>Fan6</option>";
      content += "<option value='Fan7'>Fan7</option>";
      content += "<option value='Fan8'>Fan8</option>";
      content += "<option value='Fan9'>Fan9</option>";
      content += "<option value='Fan10'>Fan10</option>";
      content += "<option value='Fan12'>Fan12</option>";
      content += "<option value='Fan13'>Fan13</option>";
      content += "<option value='Fan14'>Fan14</option>";
      content += "<option value='Fan15'>Fan15</option>";
      content += "<option value='Fan16'>Fan16</option>";
      
      content += "<option value='Television'>Television</option>";
      content += "<option value='Microwave'>Microwave</option>";
      content += "</select><br>";

// Creating option Appliance2 and giving options to select
      content += "<label for='Appliance2'>Choose Appliance2:</label><br>";
      content += "<select name='Appliance2' length=32>";
      content += "<option value='Light1'>Light1</option>";
      content += "<option value='Light2'>Light2</option>";
      content += "<option value='Light3'>Light3</option>";
      content += "<option value='Light4'>Light4</option>";
      content += "<option value='Light5'>Light5</option>";
      content += "<option value='Light6'>Light6</option>";
      content += "<option value='Light7'>Light7</option>";
      content += "<option value='Light8'>Light8</option>";
      content += "<option value='Light9'>Light9</option>";
      content += "<option value='Light10'>Light10</option>";
      content += "<option value='Light11'>Light11</option>";
      content += "<option value='Light12'>Light12</option>";
      content += "<option value='Light13'>Light13</option>";
      content += "<option value='Light14'>Light14</option>";
      content += "<option value='Light15'>Light15</option>";
      
      content += "<option value='Fan1'>Fan1</option>";
      content += "<option value='Fan2'>Fan2</option>";
      content += "<option value='Fan3'>Fan3</option>";
      content += "<option value='Fan4'>Fan4</option>";
      content += "<option value='Fan5'>Fan5</option>";
      content += "<option value='Fan6'>Fan6</option>";
      content += "<option value='Fan7'>Fan7</option>";
      content += "<option value='Fan8'>Fan8</option>";
      content += "<option value='Fan9'>Fan9</option>";
      content += "<option value='Fan10'>Fan10</option>";
      content += "<option value='Fan12'>Fan12</option>";
      content += "<option value='Fan13'>Fan13</option>";
      content += "<option value='Fan14'>Fan14</option>";
      content += "<option value='Fan15'>Fan15</option>";
      content += "<option value='Fan16'>Fan16</option>";
      
      content += "<option value='Television'>Television</option>";
      content += "<option value='Microwave'>Microwave</option>";
      content += "</select><br>";

// Creating option Appliance3 and giving options to select
      content += "<label for='Appliance3'>Choose Appliance3:</label><br>";
      content += "<select name='Appliance3' length=32>";
      content += "<option value='Light1'>Light1</option>";
      content += "<option value='Light2'>Light2</option>";
      content += "<option value='Light3'>Light3</option>";
      content += "<option value='Light4'>Light4</option>";
      content += "<option value='Light5'>Light5</option>";
      content += "<option value='Light6'>Light6</option>";
      content += "<option value='Light7'>Light7</option>";
      content += "<option value='Light8'>Light8</option>";
      content += "<option value='Light9'>Light9</option>";
      content += "<option value='Light10'>Light10</option>";
      content += "<option value='Light11'>Light11</option>";
      content += "<option value='Light12'>Light12</option>";
      content += "<option value='Light13'>Light13</option>";
      content += "<option value='Light14'>Light14</option>";
      content += "<option value='Light15'>Light15</option>";
      
      content += "<option value='Fan1'>Fan1</option>";
      content += "<option value='Fan2'>Fan2</option>";
      content += "<option value='Fan3'>Fan3</option>";
      content += "<option value='Fan4'>Fan4</option>";
      content += "<option value='Fan5'>Fan5</option>";
      content += "<option value='Fan6'>Fan6</option>";
      content += "<option value='Fan7'>Fan7</option>";
      content += "<option value='Fan8'>Fan8</option>";
      content += "<option value='Fan9'>Fan9</option>";
      content += "<option value='Fan10'>Fan10</option>";
      content += "<option value='Fan12'>Fan12</option>";
      content += "<option value='Fan13'>Fan13</option>";
      content += "<option value='Fan14'>Fan14</option>";
      content += "<option value='Fan15'>Fan15</option>";
      content += "<option value='Fan16'>Fan16</option>";
      
      content += "<option value='Television'>Television</option>";
      content += "<option value='Microwave'>Microwave</option>";
      content += "</select><br>";
       
// Creating option Appliance4 and giving options to select
      content += "<label for='Appliance4'>Choose Appliance4:</label><br>";
      content += "<select name='Appliance4' length=32>";
      content += "<option value='Light1'>Light1</option>";
      content += "<option value='Light2'>Light2</option>";
      content += "<option value='Light3'>Light3</option>";
      content += "<option value='Light4'>Light4</option>";
      content += "<option value='Light5'>Light5</option>";
      content += "<option value='Light6'>Light6</option>";
      content += "<option value='Light7'>Light7</option>";
      content += "<option value='Light8'>Light8</option>";
      content += "<option value='Light9'>Light9</option>";
      content += "<option value='Light10'>Light10</option>";
      content += "<option value='Light11'>Light11</option>";
      content += "<option value='Light12'>Light12</option>";
      content += "<option value='Light13'>Light13</option>";
      content += "<option value='Light14'>Light14</option>";
      content += "<option value='Light15'>Light15</option>";
      
      content += "<option value='Fan1'>Fan1</option>";
      content += "<option value='Fan2'>Fan2</option>";
      content += "<option value='Fan3'>Fan3</option>";
      content += "<option value='Fan4'>Fan4</option>";
      content += "<option value='Fan5'>Fan5</option>";
      content += "<option value='Fan6'>Fan6</option>";
      content += "<option value='Fan7'>Fan7</option>";
      content += "<option value='Fan8'>Fan8</option>";
      content += "<option value='Fan9'>Fan9</option>";
      content += "<option value='Fan10'>Fan10</option>";
      content += "<option value='Fan12'>Fan12</option>";
      content += "<option value='Fan13'>Fan13</option>";
      content += "<option value='Fan14'>Fan14</option>";
      content += "<option value='Fan15'>Fan15</option>";
      content += "<option value='Fan16'>Fan16</option>";
      
      content += "<option value='Television'>Television</option>";
      content += "<option value='Microwave'>Microwave</option>";
      content += "</select><br>";

// Option to submit form
      content += "<br><input type='submit'></form>";

      content += "</html>";
      server.send(1500, "text/html", content);
      });
      server.on("/scan", []() {
//setupAP();
      IPAddress ip = WiFi.softAPIP();
      String ipStr = String(ip[0]) + '.' + String(ip[1]) + '.' + String(ip[2]) + '.' + String(ip[3]);
 
      content = "<!DOCTYPE HTML>\r\n<html>go back";
      server.send(200, "text/html", content);
      });

// Copying data provided by user to varibles.
      server.on("/setting", []() {
      String qsid = server.arg("ssid");
      String qpass = server.arg("password");
      String Room = server.arg("Room");
      String Device = server.arg("Device");
      String Location = server.arg("Location");
      String GatewayAdd = server.arg("GatewayAdd");
      String Username = server.arg("Username");
      String Userpass = server.arg("Userpass");
      String Appl1_name = server.arg("Appliance1");
      String Appl2_name = server.arg("Appliance2");
      String Appl3_name = server.arg("Appliance3");
      String Appl4_name = server.arg("Appliance4");
      
      
      if (qsid.length() > 0 && qpass.length() > 0) {
       
        

        Serial.print("SSID is: ");
        Serial.println(qsid);
        Serial.print("Password is: ");
        Serial.println(qpass);
        Serial.print("Romm name is: ");
        Serial.println(Room);
        Serial.print("Device name is: ");
        Serial.println(Device);
        Serial.print("Location is: ");
        Serial.println(Location);
        Serial.print("Username is: ");
        Serial.println(Username);
        Serial.print("Userpass is: ");
        Serial.println(Userpass);
        Serial.print("Appliance1 is: ");
        Serial.println(Appl1_name);
        Serial.print("Appliance2 is: ");
        Serial.println(Appl2_name);
        Serial.print("Appliance3 is: ");
        Serial.println(Appl3_name);
        Serial.print("Appliance4 is: ");
        Serial.println(Appl4_name);
       
 // Saving data into fs memory
//cleaning FS and writing data
        Serial.println("Clearing FS");
        SPIFFS.format();
        delay(1000);
 const size_t capacity = JSON_OBJECT_SIZE(16)+400;
    DynamicJsonDocument json_write(capacity);

    json_write["qsid"] = qsid;
    json_write["qpass"] = qpass;
    json_write["Room"] = Room;
    json_write["Device"] = Device;
    json_write["Location"] = Location;
    json_write["GatewayAdd"] = GatewayAdd;
    json_write["Username"] = Username;
    json_write["Userpass"] = Userpass;
    json_write["Appliance1"] =  Appl1_name;
    json_write["Appliance2"] = Appl2_name;
    json_write["Appliance3"] = Appl3_name;
    json_write["Appliance4"] = Appl4_name;
    Serial.println("opening config file for writing");
    File configFile = SPIFFS.open("/config.json", "w");
    if (!configFile) {
      Serial.println("failed to open config file for writing");
    }
    serializeJson(json_write, configFile);    // write json objects to config file
    serializeJson(json_write, Serial);        // write json opjects on Serial monitor.
    configFile.close();
    update_state_file(init_pin,init_state);
     Serial.println("\n \n config file written succesfully, Now please connect pin D0 to GND and press reset fast in less than 6 seconds");
    //end sav
   
        content = "{\"Success\":\"saved to eeprom... reset to boot into new wifi\"}";
        statusCode = 200;
        delay(6000);
        ESP.restart();
      } else {
        content = "{\"Error\":\"404 not found\"}";
        statusCode = 404;
        Serial.println("Sending 404");
      }
      server.sendHeader("Access-Control-Allow-Origin", "*");
      server.send(statusCode, "application/json", content);
 
    });
  } 


//********************************************************************************
//Function to update pin state in ESP8266 memory i.e. in FS.
void update_state_file(char*m,char*n){

// if value of variable m is equal to value of plug 1 then
    if(atoi(m)==plug1){
    Serial.println("updating plug 1 state in json file");
    strcpy(plug1_state, n);
  }
  else if(atoi(m)==plug2){
    Serial.println("updating plug 2 state in json file");
    strcpy(plug2_state, n);
  }
  else if(atoi(m)==plug3){
    Serial.println("updating plug 3 state in json file");
    strcpy(plug3_state, n);
  }
  else if(atoi(m)==plug4){
    Serial.println("updating plug 4 state in json file");
    strcpy(plug4_state, n);
  }
// If msg arrived is to turn of all appliance.
  else if (String(m)=="ALL"){
    if (String(n)=="0"){
      strcpy(plug1_state, n);
      strcpy(plug2_state, n);
      strcpy(plug3_state, n);
      strcpy(plug4_state, n);
    }
  }

// Opening saved file to update data
 File file = SPIFFS.open("/config.json", "r"); 
  const size_t capacity = JSON_OBJECT_SIZE(16)+400;
  DynamicJsonDocument doc2(capacity);

DeserializationError err = deserializeJson(doc2, file);
      if (err) {
        Serial.print(F("deserializeJson() update failed with code "));
        Serial.println(err.c_str());
      }
      else {
Serial.println("updating data");
       doc2["plug1_state"] = plug1_state;
       doc2["plug2_state"] = plug2_state; 
       doc2["plug3_state"] = plug3_state;
       doc2["plug4_state"] = plug4_state;   
      }

file.close();

File file1 = SPIFFS.open("/config.json", "w");
Serial.println("updated the state of plug.");
serializeJson(doc2, file1);
serializeJson(doc2, Serial);
file1.close();
Serial.println();
}
//************************************************************************************


//function to publish mqtt msg, i.e. acknowledgement
char dataPublish[150];
String datasensor;
void publishMQTT(char* topics, String data){
   data.toCharArray(dataPublish, data.length() + 1);
   client.publish(topics, dataPublish);
}

//************************************************************************************
// Function to connect MQTT broker
void reconnect(){ 

//Creating topic to subscribe msg
  topic_input = String(room_name) + "/" + String(device_name);
char *topic_sub = new char[topic_input.length() + 1];
strcpy(topic_sub, topic_input.c_str());

  while(!client.connected()){                     // MQTT Begin

// Creating topic to subscribe from room_name and device_name. topic will be "Room_name/device_name".

    

    Serial.println("Connecting to MQTT Server..");
    Serial.print("IP MQTT Server : ");
    Serial.print(mqtt_server);
    Serial.print("  username: ");
    Serial.print(mqtt_username);
    Serial.print("  password: ");
    Serial.print(mqtt_password);
    Serial.print("  topic:");
    Serial.println(topic_sub);
    
// Connect to gateway   
 if (client.connect(device_name, mqtt_username, mqtt_password )) {
 
      Serial.println("connected");
      digitalWrite(LED_BUILTIN, HIGH);


// Publishing device configuration to gateway when device restart.
creat_pub_topic = "configure/"+String(room_name) + "/" + String(device_name);
   char *topic_pub = new char[creat_pub_topic.length() + 1];
   strcpy(topic_pub, creat_pub_topic.c_str());

// Creating Json msg
    const size_t capacity = JSON_OBJECT_SIZE(12)+400; //Declaring msg size
    DynamicJsonDocument doc(capacity);
    //doc["Username"] = mqtt_username;
   // doc["Location"] = Location;
    doc["Room"] = room_name;
    doc["Device"] = device_name;
    doc["Appliance1"] =Appliance1;
    doc["Appliance2"] =Appliance2;
    doc["Appliance3"] =Appliance3;
    doc["Appliance4"] =Appliance4;
  serializeJson(doc, data);
  
//Converting msg into string
        datasensor = String(data);
        Serial.print("publishing device configuration to gateway.");
        Serial.println(datasensor);
        publishMQTT(topic_pub,datasensor);

      
     int qos_level= 1;  
//Subscribing topic RoomName/DeviveName with qos=0
      client.subscribe(topic_sub,qos_level);
    } else {
      Serial.println(client.state());
     
     // delay(1000);
      Serial.println("Try to connect...");
    }
  }
}


//************************************************************************************
//Reading message and working accoprdingly
//Msg format will be {"Username":"username",  "AccessKey":"xyz", "Location":"Mumbai", "Appliance":"ApplianceName", "state”:"0/1.."}
//0 to OFF and 5 to ON 

void callback(char* topic, byte* payload, unsigned int length) {

// Creating topic to subscribe
// Msg should me published on topic RoomNmae/DeviceName
       topic_input = String(room_name) + "/" + String(device_name);
       char *topic_sub = new char[topic_input.length() + 1];
       strcpy(topic_sub, topic_input.c_str());

       Serial.print("Message arrived in topic: ");
       Serial.println(topic);


Serial.print(". Message: ");
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
    messageTemp += (char)payload[i];
  }
  Serial.println();

  
       
       StaticJsonDocument<256> doc1;
// Reading message arrived
      DeserializationError err = deserializeJson(doc1, payload, length);
      if (err) {
        Serial.print(F("deserializeJson() failed with code "));
        Serial.println(err.c_str());
      }
      else {
// Copying msg data to variables
strcpy(Access_key, doc1["AccessKey"]);    // Copying Accesskey
strcpy(user_loc, doc1["Location"]);       // Copying Location of user who published data  
strcpy(pin_state,doc1["state"]);         // Copying state from the message to variable pin_state
strcpy(Appliance, doc1["Appliance"]);    // Copying appliance name
strcpy(pub_client, doc1["Username"]);    // Copying username who published data
Serial.print("Message published by: ");
Serial.print(pub_client);
Serial.print(" for: ");
Serial.print(Appliance);       
Serial.print("to change state to: ");
Serial.println(pin_state);
      }
  
 
//Code to ON/OFF appliance. 0 to OFF and 5 to ON
if (String(topic) == String(topic_sub)) {
    Serial.print("Changing output of ");
    Serial.print(Appliance);

// If msg arrived for appliance 1 then
    if(String(Appliance) == String(Appliance1)){ 
      
// writing analog pin  
       analogWrite(plug1, atoi(pin_state)*200);
       
//Converting int plug to char
          char c[4];
sprintf(c, "%d", plug1);

//upadting state of plug in ESP8266 memory
      update_state_file(c,pin_state);
      
//Publishing ack
      acknowledgement(pub_client, Appliance, pin_state, Access_key, user_loc);
    }
    
//Above process is apllied for other appliances
    else if(String(Appliance) == String(Appliance2)){
         analogWrite(plug2, atoi(pin_state)*200);
         char c[4];
         sprintf(c, "%d", plug2);
         update_state_file(c,pin_state);
         acknowledgement(pub_client, Appliance, pin_state, Access_key, user_loc);
      }


    else if(String(Appliance) == String(Appliance3)){
         analogWrite(plug3, atoi(pin_state)*200);
         char c[4];
         sprintf(c, "%d", plug3);
         update_state_file(c,pin_state);
         acknowledgement(pub_client, Appliance, pin_state, Access_key, user_loc);
      }


  
    else if(String(Appliance) == String(Appliance4)){
         analogWrite(plug4, atoi(pin_state)*200);
         char c[4];
         sprintf(c, "%d", plug4);
         update_state_file(c,pin_state);
         acknowledgement(pub_client, Appliance, pin_state, Access_key, user_loc);
      }

    
    
// Turn OFF all the appliance
//Msg format will be {"Username":"abcd", "AccessKey":"xyz", "Location":"xyz", "Appliance":"ALL", "state":"0"}
    else if (String(Appliance) == "ALL"){
        if (String(pin_state) == "0"){          
        analogWrite(plug1, atoi(pin_state)*100);
        analogWrite(plug2, atoi(pin_state)*100);
        analogWrite(plug3, atoi(pin_state)*100);
        analogWrite(plug4, atoi(pin_state)*100);
        update_state_file(Appliance,pin_state);
        acknowledgement(pub_client, Appliance, pin_state, Access_key, user_loc);
      }
    }
    
// Reset the device using sending msg
    else if (String(Appliance) == "device"){         // Msg format will be {"Username":"abcd",  "AccessKey":"xyz", "Location":"xyz", "Appliance":"device", "state":"0"}
      if (String(pin_state) == "0"){
      Serial.print("RESETTING THE DEVICE ");
      delay(1000);
      SPIFFS.format();
      delay(1000);
      ESP.restart();
   }  
  }
 }
}

//**********************************************************************************
//  Function to send acknowledgement msg on topic status/RoomName/DeviceName
// Msg will be in the form {"Username":"abcd", "AccessKey":"xyz", "Location":"xyz", "Appliance":"ApplianceName", "state":"0/1.."}

void acknowledgement(char* pub_client, char* pin, char* pinstate, char* Accesskey, char* Location){

// Creating topic for publishing ack
   creat_pub_topic = "ack/"+String(room_name) + "/" + String(device_name);
   char *topic_pub = new char[creat_pub_topic.length() + 1];
   strcpy(topic_pub, creat_pub_topic.c_str());

// Creating Json msg
    const size_t capacity = JSON_OBJECT_SIZE(12)+400; //Declaring msg size
    DynamicJsonDocument doc(capacity);
    doc["Username"] = pub_client;
    doc["AccessKey"] = Accesskey;
    doc["Location"] = Location;
    doc["Appliance"] = pin;
    doc["state"] = pinstate;
 
   serializeJson(doc, data);
  
//Converting msg into string
        datasensor = String(data);
    Serial.print("publishing acknowledgement: ");
    Serial.println(datasensor);
   
    publishMQTT(topic_pub,datasensor);
}