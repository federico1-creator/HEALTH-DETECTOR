int scrittura_new_GPS(int flag)
{

 // modificare lo stato del bottone per non continuare a scrivere su EEPROM
if ((millis() - lt3 > 5000)&&(flag == 1)) // condizione sul tempo e bottone pin=6
{
  lt3= millis();

  // leggo il dato dal sensore e poi devo SCRIVERLO in memoria 
 //leggo dato da GPS
  
  decimale= modf(lat, &intera);
  decimale= int(decimale*10000);
  int lat_1 = int(intera);

  double l1= decimale/100;
  decimale= modf(l1, &intera);
  decimale= int(decimale*100);
  int lat_2 = int(intera);
  int lat_3 = int(decimale);
  // lat_1 , lat_2, lat_3


  decimale= modf(lon, &intera);
  decimale= int(decimale*10000);
  int lon_1 = int(intera);

  double l2= decimale/100;
  decimale= modf(l2, &intera);
  decimale= int(decimale*100);
  int lon_2 = int(intera);
  int lon_3 = int(decimale);
  // lon_1 , lon_2, lon_3
  
  int array1[6] = {lat_1, lat_2, lat_3, lon_1, lon_2, lon_3};

  // scrittura: [0,1,2] [3,4,5]
  for (int i = 0; i < 6; i++)
    EEPROM.write(i, array1[i]);

  // lettura di quello scritto
  for (int i = 0; i < 6; i++)
  {
    letto= EEPROM.read(i);
   // Serial.println(letto); // tolto la descrizione, è il nuovo dato inserito in EEPROM
  }
  digitalWrite(13, HIGH);
  button=LOW;
  return 2;
}
return flag;
}
