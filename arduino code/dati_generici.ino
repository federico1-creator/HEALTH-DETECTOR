void dati_generici(){
  if (millis() - lt1 > 2000)
  {
  lt1= millis();

  // dati battito, temp, ossigeno 
  // read, attenzione al tempo per la conversione se il dato è analogico

  //t= t + 0.5;
  t= acquisisco_temp();
  //battito = battito + 1;
  //ossigeno = ossigeno + 1;
  acquisisco_puls(battito, ossigeno);
  

  resto= modf(t, &temp);
  resto= int(resto*10);
   


  // CONTROLLI sui dati prima di inviarli
  if ((battito>= 50 && battito<180) && (ossigeno<100) && (t>20 && t<43))  // guardare che temp ottengo dal sensore
  {
    // print the results to the Serial Monitor:
    Serial.write(0xff);
    Serial.write(0x04);
    Serial.write((char)battito);
    Serial.write((char)ossigeno);
    Serial.write((char)resto);
    Serial.write((int)temp);

    
    //Serial.write((char)(map(sensorValue1,0,1024,0,253)));
    //Serial.write((char)(map(sensorValue2,0,1024,0,253)));
    Serial.write(0xfe);
   }
  }
 }
