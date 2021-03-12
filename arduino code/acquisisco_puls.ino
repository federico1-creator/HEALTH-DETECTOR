
void acquisisco_puls(int &a, int &b){ // battito e ossigeno
  
  


// PulseOximeter is the higher level interface to the sensor
// it offers:
//  * beat detection reporting
//  * heart rate calculation
//  * SpO2 (oxidation level) calculation


// Callback (registered below) fired when a pulse is detected



    // Make sure to call update as fast as possible
    pox.update();

    // Asynchronously dump heart rate and oxidation levels to the serial
    // For both, a value of 0 means "invalid"
    if (millis() - tsLastReport > REPORTING_PERIOD_MS) {
        a = pox.getHeartRate();
        b = pox.getSpO2();
     
        
        tsLastReport = millis();
    }

  }
