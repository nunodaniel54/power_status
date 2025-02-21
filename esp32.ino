#include <Arduino.h>
#include <ESPSupabase.h>
#include <WiFi.h>

Supabase db;

// Put your supabase URL and Anon key here...
String supabase_url = "https://gfaxitbbwlclnuhqucqi.supabase.co";
String anon_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdmYXhpdGJid2xjbG51aHF1Y3FpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzY0NTkxNDcsImV4cCI6MjA1MjAzNTE0N30.6CaV16yQM1n42BjhaQcLra3Z9_Yw0Mhg9w3x24p8Kuo";

// put your WiFi credentials (SSID and Password) here
/*const char *ssid = "Vodafone-73E840";
const char *psswd = "zHR7pwasb2X3VzWf"; */

const char *ssid = "Net Pena_plus";
const char *psswd = "pass2023";

#define uS_TO_S_FACTOR 1000000  /* Conversion factor for micro seconds to seconds */
#define TIME_TO_SLEEP  200        /* Time ESP32 will go to sleep (in seconds)  10 minutos */
// Put your target table here
String table = "wake_up";
String JSON = "{\"notification\":\"0\"}";

void setup()
{ // Serial.begin(115200);
  esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);
  //Serial.println("Acordou");
}

void loop()
{ 
 if(enableWiFi()){
      do_sequence();
      delay(10000);
 }
  hibernate();
}

void do_sequence(){
 // Serial.println(JSON); 
  db.begin(supabase_url, anon_key);
  int code = db.insert(table, JSON, false);
  db.urlQuery_reset();
  Serial.println("Heart Beat created");

}


int enableWiFi(){
    WiFi.disconnect(false);  // Reconnect the network
    WiFi.mode(WIFI_STA);    // Switch WiFi off
    Serial.begin(9600);
    WiFi.begin(ssid, psswd);
    int i =0;

    while (WiFi.status() != WL_CONNECTED) {
      if(i > 20){
        return 0;
      }
        delay(500);
        i = i+1;
        Serial.println("Connecting to wifi ...");
    }
    return 1;
}

void hibernate() {
    esp_sleep_pd_config(ESP_PD_DOMAIN_RTC_PERIPH,   ESP_PD_OPTION_OFF);
    esp_sleep_pd_config(ESP_PD_DOMAIN_RTC_SLOW_MEM, ESP_PD_OPTION_OFF);
    esp_sleep_pd_config(ESP_PD_DOMAIN_RTC_FAST_MEM, ESP_PD_OPTION_OFF);
    esp_sleep_pd_config(ESP_PD_DOMAIN_XTAL,         ESP_PD_OPTION_OFF);
    //esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);
    esp_deep_sleep_start();
}
