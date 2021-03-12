void stato_salute()
{
int iFutureState;
int iReceived;

 

if(Serial.available() >0)
{
  iReceived= Serial.read();
  iFutureState=0; //primo stato
  // quando ho fatto la POST trasmetto un 'P'
  // devo spegnere il LED se sto bene

 

  if (iState==0 && iReceived=='O') iFutureState=1;
  if (iState==1 && iReceived=='N') iFutureState=2;
  if (iState==1 && iReceived=='F') iFutureState=3;
  if (iState==3 && iReceived=='F') iFutureState=4;
  if (iState==4 && iReceived=='O') iFutureState=1;
  if (iState==2 && iReceived=='O') iFutureState=1;

 

   // CR and LF always skipped (no transition)
   if (iReceived==10 || iReceived==13) iFutureState=iState;

 

   if(iFutureState==2 && iState==1) digitalWrite(12, HIGH);
   if(iFutureState==4  && iState==3) digitalWrite(12, LOW);
   // qui se voglio spegnere il 12, è già definito
   if(iFutureState==2 || iFutureState==4) digitalWrite(13, HIGH);
   
   iState = iFutureState;
}
}
