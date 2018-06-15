# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 01:43:53 2018

@author: Ng Jen Yang
"""

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#Fetch the service account key JSON file contents
cred = credentials.Certificate('''enter your key here''')

#Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {    'databaseURL': 'https://term-3-1d-b9d6b.firebaseio.com/'})

dborders = db.reference('orders')
dborders.push((29,7,8))
#dborders.push((23,1,4))
#dborders.push((23,6,5))
dborders.push((29,5,3))

#db.reference("{}".format(2901)).update({"status" : "unavailable"})
#bot2901.status()
#bot2901.status("unavailable")
#bot2901.status("available")
#db2901 = db.reference('2901')


#db.reference('2901').update()
