// da inserire in leggo_GPS
// prima devo estrarre la stringa dei dati {dato}

#ifndef GPSPARSER_H
#define GPSPARSER_H

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

void gpsparser(char* dato,double &latitude,double &longitude)
{   
    // 1° parte
    
    // dal sensore GPS viene estratta la stringa, su cui faccio manipolazioni
    //char dato[]= "GPRMC,103726.00,A,4437.24013,N,01056.35045,E,0.941,,150221,,,A1719";
    char confronto[]= "GPRMC";
    // in alternativa con ciclo per scrivere uin carattere alla volta (%c)  ...[i]!='\0'
    printf("\n%s\n", dato);
    
    double risultato_lat;
    double risultato_lon;
    
    int c=0;
    int i;
    int val=0;
    char lat[15]= {0};
    char lon[11]= {0};
    
    for (i=0; i<5; i++ ){
        if (dato[i]==confronto[i])
            c++;
    }
    //printf("%d\n", c); //5
    if (c==5){
        printf("dato corretto, continuo\n");
        // ...
        i=0;
        int j=0;
        char *p;
        
        p= strtok(dato, ",");
        while(p!= NULL)
        {
        printf("%s\n",p);
        //printf("%d\n", strlen(p));
        
        if (i==3){
            for (j=0; j<10; j++)
            {
                lat[j]= p[j];
               
            }
        }
        
        if (i==5){
            for (j=0; j<11; j++)
            {
                lon[j]= p[j];
               
            }
        }
        
        p= strtok(NULL, ",");
        i+=1;
        }
        val=1;
    }
    else
        printf("dato incompleto, RIPROVO\n");
        
    if(val==1){
    printf("\nnel posto 3: %s\n", lat);
    printf("nel posto 5: %s\n", lon);
    printf("%d\n", i);  // splittato in 10 blocchi la stringa iniziale
    
    
    //char p_array[i]= {p};
    //printf(sizeof(p_array));

    double latitudine = strtod(lat,NULL);
    double longitudine = strtod(lon,NULL);
    //double ftemp = atof(lat); // double 
    printf("coordinate: %f, %f",latitudine, longitudine);   // valori da usare per le conversioni
    
    
    
    // 2° parte
    
    double fract1;
    double intero1;
    
    // inizio divisione lat
    fract1= modf(latitudine, &intero1);
    int numero1= (int)intero1;
    printf("parte intera: %f e parte decimale: %f\n", intero1, fract1);
    fract1= fract1*100;
    
    printf("%f\n",fract1);
    printf("%d\n",numero1);
    
    double minuti1, gradi1;
    double inizio1;
    inizio1= intero1/100;
    minuti1= modf(inizio1, &gradi1);
    printf("parte intera: %f e parte decimale: %f\n\n", gradi1, minuti1);
    minuti1= minuti1*100;
    
    risultato_lat= fract1/60;
    risultato_lat= risultato_lat+minuti1;
    risultato_lat= risultato_lat/60;
    risultato_lat= risultato_lat+gradi1;
    
    printf("risultato: %f\n", risultato_lat);
    
    
    // inizio divisione lon
    double fract2;
    double intero2;
    
    fract2= modf(longitudine, &intero2);
    int numero2= (int)intero2;
    printf("parte intera: %f e parte decimale: %f\n", intero2, fract2);
    fract2= fract2*100;
    
    printf("%f\n",fract2);
    printf("%d\n",numero2);
    
    double minuti2, gradi2;
    double inizio2;
    inizio2= intero2/100;
    minuti2= modf(inizio2, &gradi2);
    printf("parte intera: %f e parte decimale: %f\n\n", gradi2, minuti2);
    minuti2= minuti2*100;
    
    risultato_lon= fract2/60;
    risultato_lon= risultato_lon+minuti2;
    risultato_lon= risultato_lon/60;
    risultato_lon= risultato_lon+gradi2;

    printf("risultato: %f", risultato_lon);
    
    // risultato_lat e risultato_lon
    }
    
    // dati GPS da mandare
    printf("\noordinate latitudine: %f", risultato_lat);
    printf("\ncordinate longitudine: %f", risultato_lon);
    latitude=risultato_lat;
    longitude=risultato_lon;
}
#endif
