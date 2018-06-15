# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 19:04:02 2018

@author: Ng Jen Yang
"""

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#Fetch the service account key JSON file contents
cred = credentials.Certificate('''enter your key here''')

#Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {    'databaseURL': 'https://term-3-1d-b9d6b.firebaseio.com/'})

from virtual_bot import MyBot

import time
import threading
from queue import Queue

Q = Queue()
q = Queue()
num_worker_threads = 2
num_sender_threads = 1

def worker():
    while True:
        print("worker idle on thread {} : 1".format(threading.get_ident()))
        order = Q.get()
        if order is None:
            print("worker idle on thread {} : 2".format(threading.get_ident()))
            Q.task_done()
            print("worker kill on thread {}".format(threading.get_ident()))
            break
        else:
#            print("order received on thread {} : order is {}".format(threading.get_ident(), order))
            assign_order(order,botlist)
            Q.task_done()
            
def sender():
    while True:
        print("sender idle on thread {} : 1".format(threading.get_ident()))
        order_pair = q.get()
        if order_pair is None:
            print("sender idle on thread {} : 2".format(threading.get_ident()))
            q.task_done()
            print("sender kill on thread {}".format(threading.get_ident()))
            break
        else:
#            print("order received on thread {} : order is {}".format(threading.get_ident(), order))
            send_order(order_pair)
            q.task_done()
    
#==============================================================================
    
dborders = db.reference('orders')

def select_bots(block, botlist):
    blocklist=[]
    humanreadable = []
    for bot in botlist:
        print ("check 1")
        if bot.block() == block:
            print("check 2.1; block match")
            if bot.status() != "unavailable":
                blocklist.append(bot)
                humanreadable.append(bot.name())
                print("check 2.2 ; accepted")
            else:
                print("check 3.1; bot is unavailable")
                pass
        else:
            print ("No, {} != {}".format(bot.block() , block))
        print ("check 3.2; mismatch")
    print("what",humanreadable)
    return blocklist

def best_bot(blocklist):
    busybot = []
    for bot in blocklist:
        current_json = bot.orders()
        current_orders = list(current_json.values())
        number_of_orders = len(current_orders)
        if len(current_orders) == 1:
            if "no orders yet!" in current_orders:
                number_of_orders = 0
        print("hello>>>>>>>>>>>",bot,number_of_orders)
        busybot.append((bot,number_of_orders))
        print(busybot)
        least_orders = busybot[0][1]
        best_bot = busybot[0][0]
    for i in range(0,len(busybot)-1,1):
        if busybot[i][1] <= busybot[i+1][1]:
            print ("yes; {} =< {}".format(busybot[i][1],busybot[i+1][1]))
            least_orders = busybot[i][1]
            best_bot = busybot[i][0]
        else:
            least_orders = busybot[i+1][1]
            best_bot = busybot[i+1][0]
            print ("no; {} > {}".format(busybot[i][1],busybot[i+1][1]))
            pass
    repeats = 0
    for i,j in busybot:
        if j == least_orders:
            repeats += 1            
    if repeats>1:
            print("Multiple bots with least orders of {}; running priority check.".format(least_orders))
            best_bot = priority_check(busybot,least_orders)
    else:
        print("absolute best found")
        pass
    print("The most available bot is {}, with {} pending orders. It is currently {}.".format(best_bot.name(),least_orders,best_bot.status()))
    return best_bot

def priority_check(busybot,least_orders):
    collection = [bot for (bot,no_of_orders) in busybot if no_of_orders == least_orders]
    print(collection)
    best_bot = collection[0]
    best_bot_status = associated_priorities[collection[0].status()]
    for i in range (0, len(collection)-1, 1):
        if associated_priorities[collection[i].status()] > associated_priorities[collection[i+1].status()]:
            best_bot_status = collection[i].status()
            best_bot = collection[i]
        else:
            best_bot_status = collection[i+1].status()
            best_bot = collection[i+1]
    print("The best bot that is has the least orders and is most available is bot {}, with {} pending orders and a status of {}".format(best_bot.name(), least_orders, best_bot_status))
    return best_bot

def assign_order(order,botlist):
    blocklist = select_bots(order[0],botlist)
    selected_bot = best_bot(blocklist)
    print(order)
    print(associations)
    translated_order = associations[tuple(order)]
    print("the translated order is : {}".format(translated_order))
    #print("order pushed to {}, {}".format(selected_bot.name(), selected_bot.orders()))
    q.put((selected_bot,translated_order))

def send_order(order_pair):
    order_pair[0].orders(order_pair[1])
    print("order pushed to {}, {}".format(order_pair[0].name(), order_pair[1]))
        
def dict_compare(d1, d2):
    print("init comparison")
    if type(d2) == str:
        d2_keys = {'0'}
    else:
        d1_keys = set(d1.keys())
        d2_keys = set(d2.keys())
        temp_1 = []
        for i in d1.values():
            temp_1.append(tuple(i))
        d1_values = set(temp_1)
        temp_2 = []
        for i in d2.values():
            temp_2.append(tuple(i))
        d2_values = set(temp_2)
        print (d1_values,d2_values)
        intersect_keys = d1_keys.intersection(d2_keys)
#        intersect_values = d1_values.intersection(d2_values)
        added = d1_keys - d2_keys
        new_orders = {o: d1[o] for o in added}
        removed = d2_keys - d1_keys
        new = {o : d1[o] for o in intersect_keys if d1[o] != d2[o]}
        same = set(o for o in intersect_keys if d1[o] == d2[o])
        return added, removed, new, same , new_orders

#==============================================================================

actual_address = [(23,1,4),(23,6,5),(29,7,8),(29,5,3)]
robot_orders = [(1,"left",1),(6,"left",2),(7,"right",4),(5,"left",2)]
associations = dict(zip(actual_address,robot_orders))
print(associations)
print(associations[(23,1,4)])

allowed_statuses = ["going", "returning","unavailable", "available"]
priority_values = [1,2,0,3]
associated_priorities = dict(zip(allowed_statuses, priority_values))
print(associated_priorities)


bot2901 = MyBot(2901,29)
bot2902 = MyBot(2902,29)
bot2301 = MyBot(2301,23)
bot2302 = MyBot(2302,23)
botlist =[bot2901, bot2902, bot2301, bot2302]

#bot2902.orders((3,"up",4))
#bot2901.status("unavailable")
#bot2901.status("available")

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

#==============================================================================

''' initialising workers '''
threads = []
for i in range(num_worker_threads):
    t = threading.Thread (target = worker)
    t.start()
    threads.append(t)
    
threadss = []
th = threading.Thread (target = sender)
th.start()
threadss.append(th)
    
#==============================================================================

''' initialising server '''
try:
    counter = 0
    ordersold = dborders.get()
    print(ordersold)
    print("start")
    while True:
        print(counter)
        counter += 1
        print(counter)
        orders = dborders.get()
        print("orders: this >>>> {}".format(orders))
        print("previous orders: this >>>> {}".format(ordersold))
        if orders == ordersold:
            print("idleidle")
            pass    
        else:
            print("new!")
            if ordersold == [{"null":"nope"}]:
                new_orders = orders
                print("no updates")
            else:
                added, removed, new, same , new_orders = dict_compare(orders,ordersold)
            ordersold = orders  #updates old list
            print(new_orders)
            addresses = list(new_orders.values())
            print("addresses: this >>> {}".format(addresses))
            for i in addresses:
                Q.put(i)
    #            sb_name, sb_orders = assign_order(i,botlist)
        if counter == 100:
            dborders.set({"null":"nope"})
            print("firebase orders cleared")
            ordersold = {"null":"nope"}
            orders = {"null":"nope"}
            print("server orders cleared")
            print("!!!!!!!!!!!!!!!!!!!!!!!100th iteration; clearing order lists!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            counter = 0
            print("counter reset: current counter {}".format(counter))
        print("####################looping####################")
            
#==============================================================================
except (KeyboardInterrupt,SystemExit):
    print ("killing workers")
    for i in range (num_worker_threads):
        Q.put(None)
    print ("workers killed; killing server")
    raise
    
print(associated_priorities["returning"])
