import tkinter as tk
import time
import requests
import webbrowser
import json
import schedule
# quando poi vado ad importare il file, le variabili globali disponibili come: grafica_0.bella

# conf / globali
USER= '' 
PSWD= ''
DATI= [1,2]
RICHIESTA= [0]

def root():
    #azione=0

    window= tk.Tk()
    window.geometry('600x400')
    window.configure(background='light blue')
    window.title('Inserisci i dati')
    #window.grid_columnconfigure(0, weight=1)
    ritorno= {}


    def iscrizione(): # se ho dimenticato codici o mi devo iscrivere
        url= 'http://127.0.0.1:5000/register' # link alla pagina di login
        webbrowser.open_new(url)
        # r = requests.get('http://127.0.0.1:5000/register')
        # print(r.status_code)
        # print(r.text)                        


    def azione_1():
        payload= {
            'nome utente' :  nome_utente.get(),
            'password' : password.get()
        }
        print(payload)

        headers= {'content-type': 'application/json'}
        # session per continuare a rimanere collegato
        s= requests.Session()
        # get ('https://www.google.it/')
        r= s.post('http://127.0.0.1:5000/log_control', data=json.dumps(payload), headers=headers) # aperta nuova route
        ritorno= r.text # è un dictionary ['Result']
        ritorno= ritorno.find("Success")

        print('testo della get:', ritorno)
        print( type(ritorno))
        if ritorno != -1 :
            RICHIESTA[0]= r.status_code
            passo= 'richiesta andata a buon fine'

            text= tk.Text(width= 30, height= 1)
            text.insert(tk.END, passo)
            text.grid(row=5, column= 1)
            
            p= list (payload.values())
            DATI[0]= p[0]
            DATI[1]= p[1]
            # DATI.append(p[0])
            # DATI.append(p[1])
            print(DATI[:])

            time.sleep(2)
            window.destroy()

        else:
            passo= 'richiesta rifiutata'
            #azione=1
            text= tk.Text(width= 30, height= 2)
            passo2= 'Inserire un nome utente ed una password validi'
            text.insert(tk.END, passo2)
            text.grid(row=7, column= 1)

            text= tk.Text(width= 30, height= 1)
            text.insert(tk.END, passo)
            text.grid(row=5, column= 1)

    


    label_1 = tk.Label(window, text= 'Se vuoi utilizzare il sistema con arduino, collegalo!!!')
    label_1.grid(row=0, column= 0, padx= 10, pady=20, sticky='WE')

    label_2 = tk.Label(window, text= 'Interfaccia per connessione con il server')
    label_2.grid(row=1, column= 0, padx= 10, pady=20, sticky='WE')

    label_3 = tk.Label(window, text='Inserire la e-mail')
    label_3.grid(row=3, column= 0, padx= 10, pady=10)

    nome_utente= tk.Entry()
    nome_utente.grid(row=3, column= 1, padx= 80)

    label_4 = tk.Label(window, text='Inserire la password')
    label_4.grid(row=4, column= 0, padx= 80, pady=10)

    password= tk.Entry()
    password.grid(row=4, column= 1, padx= 10)
    
    button_1 = tk.Button(text='RICHIESTA', command=azione_1)
    button_1.grid(row=5, column= 0, pady=10)

    
    # devo controllare anche la richiesta, 

    button_4 = tk.Button(text='Iscriversi 1° volta', command=iscrizione)
    button_4.grid(row=7, column= 0, pady=10) # 6

    print(DATI[:])

    window.mainloop()

# if __name__ == '__main__':

#     root()
#     print(bella)

""" 
s = requests.Session()
s.auth = ('user', 'pass')
s.post()

payload = {
    'inUserName': 'username',
    'inUserPass': 'password'
}

s= requests.Session()
p = s.post('LOGIN_URL', data=payload) # contiene dati dell'utente 


class requests.Request(method=None, url=None, headers=None, files=None, data=None, params=None, auth=None, cookies=None, hooks=None, json=None)
A user-created Request object.

Used to prepare a PreparedRequest, which is sent to the server.

Parametri:	
method – HTTP method to use.
url – URL to send.
headers – dictionary of headers to send.
files – dictionary of {filename: fileobject} files to multipart upload.
data – the body to attach to the request. If a dictionary is provided, form-encoding will take place.
json – json for the body to attach to the request (if data is not specified).
params – dictionary of URL parameters to append to the URL.
auth – Auth handler or (user, pass) tuple.
cookies – dictionary or CookieJar of cookies to attach to this request.
hooks – dictionary of callback hooks, for internal usage.
"""