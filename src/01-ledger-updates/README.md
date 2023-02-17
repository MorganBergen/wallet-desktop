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

thus for reasons specific to python, it's best to use two _threads_, a gui thread in order to handle user input and display, and a worker thread for xrp ledger network connectivity.  the operating system can switch quickly between the two threads at any time, so the user interface can remain responsive while the background worker threads waits on information from the network that may take a while to arrive.


