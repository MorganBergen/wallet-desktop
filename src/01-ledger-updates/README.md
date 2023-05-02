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
    """
    A worker thread to watch for new ledger events and pass the info back to
    the main frame to be shown in the UI. Using a thread lets us maintain the
    responsiveness of the UI while doing work in the background.
    """
    def __init__(self, url, gui):
        Thread.__init__(self, daemon=True)
        # Note: For thread safety, this thread should treat self.gui as
        # read-only; to modify the GUI, use wx.CallAfter(...)
        self.gui = gui
        self.url = url
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.set_debug(True)

    def run(self):
        """
        This thread runs a never-ending event-loop that monitors messages coming
        from the XRPL, sending them to the GUI thread when necessary, and also
        handles making requests to the XRPL when the GUI prompts them.
        """
        self.loop.run_forever()

    async def watch_xrpl(self):
        """
        This is the task that opens the connection to the XRPL, then handles
        incoming subscription messages by dispatching them to the appropriate
        part of the GUI.
        """

        async with xrpl.asyncio.clients.AsyncWebsocketClient(self.url) as self.client:
            await self.on_connected()
            async for message in self.client:
                mtype = message.get("type")
                if mtype == "ledgerClosed":
                    wx.CallAfter(self.gui.update_ledger, message)

    async def on_connected(self):
        """
        Set up initial subscriptions and populate the GUI with data from the
        ledger on startup. Requires that self.client be connected first.
        """
        # Set up a subscriptions for new ledgers
        response = await self.client.request(xrpl.models.requests.Subscribe(
            streams=["ledger"]
        ))
        # The immediate response contains details for the last validated ledger.
        # We can use this to fill in that area of the GUI without waiting for a
        # new ledger to close.
        wx.CallAfter(self.gui.update_ledger, response.result)

```
