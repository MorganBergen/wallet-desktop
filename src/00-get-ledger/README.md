# latest validated ledger index with TWaXL

**contents**

1.  [brief](#brief)
2.  [output](#output)
3.  [description](#description)
4.  [script](#script)
5.  [background](#background)

# brief

the following scirpt will display a single window that returns a formatted string stating the latest validated ledger index on the xrp ledger testnet the init will instantiate the TWaXLFrame class and define a self.client variable as a JSON-RPC client using the method .JsonRpcClient(url) member method from the xrpl-py library.  this method connects to a public testnet server "https://s.altnet.rippletest.net:51234/" using the ledger method to get this data meanwhile it creates a wx.Frame subclass as the base of the user interface this class makes a window the user can see with a wx.StaticText widget to display text to the user and a wx.Panel to maintain that widget.

# output

![ui-twaxlframe](https://user-images.githubusercontent.com/65584733/218774838-9b521a28-2252-4abc-b417-4096ede32775.png)

# description

1.  `import xrpl`

the `xrpl-py` library for the this utilizes `python 3.7` || >, it is a pure python implementation for interacting with the xrp ledger.  the `xrpl-py` library simplifies the hardgest aspects of the xrp ledger interactions, such as serialization and transaction signing, by providing native python methods and models for the [xrp ledger transactions](https://xrpl.org/transaction-formats.html)

2.  `import wx`

the `wxpython` library is a cross-platform guideline user interface toolkit for python, it allows programmers to create programs with robuts, highly functional graphical user interfaces, simply.  it is implemented as a set of python extension modules that wrap the guii comoonents of the popular [`wxWidget`](https://github.com/wxWidgets/wxWidgets) cross platform library which is implemented in cpp.

3.  `class TWaXLFrame(wx.Frame)`

this class is a subclass of the wx.Frame class, it is the base of the user interface.  the `main()` we will construct an object called `frame` with the default constructor, the parameter we are passing is the `JSON_RPC_URL` which will be the `rippletest.net`

4.  `def __init__(self, url)`

this is the constructor for the TWaXLFrame class, it is called when the object is created, and will take the string literal `https://s.altnet.rippletest.net:51234/` as the first passby reference value parameter.

5.  `wx.Frame.__init__(self, None, title="TWaXL", size=wx.size(400, 400))`

`wx.Frame` is the base class for all top-level windows, it is the parent class of all other window classes.  the title will populate at the top of the window 



# background

1.  transaction reference

a transaction is the only way to cause changes in the xrp ledger.  transaction outcomes are only [final](https://xrpl.org/finality-of-results.html) if signed, submitted, and accepted into the validated ledger version following the consensus process.  some ledger rules also generate [pseudo-transactions](https://xrpl.org/pseudo-transaction-types.html), these are never submitted or signed, however they are required to be accepted by the network consensus protocol.  transactions that fail are also included in ledger becaus ethey modify balances of the xrp to pay for the ani-spam transaction cost.

2.  transaction types




2.  pseudo-transactions

pseudo-transactions are never submitted by users, nor are they propagated through the network.  instead a server may choose to inject pseudo-transctions in a proposed ledger directly according to specific protocol rule.  if enough servers propose the exect same pseudo-transaction, the consensus process approves it and the pseudo-transaction is inluded in that ledger's transaction data
