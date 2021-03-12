import datetime
import json
import numpy as np
import serial
import serial.tools.list_ports
import time
import requests
import schedule 
from numpy import mean
from utils import health_state

class Bridge ():

    def setup(self):
        self.dato1=[]
        self.dato2=[]
        self.dato3=[]
        
        self.v= None
        self.ser = None
        self.c=0

        print("list of available ports: ")
        ports = serial.tools.list_ports.comports()

        self.portname=None
        for port in ports:
            print (port.device)
            print (port.description)
            if 'arduino' in port.description.lower():
                self.portname = port.device
        
        self.portname = 'COM6'
        try:
            if self.portname != None:
                print ("connecting to " + self.portname) 
                self.ser = serial.Serial(self.portname, 9600, timeout=0)
        except:
            self.ser = None
            print('Dispositivo non connesso')

        finally:
            print('check della connessione')

        self.inbuffer=[]

    
    def loop(self, user, pswd):
        c=0
        starttime= time.time()
        print('partenza',int(starttime))

        def job():
            # v= None
            headers = {'content-type':'application/json'}
            r= requests.post('http://127.0.0.1:5000/health_state', data=json.dumps({'user':user, 'password':pswd}),headers=headers) # stato di salute
            v= r.text
            print('salute: ', v)

            stringa = str.encode('ON')
            if v=='malato':
                print('stampo su arduino')
                self.ser.write(stringa) #pezzo per spegnere il LED, se disconnetto rompo
            
            else:
                # da implementare {1}
                spengo = str.encode('OFF')
                print('spengo arduino')
                self.ser.write(spengo)
            
        schedule.every(10).seconds.do(job)
        
        while (True):

            if self.ser != None:
                
                #look for a byte from serial
                if self.ser.in_waiting>0:
                    # data available from the serial port
                    lastchar=self.ser.read(1)


                    if lastchar==b'\xfe': #EOL
                        print("\nValue received")
                        self.useData() # agisco sul buffer
                        self.sendData(user, pswd) 
                        self.inbuffer =[]
                    else:
                        self.inbuffer.append (lastchar)
            
                schedule.run_pending() # NO valori di ritorno
                

            else:

                # aspetto e rifaccio il setup
                print('non connesso con arduino')
                time.sleep(10)
                self.setup()


            #schedule.run_pending() # NO valori di ritorno, posizione iniziale

            # v= health_state(starttime) # ritorna 'ok'
            """ stringa = str.encode('AM')
            if self.v=='ok':
                print('stampo su arduino')
                self.ser.write(stringa) # se disconnetto rompo
            # pezzo per spegnere il LED
            else:
                spengo = str.encode('HE')
                self.ser.write(spengo) """



    def useData(self):
        if self.inbuffer[0] != b'\xff': # split parts, inizio corretto
            return False

        # condizione per i diversi pacchetti
        if len(self.inbuffer) == 6:
            self.Pac1()
        if len(self.inbuffer) == 8: # dimensione da impostare
            self.Pac2()
        

    def Pac1(self):
        print(self.inbuffer)
        if len(self.inbuffer)<3:   # at least header, size, footer
            return False           # può essere anche tolto, controllo già fatto
        
        numval = int.from_bytes(self.inbuffer[1], byteorder='little')
        if len(self.inbuffer) == (numval+2):
            print('Buffer di dimensione corretta')

        j=['Battito', 'Ossigeno', 'Temp1', 'Temp2']
        for i in range (numval):
            val = int.from_bytes(self.inbuffer[i+2], byteorder='little') # primi 2 posti contengono sporco
            print("Sensor %s: %d " % (j[i], val))
            if i==0:
                self.dato1.append(val)
            if i==1:
                self.dato2.append(val)
            if i==2:
                dato4 = val/10
            if i==3:
                if dato4 != 0:
                    self.dato3.append(val + dato4)
                else:
                    self.dato3.append(val)


    def Pac2(self): 
        print('Arrivato pacchetto 2')
        lat= []
        lon= []
        numval = int.from_bytes(self.inbuffer[1], byteorder='little')
        if len(self.inbuffer) == (numval+2):
            print('Buffer di dimensione corretta')  
        
        for i in range(3):
            val = int.from_bytes(self.inbuffer[i+2], byteorder='little')
            lat.append(val)

        for i in range(3): # lon
            val = int.from_bytes(self.inbuffer[3+i+2], byteorder='little')
            lon.append(val)

        # creo il valore corretto, da prendere fuori il valore
        s= str(lat[1]) + str(lat[2])
        v= str(lon[1]) + str(lon[2])

        self.latitudine= float(str(lat[0]) + '.' + s)
        self.longitudine= float(str(lon[0]) + '.' + v)
        self.lis= [self.latitudine, self.longitudine]
        print(self.latitudine) #
        print(self.longitudine)


    # quando finisce Pac2 passso sendData con i dati di tutti e 2 i pacchetti
    def sendData(self, user, pswd): 
        # sincronizzazione dei 2 pacchetti
        self.media1 = None
        send1 = {} # inizializzazione

        if len(self.dato1) >= 3 and len(self.dato2) >= 3 and len(self.dato3) >= 3 and len(self.lis) == 2: # condizioni per tutto
            self.media1 = np.round(mean(self.dato1), decimals=2)
            self.media2 = np.round(mean(self.dato2), decimals=2)
            self.media3 = np.round(mean(self.dato3),decimals=2)

            send1 = {
                'battito' : self.media1,
                'ossigeno' : self.media2,
                'temp' : self.media3,
                'posizione' : [self.lis[0], self.lis[1]]
            }
       
            if self.c==0: #POST solo 1 volta
                oggi= datetime.date.today()
                dati= {
                    'user' : user,
                    'password' : pswd,
                    'data' : str(oggi)
                    }
                # l'unione dei dizionari dipende da come funziona la sessione
                send= dict(send1, **dati) # combino i 2 dizionari
                headers= {'content-type': 'application/json'}
                url= 'http://127.0.0.1:5000/load_data'
                s= requests.Session()
                r1= s.post(url, data=json.dumps(send), headers=headers) # o data=send1
                
                # successo?
                ritotno= r1.text
                ritotno= ritotno.find("Sucess")
                if ritotno != -1:
                    # andata a buon fine, ACCENDO
                    trasmesso= str.encode("P") #P
                    print('POST avvenuta, accendo arduino')
                    self.ser.write(trasmesso)

                # da togliere
                print(s.cookies)
                print(send)

                self.c= self.c+1
            else:
                print('POST giè eseguita !!!')
        
        #print('invio',send)
        print(self.media1)
        print(self.dato1)
        self.dato2 # se voglio stamparli
        self.dato3