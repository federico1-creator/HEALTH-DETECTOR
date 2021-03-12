void dati_GPS(){
  // scrivo i dati sulla seriale
  if (millis() - lt2 > 2500 && i==0)
{
  lt2= millis();
  ///////////////////
  // vado a leggere in memoria
  int array2[6];

  for (int i = 0; i < 6; i++)
    array2[i] = EEPROM.read(i);

  // print the results to the Serial Monitor: 8
  Serial.write(0xff);
  Serial.write(0x06);
  Serial.write(array2[0]);  // lat
  Serial.write(array2[1]);
  Serial.write(array2[2]);
  Serial.write(array2[3]);  // lon
  Serial.write(array2[4]);
  Serial.write(array2[5]);

  // (int) (char)
  //Serial.write((char)(map(sensorValue1,0,1024,0,253)));
  //Serial.write((char)(map(sensorValue2,0,1024,0,253)));
  Serial.write(0xfe);
  i++;  
}
}

/*   
  // DA TOGLIERE
  // read, attenzione al tempo per la conversione se il dato è analogico
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

  
  // print the results to the Serial Monitor: 8
  Serial.write(0xff);
  Serial.write(0x06);
  Serial.write(int(lat_1));  // lat
  Serial.write(int(lat_2));
  Serial.write(int(lat_3));
  Serial.write(lon_1); // lon
  Serial.write(lon_2);
  Serial.write(lon_3);
    
  // (int) (char)
  //Serial.write((char)(map(sensorValue1,0,1024,0,253)));
  //Serial.write((char)(map(sensorValue2,0,1024,0,253)));
  Serial.write(0xfe);
  i++; 
*/
