# recycling-botnet

hullo!

summary of files: 

file 1: virtual_bot.py
Contains a single class (along with test code commented out) for a virtual bot. Class contains methods that establishes a bot's identity (name, assigned block, status, address in database,), and methods that constitute the actions that the bot can take (accept order, clear order, reset orders, change status). Test code commented out at the end.

Bot methods allow:
1. Reassociation of bots; private attribute self.total tracks usage statistics, according to how many orders are completed. If a certain block uses the service much more than another, bots can be reassigned to meet the usage of each block.
2. Enabling/disabling of bot; if bot is damaged, status can be changed to exclude the bot from receiving more orders until reactivated.
3. Prioritisation; orders will go to bots that are more ready to accept the order (by number of orders and bot status).
4. Self-clearing; the bot can manage its own orders. The bot is allowed to clear its own orders on completion. Also, due to the nature of the data, the bot _can_ be written to prioritise certain units before others regardless of order in the list, _if_ it increases the efficiency of the bot's pathing. (eg the if the bot has 3 orders on level 3 and 2 orders on level 14, it will serve by level instead of alternating if the path is significantly more efficient.)

Behavior:
1. Orders(): returns the current list of orders, issues order if (single) argument specified
2. done(): removes completed order from that bot's order list, and reorders the list such that orders all start from order 1 (i.e. previous order 2 is pushed up to be order 1)
3. clear(): resets orders 


file 2: compiled.py
Pulls class from virtual_bot.py, runs a while True loop to determine new orders, and uses workers (default qty: 2) that listens and processes orders. Keyboard interrupt terminates workers and server code. Workers issue orders to bots in order of which bot assigned to that block is most available (has least number of pending orders in its orders list + priority in available > returning > going, unavailable not considered)
Also contains dictionaries used to translate orders from a human-readable format (#xx-yy-zz) to a format that the bot can parse using line following + color detection, henceforth referred to as bot-readable.

Behaviour:
1.Accepts input from widget (not included) as (block,floor,unit), data is written to a node in Firebase that functions as a collective orders list.

2. Server compares current collective orders list with the previous collective orders list stored in the previous loop.
a. if same: idleidle
b. if different: 
  i. locate the differences, and individually put them into a local (serverside) queue.
  
3 Orders are now assigned by two different types of workers.
a. Workers pick orders from the queue, then determines and assigns which bot it should go to.If the bot's status == "unavailable", then the bot is excluded from the assignment process. 
b. Another worker picks up the orders and associated bot, then sends them in with the correct order number (prevents overwriting one order with another using the same order number)

4. Bot nodes in firebase (i.e. 2901 for bot 2901) have two direct child nodes; status and orders. On receiving an order:
  a. order is placed into the bot/orders node as { "order n" : bot-readable }
  b. if it initially had no order, bot removes {"null" : "no orders yet!"}
  
5. On completion of an order:
  a. Removes that order from the list
  b. Orders are pushed forward; previous order 2 , stored as {"order 2" : bot-readable} is now stored as {"order 1" : bot-readable}.
  c. If no orders left in list, orders are reset to {"null" : "no orders yet!"}

Keyboard interrupt kills workers, senders, and server script.
