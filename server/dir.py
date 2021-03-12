""" import os

def list_file(start):
    for root, dirs, files in os.walk(start):
        if dir!= '.git':
            level= root.replace(start, '').count(os.sep)
            indent= ''*4*(level)
            print('{}{}/'.format(indent, os.path.basename(root)))
            subindent= ''*4*(level+1)
            for f in files:
                print('{}{}/'.format(subindent, f))

start= os.getcwd()
list_file(start) """

import folderstats
import os

percorso= os.getcwd()
df = folderstats.folderstats('.', ignore_hidden=True)
print(percorso)
print(df)