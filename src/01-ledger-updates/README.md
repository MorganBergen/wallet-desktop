# show ledger updates via network threading

**contents**

0.  [main readme](https://github.com/MorganBergen/wallet-desktop)
1.  [previous project](https://github.com/MorganBergen/wallet-desktop/tree/main/src/00-get-ledger)
2.  [view code](./main.py)
3.  [brief](#brief)
4.  [description](#description)
5.  [script](#script)
6.  [background](#background)

## brief

previous project simply revealed the latest validated ledger index at the time of interpretation. this project will reveal the latest validated ledger index as it changes in time, the ledger is constantly making forward progress, so in order to continually watch the ledger for updates then there needs to be changes to the architecture of the app.  the manipulation of such architecture will allow for a user for example to see when new transactions have been confirmed in real time, not simple after program execution.  

thus for reasons specific to python, it's best to use two _threads_, a gui thread in order to handle user input and display, and a worker thread for xrp ledger network connectivity.  the operating system can switch quickly between the two threads at any time, so the user interface can remain responsive while the background thread waits on information from the network that may take a while to arrive.  

the main challenge with threads is that you have to be careful not to access data from one thread that another thread may be in the middle of changing.  a straightfoward way to do this is to design your program so that each thread has variables it "owns" and doesn't write to the other thread's variables.  in this program each thread is to its own class, so each thread should only write to its own class attributes.  when the threads need to communicate, they use specific, "thread-safe" methods of communication these include but are not limited to

-  gui to worker thread `asyncio.run_coroutine_threadsafe()`

-  for worker to gui communications, use `wx.CallAfter()`

to make full use of the ledger's ability to push messages to the client use xrpl-py's `AsyncWebsocketClient` and ❌ `JsonRpcClient`.  this lets you "subscribe" to updates using aynchronous code, while also performing other requests / response actions in response to various events such as user input.

