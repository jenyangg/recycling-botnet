# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 05:55:38 2018

@author: Ng Jen Yang
"""
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 07:27:47 2018

@author: Ng Jen Yang
"""
import time
import threading
from queue import Queue

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db




#Fetch the service account key JSON file contents
#cred = credentials.Certificate("C:/Users/Ng Jen Yang/Downloads/term-3-1d-b9d6b-firebase-adminsdk-3ycpt-5e7cf7c1db.json")

#Initialize the app with a service account, granting admin privileges
#firebase_admin.initialize_app(cred, {    'databaseURL': 'https://term-3-1d-b9d6b.firebaseio.com/'})
#==============================================================================

db.reference("{}".format(2901)).update({"status" : "unavailable"})

#import virtual_bot
#
##==============================================================================
#
#dborders = db.reference('orders')
##dborders.push((3,"right"))
#
#Q = Queue()
#
#num_worker_threads = 2
#def worker():
#    while True:
#        print("worker idle on thread {} : 1".format(thread = threading.get_ident()))
#        order = Q.get()
#        if item is None:
#            print("worker idle on thread {} : 2")
#            Q.task_done()
#            break
#        else:
#            print("order received on thread {} : order is {}".format(threading.get_ident(), order))
#            assign_order(order)
#            Q.task_done()
#
#def select_bots(block, botlist):
#    blocklist=[]
#    humanreadable = []
#    for bot in botlist:
#        print ("check 1")
#        if bot.block() == block:
#            print("check 2.1")
#            blocklist.append(bot)
#            humanreadable.append(bot.name())
#            print("check 2.2")
#        else:
#            print ("No, {} != {}".format(bot.block() , block))
#        print ("check 3")
#    print("what",humanreadable)
#    return blocklist
#
#def best_bot(blocklist):
#    busybot = []
#    for bot in blocklist:
#        current_json = bot.orders()
#        current_orders = list(current_json.values())
#        number_of_orders = len(current_orders)
#        if len(current_orders) == 1:
#            if "no orders yet!" in current_orders:
#                number_of_orders = 0
#        print("hello>>>>>>>>>>>",bot,number_of_orders)
#        busybot.append((bot,number_of_orders))
#        print(busybot)
#    for i in range(0,len(busybot)-1,1):
#        least_orders = busybot[0][1]
#        best_bot = busybot[0][0]
#        if busybot[i][1] <= busybot[i+1][1]:
#            print ("yes; {} =< {}".format(busybot[i][1],busybot[i+1][1]))
#            least_orders = busybot[i][1]
#            best_bot = busybot[i][0]
#        else:
#            least_orders = busybot[i+1][1]
#            best_bot = busybot[i+1][0]
#            print ("no; {} > {}".format(busybot[i][1],busybot[i+1][1]))
#            pass
#    print("The most available bot is {}, with {} pending orders.".format(best_bot.name(),least_orders))
#    return best_bot
#
#def assign_order(order,botlist):
#    blocklist = select_bots(order[0],botlist)
#    selected_bot = best_bot(blocklist)
#    print(order)
#    print(associations)
#    translated_order = associations[tuple(order)]
#    print("the translated order is : {}".format(translated_order))
#    selected_bot.orders(translated_order)
#    print("order pushed to {}, {}".format(selected_bot.name(), selected_bot.orders()))
#    return (selected_bot._name,selected_bot.orders())
#        
#def dict_compare(d1, d2):
#    if type(d2) == str:
#        d2_keys = {'0'}
#    else:
#        d1_keys = set(d1.keys())
#        d2_keys = set(d2.keys())
#        temp_1 = []
#        for i in d1.values():
#            temp_1.append(tuple(i))
#        d1_values = set(temp_1)
#        temp_2 = []
#        for i in d2.values():
#            temp_2.append(tuple(i))
#        d2_values = set(temp_2)
#        print (d1_values,d2_values)
#        intersect_keys = d1_keys.intersection(d2_keys)
#        intersect_values = d1_values.intersection(d2_values)
#        added = d1_keys - d2_keys
#        new_orders = {o: d1[o] for o in added}
#        removed = d2_keys - d1_keys
#        new = {o : d1[o] for o in intersect_keys if d1[o] != d2[o]}
#        same = set(o for o in intersect_keys if d1[o] == d2[o])
#        return added, removed, new, same , new_orders
#
#
#
#
#
#==============================================================================

