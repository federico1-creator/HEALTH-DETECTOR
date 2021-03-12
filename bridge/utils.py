import time  
import requests
   
def health_state(starttime):
    # starttime= int(time.time())
    v= None
    if ( int(time.time()) - int(starttime) ) > 10 :
        print('time', int(time.time())  )
        print('star1', int(starttime))
        starttime= time.time() # now
        print('star2', int(starttime))
        r= requests.get('http://127.0.0.1:5000/health_state') # stato di salute
        v= r.text
    #if v== 'ok:':
         #v=1
    return v