import requests
import time
import json
import os
import tkinter as tk
import webbrowser
from selenium import webdriver
#r'chromedriver_win32\chromedriver.exe'


def richiesta(user, pswd): # viene eseguito subito, per i parametri che ha
        # user, pswd
        basedir = os.path.abspath(os.path.dirname(__file__))
        CHROME_DIR = os.path.join(basedir, 'chromedriver_win32\chromedriver.exe')
        
        url='http://127.0.0.1:5000/login' # login_bridge
        #url='https://www.google.com/'

        time.sleep(2)
        # percorso dove è salvato il driver
        chrome_driver= webdriver.Chrome(CHROME_DIR) 

        chrome_driver.get(url)
        chrome_driver.maximize_window()

        #chrome_driver.find_element_by_name()
        email_field= chrome_driver.find_element_by_id('email')
        email_field.send_keys(user)
        password_field= chrome_driver.find_element_by_id('password')
        password_field.send_keys(pswd)
        sub_field= chrome_driver.find_element_by_id('submit')
        sub_field.click()

        
        # BUG qui non rimane in loop la funzione
        # NON HO window.mainloop()

def root():

    window = tk.Tk()
    window.geometry('570x400')
    window.configure(background='light blue')
    window.title('Interfaccia Bridge!')
    #window.grid_columnconfigure(0, weight=1)

    def azione_1():
        window.destroy()

    label_1 = tk.Label(window, text= 'COMPLIMENTI !!!')
    label_1.grid(row=0, column= 0, padx= 10, pady=20, sticky='WE')

    label_2 = tk.Label(window, text='Sei connesso al tuo account')
    label_2.grid(row=1, column= 0, padx= 10, pady=10)

    label_3 = tk.Label(window, text='Vuoi accedervi?')
    label_3.grid(row=2, column= 0, padx= 10, pady=10)

    button_1 = tk.Button(text='RICHIESTA DI ACCESSO', command=azione_1)
    button_1.grid(row=2, column= 1, pady=10) 

    """ button_3 = tk.Button(text='APERTURA BROWSER', command=apro_br)
    button_3.grid(row=10, column= 0, pady=10)
 """
    passo= 'INFO: se vuoi aggiornare la tua posizione GPS aspetta qualche minuto e spingi il pulsante su arduino. Nel mentre non posizionare le dita in prossimità dei sensori'

    text= tk.Text(width= 40, height= 8)
    text.insert(tk.END, passo) # dimensioni
    text.grid(row=3, column= 0, padx= 10)
    
    window.mainloop()

""" # per prove, POI MESSO NEL BRIDGE COMPLETO
if __name__ == '__main__':
    user= 'laura@gmail.com'
    pswd= '123'

    root()
    richiesta(user, pswd) """