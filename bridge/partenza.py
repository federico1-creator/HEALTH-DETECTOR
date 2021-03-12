import datetime
import os
import json
# import serial
# import serial.tools.list_ports
import time
import requests
from threading import Thread, Lock
# from threading
import webbrowser
from selenium import webdriver

from ponteprova import Bridge
import grafica_0
import grafica2prova


lucchetto= Lock()
class primo (Thread): # da rendere bloccante
    def __init__(self, nome, durata):
        Thread.__init__(self)
        self.nome= nome
        self.durata= durata

    def run(self):
        lucchetto.acquire()

        print(self.nome + ' avviato')

        grafica_0.root()
        print('proviamo:', grafica_0.DATI[:])
        time.sleep(self.durata)
        print('fine di ' + self.nome)

        lucchetto.release()

class conn (Thread): #2 thread con diverse funzioni di run
    def __init__(self, nome, lista): # valore che passo quando chiamo la classe
        Thread.__init__(self)
        self.nome=nome
        self.user= lista[0]
        self.pswd= lista[1]


    def run(self):
        print(self.nome + ' avviato')

        # eseguo il bridge
        br=Bridge()  
        br.setup()
        br.loop(self.user, self.pswd)
        
        print('fine di ' + self.nome)

class visual (Thread):
    def __init__(self, nome, durata, lista):
        Thread.__init__(self)
        self.nome= nome
        self.durata= durata
        self.user= lista[0]
        self.pswd= lista[1]

    def run(self):
        print(self.nome + ' avviato')
        #url= 'https://www.google.it/'
        #webbrowser.open_new(url)

        #time.sleep(self.durata)
        grafica2prova.root()
        # selenium part

        basedir = os.path.abspath(os.path.dirname(__file__))
        CHROME_DIR = os.path.join(basedir, 'chromedriver_win32\chromedriver.exe')
        
        url='http://127.0.0.1:5000/login' # login_bridge
        #url='https://www.google.com/'

        #time.sleep(2) # da valutare se toglierlo
        # percorso dove è salvato il driver
        chrome_driver= webdriver.Chrome(CHROME_DIR) 

        chrome_driver.get(url)
        chrome_driver.maximize_window()

        #chrome_driver.find_element_by_name()
        email_field= chrome_driver.find_element_by_id('email')
        email_field.send_keys(self.user)
        password_field= chrome_driver.find_element_by_id('password')
        password_field.send_keys(self.pswd)
        sub_field= chrome_driver.find_element_by_id('submit')
        sub_field.click()      

        print('fine di ' + self.nome )
        # c= 'ciao'
        # return c


if __name__ == '__main__': # se uno dei 2 si rompe, l'altro continua
    th0= primo('primo',3)
    
    th0.start()
    th0.join()
    
    th1=conn('1', grafica_0.DATI[:]) # da passare parametri per init
    th2=visual('2', 5, grafica_0.DATI[:])

    th1.start()
    th2.start()

    # non indispensabile
    th1.join()
    th2.join()
    print('FINE')
    