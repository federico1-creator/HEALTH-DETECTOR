import time
import datetime

c= datetime.date.today()
#print(c)
di= {'data': str(c)}
print(di)
data= datetime.datetime.strptime(str(c),'%Y-%m-%d')
#print(data)

#   print(send['posizione'][0])

c= 'str'
print(type(c))