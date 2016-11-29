'''
Created on 31.03.2016

@author: jannik
'''

from Werkzeug.KSoPSWerkzeug import Werkzeug

wz = Werkzeug()

ex = "n"
step = 0
while ex!="q":
    wz.run()
    ex = input("quit?")