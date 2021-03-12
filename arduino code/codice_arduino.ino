// cosa c'è ora in EEPROM (lettura scrittura.ino) --> tutto 0
// creato pulsante sulla breadboard
// provare il funzionamento
// dividere il file in più tab (che creano un unico file sorgente)

# include <math.h>
# include <EEPROM.h>
#include <Wire.h>
#include <Adafruit_MLX90614.h>
#include "MAX30100_PulseOximeter.h"
#include <TinyGPS.h>
#include <SoftwareSerial.h>

#define REPORTING_PERIOD_MS     1000
 
PulseOximeter pox;
uint32_t tsLastReport = 0;
Adafruit_MLX90614 mlx = Adafruit_MLX90614(0x5a);


// DA CAMBIARE PIN
SoftwareSerial gpsSerial(10, 11); //3: esce come TX e diventa RX
TinyGPS gps;

// dati sintetici
int battito; //=48; // da 50 a 180        
int ossigeno; //= 85; // minore di 100
double t; //= 34; // tra 31 e 43, esclusi
double resto, temp;

//servono per prendere i dati da scrivere sulla memoria
float lat; //= 43.823761; //44.494297;
float lon; //= 11.193472; //11.342021;
double decimale, intera;

int button=0; // è lo stato del bottone
const int bottone= 6;

int letto;
int i;
int iState;
int flag=0;

unsigned long lt1;
unsigned long lt2;;
unsigned long lt3;


void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
  pinMode(13,OUTPUT);
  digitalWrite(13, LOW);
  pinMode(12,OUTPUT);
  digitalWrite(12, LOW);
  pinMode(bottone, INPUT);
  gpsSerial.begin(9600);
  mlx.begin();
  
  iState=0;
  lt1= millis();
  lt2= millis();
  lt3= millis();
  i=0;  //inizializzo
  if (!pox.begin()) 
      for(;;);

  
}

void loop() {
button= digitalRead(bottone);

dati_generici();

dati_GPS();
if( flag != 2){
leggo_GPS(lat, lon, flag); }
flag = scrittura_new_GPS(flag);

stato_salute();

// non aggiunge niente
  
}