#actual_address = [(23,1,4),(29,7,8),(29,5,3)]
#robot_orders = [(1, "left" , 1),(7, "right" , 4),(5,"left", 2)]
#associations = dict(zip(actual_address,robot_orders))
#print(associations)
#print(associations[(23,1,4)])
#
#bot2901 = MyBot(2901,29)
#bot2902 = MyBot(2902,29)
#bot2301 = MyBot(2301,23)
#bot2302 = MyBot(2302,23)
#botlist =[bot2901, bot2902, bot2301, bot2302]

#==============================================================================

#threads = []
#for i in range(num_worker_threads):
#    t = threading.Thread (target = worker)
#    t.start()
#    threads.append(t)
    
#==============================================================================

#counter = 0
#ordersold = dborders.get()
#print(ordersold)
#print("start")
#while True:
#    print(counter)
#    counter += 1
#    print(counter)
#    orders = dborders.get()
#    print("orders: this >>>> {}".format(orders))
#    print("previous orders: this >>>> {}".format(ordersold))
#    if orders == ordersold:
#        print("idleidle")
#        pass    
#    else:
#        print("new!")
#        if ordersold == ["nope"]:
#            new_orders = orders
#            print("no updates")
#        else:
#            added, removed, new, same , new_orders = dict_compare(orders,ordersold)
#        ordersold = orders  #updates old list
#        print(new_orders)
#        addresses = list(new_orders.values())
#        print("addresses: this >>> {}".format(addresses))
#        for i in addresses:
#            Q.put(i)
#            sb_name, sb_orders = assign_order(i,botlist)
#    if counter == 100:
#        dborders.set("nope")
#        print("firebase orders cleared")
#        ordersold = "nope"
#        orders = "nope"
#        print("server orders cleared")
#        print("!!!!!!!!!!!!!!!!!!!!!!!100th iteration; clearing order lists!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#        counter = 0
#        print("counter reset: current counter {}".format(counter))
#    print("####################looping####################")
        
#==============================================================================



    


    
#assign_order((23,1,4),botlist) 
    


#
#d1 = {"hello":"hi", "nani":"defuk"}
#d2 = {"hello":"hi", "nani":"defuk", "omaewamou":"shindeiru"}
#dict_compare(d2,d1)


#d3 = {'-LEJ3AV2cwd-PBE83yre': [3, 'left'], '-LEJ3KIWbO8yxhpZ4po7': [3, 'left'], '-LEfYop74DADMiQU3N8j': 'HELLO', '-LEfZBIV1SnK_SP7d5z9': 'HELLO', '-LEfZJxHXFeUSK6zlXqb': 'HELLO', '-LEfZhUhKpt7inkmuOs_': 'HELLO', '-LEfc_NmzWVVnYVGEvwC': 'HELLO'}
#d4 = {'-LEJ3AV2cwd-PBE83yre': [3, 'left'], '-LEJ3KIWbO8yxhpZ4po7': [3, 'left'], '-LEfYop74DADMiQU3N8j': 'HELLO', '-LEfZBIV1SnK_SP7d5z9': 'HELLO', '-LEfZJxHXFeUSK6zlXqb': 'HELLO', '-LEfZhUhKpt7inkmuOs_': 'HELLO', '-LEfc_NmzWVVnYVGEvwC': 'HELLO', '-LEfcsd2L3rlep1hOjxP': 'nani', "whatt":"pls"}
#dict_compare(d4,d3)


#import firebase_admin
#from firebase_admin import credentials
#from firebase_admin import db
#
##Fetch the service account key JSON file contents
#cred = credentials.Certificate("C:/Users/Ng Jen Yang/Downloads/term-3-1d-b9d6b-firebase-adminsdk-3ycpt-5e7cf7c1db.json")
#
##Initialize the app with a service account, granting admin privileges
#firebase_admin.initialize_app(cred, {    'databaseURL': 'https://term-3-1d-b9d6b.firebaseio.com/'})
#
#bot2901 = MyBot(2901,29)
#bot2902 = MyBot(2902,29)
#bot2301 = MyBot(2301,23)
#bot2302 = MyBot(2302,23)
#botlist =[bot2901, bot2902, bot2301, bot2302]
#
#botname
#db.reference("{}".format(self._name)).set({"status":status,"orders":{"null":"no orders yet!"}})