# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 04:03:18 2018

@author: Ng Jen Yang
"""

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#Fetch the service account key JSON file contents
#cred = credentials.Certificate('''enter your key here''')

#Initialize the app with a service account, granting admin privileges
#firebase_admin.initialize_app(cred, {    'databaseURL': 'https://term-3-1d-b9d6b.firebaseio.com/'})



# =============================================================================
# bot2901 = db.reference('bot2901')
# bot2902 = db.reference('bot2902')
# bot2501 = db.reference('bot2501')
# bot2502 = db.reference('bot2502')
# bot2301 = db.reference('bot2301')
# bot2302 = db.reference('bot2302')
# =============================================================================



class MyBot():
    def __init__(self, name = "defaultname", block="unassigned",status = "available"):
        self._name = name
        self._block = block
        self._status = status    
        self._counter = 0
        self._total = 0
        self._address = db.reference("{}".format(self._name)).set({"status":status,"orders":{"null":"no orders yet!"}})
        
# =============================================================================
    #identity
    def name(self,new_name = None):
        if new_name == None:
            return ("The bot's name is registered as {}".format(self._name))
        else:
            if len(str(new_name)) == 4:
                if new_name >= 2000:
                    self._name = new_name
                    return ("Bot ID successfully assigned as {}".format(self._name))
                else:
                    return("invalid name!")
    def block(self, new_block = None):
        if new_block == None: 
            print ("The bot is currently assigned to: {}".format(self._block))
            return (self._block)
        else:
            if len(str(new_block)) == 2:
                if new_block >= 20:
                    self._block = new_block
                    return ("Bot successfully assigned to block {}".format(self._block))
    def status(self, new_status = None):
        if new_status == None:
            online_status = db.reference("{}/{}".format(self._name,"status")).get()
            print ("The bot is {}; online status registered as {}".format(self._status,online_status))
            return (online_status)
        else:
            allowed_statuses = ["going", "returning","unavailable", "available"]
            if new_status in allowed_statuses:
                self._status = new_status
                db.reference("{}".format(self._name)).update({"status" : self._status})
                return ("Status successfully changed to {}".format(self.status()))
            else:
                return ("Error setting status: current status is {}".format(self.status()))
    def counter (self, check = None):
        if check == "check":
            return self._counter
        elif check == "reset":
            self._counter = 0
            return("Counter reset")
        else:
            self._counter += 1
            print (">>>>>>>>>THIS : {}<<<<<<<<<<".format(self._counter))
            return self._counter
    def total (self, reset = None):
        if reset == "reset":
            self._total = 0
            return ("Total number of orders the bot processed thus far has been reset")
        else:
            return ("Total number of orders this bot has processed since last reset : {}".format(self._total))
#==============================================================================
    #execution
    def orders(self, new_order = None):
        if new_order == None:
            current_json = db.reference("{}/{}".format(self._name,"orders")).get()
            print ("\nOrders are currently: {}".format(current_json))
            return (current_json)
        else:
            self._total += 1
            current_json = db.reference("{}/{}".format(self._name,"orders")).get()
            print("THIS >>>>>>>>>>>>>>>{}<<<<<<<<<<<<<<<<<".format(current_json))
            current_orders = list(current_json.values())
            current_orders.append(new_order)
            print(current_orders)
            if "no orders yet!" in current_orders:
                print("yeah it's here")
                print ("             1              ",current_orders)
                current_orders.remove("no orders yet!")
                print ("             2              ",current_orders)
            self.counter("reset")
            new_json = {}
            for i in current_orders:
                new_json["order {}".format(self.counter())] = i
            db.reference("{}/{}".format(self._name,"orders")).set(new_json)
            return ("Success; orders are currently {}".format(self.orders()))
    def clear(self,neworder = None):
        db.reference("{}".format(self._name)).set({"null":"no orders yet!"})
        if self._status == "going":
            self.status("returning")
            print("yanny")
        elif self._status =="returning":
            self.status()
            print("laurel")
        return ("Orders cleared; bot {} currently has no orders in queue(bot queue: {}). Bot status is now {}.".format(self._name,self.orders(),self._status))
    def done(self, completed_order):
        if completed_order == None:
            return ("nani")
        else:
            things = db.reference("{}".format(self._name)).get()
            current_orders = list(things.values())
            print(current_orders)
            if completed_order in current_orders:
                print("yeah it's here: {} in {}".format(completed_order,current_orders))
                #current_orders.remove(completed_order)
                current_orders[:] = [x for x in current_orders if x != completed_order]
                self.counter("reset")
                new_json = {}
                if current_orders != []:
                    for i in current_orders:
                        new_json["order {}".format(self.counter())] = i
                else:
                    new_json = {"null":"no orders yet!"}
                db.reference("{}".format(self._name)).set(new_json)
                if self._status == "going":
                    self.status("returning")
                    print("yanny")
                elif self._status =="returning":
                    self.status()
                    print("laurel")
            else:
                return("No such order issued to bot {}".format(self._name))
            #for i in current_orders:
                #self.orders(i)
            #return("Order completed; orders for bot {} are now: {}".format(self._name,self.orders()))
            

#==============================================================================
#test code; testing for identity
#bot2901 = MyBot(2901,29)
#print("hello")
#print (bot2901.name())
#print(bot2901.block())
#print(bot2901.status())
#print(bot2901.counter("check"))
#print(bot2901.total())
#print(bot2901.total("reset"))
#bot2901.counter()
#test code; testing for execution
#print(bot2901.orders())
#print(bot2901.clear())
#print(bot2901.orders((3,"left")))
#print(bot2901.orders((3,"RIGHT")))
#print(bot2901.orders((3,"RIGHT")))
#print(bot2901.orders((3,"RIGHT")))
#print(bot2901.orders((3,"wat")))
#print(bot2901.done([3,"left"]))
#print(bot2901.done([3,"RIGHT"]))
#
#print(bot2901.counter("check"))
#print(bot2901.total())
#print(bot2901.total("reset"))


#==============================================================================
bot2901 = MyBot(2901,29)
bot2902 = MyBot(2902,29)
bot2301 = MyBot(2301,23)
bot2302 = MyBot(2302,23)
botlist =[bot2901, bot2902, bot2301, bot2302]
