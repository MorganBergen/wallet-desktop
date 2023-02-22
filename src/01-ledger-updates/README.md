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

the following libraries must be imported into the current main module youre working in

```python
import asyncio
from threading import Thread    
```

`import asyncio` is used to create a new event loop for the worker thread, and to run the `AsyncWebsocketClient` in the worker thread.  `from threading import Thread` is used to create a new thread for the worker thread.

`from threading import Thread` is used to create a new thread for the worker thread.

```python
class XRPLMonitorThread(Thread):
    '''
    this will be the worker thread to watch for new ledger event updates and will be used to 
    pass information back to the main frame to be shown in the user interface
    using a thread let us maintain the gui responsiveness while doing work in the background
    '''
    
    # default constructor to initialize url, gui, and event loop
    def __init__(self, p_url, p_gui):
        self.gui = p_gui
        self.url = p_url
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.set_debug(True)

    def run(self):
        self.loop.run_forever()

    async def watch_xrpl(self):
        











```
