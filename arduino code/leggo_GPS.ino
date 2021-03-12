#include "gpsparser.h"

void leggo_GPS(float &a, float &b, int &flag){ // lat, lon (in modo normale)
    // devo assegnare ad A,B i valori estratti della latitudine e longitudine 
    
    char dato;

      while (gpsSerial.available()) {
        char c = gpsSerial.read();

    if (gps.encode(c)) {
      gps.f_get_position(&lat, &lon);

      a = lat;

      b = lon;
      flag = 1;
    }
    /*double longitude,latitude;
    gpsparser(&c,longitude,latitude);
    a= longitude;
    b= latitude;*/
    // da estarrre lat, lon
 }

 

}
