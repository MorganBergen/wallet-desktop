# latest validated ledger with [`JsonRpcClient() protocol`](https://xrpl-py.readthedocs.io/en/stable/source/xrpl.clients.html#xrpl.clients.JsonRpcClient)  


**contents**

0.  [view code](https://github.com/MorganBergen/wallet-desktop/blob/main/src/00-get-ledger/main.py)
1.  [brief](#brief)
2.  [output](#output)
3.  [description](#description)
4.  [script](#script)
5.  [background](#background)

# brief

the following scirpt will display a single window that returns a formatted string stating the latest validated ledger index on the xrp ledger testnet the init will instantiate the TWaXLFrame class and define a self.client variable as a JSON-RPC client using the method .JsonRpcClient(url) member method from the xrpl-py library.  this method connects to a public testnet server "https://s.altnet.rippletest.net:51234/" (note that if you click on this link right now you will recieve an erro stating undefined object, meaning it can only be accessed default class construction.  the connection using the ledger method will get this data and meanwhile it creates a wx.Frame subclass as the base of the user interface this class makes a window the user can see with a wx.StaticText widget to display text to the user and a wx.Panel to maintain that widget.

the `JsonRpcClient()` protocol is used for this software application to interact with the xrp blockchain, either by reading blockchain data or by sending transactions to the network, and it be connected to an xrpl node. it will invoke a `RPCCall.cpp` module within the `XRPLF/rippled/src/ripple/net/impl/RPCCall.cpp` view [RPC client protcol here](https://github.com/XRPLF/rippled/blob/5834fbbc5d5f7354f2ba4e8426391f8ff112c744/src/ripple/net/impl/RPCCall.cpp)


# output

![ui](https://user-images.githubusercontent.com/65584733/218776766-78d3ae0f-cc0d-4757-9983-b7c0ec3d533d.png)

**request format for ledger index data**

```python
{
    "method": "ledger",
    "params": [
        {
            "ledger_index": "validated",
            "accounts": false,
            "full": false,
            "transactions": false,
            "expand": false,
            "owner_funds": false
        }
    ]
}
```

the ledger index of the ledger to use is a 32-bit unsigned integer used ot identify the ledger and is also known as the ledger's sequence number.

# description of code

1.  `import xrpl`

the `xrpl-py` library for the this utilizes `python 3.7` || >, it is a pure python implementation for interacting with the xrp ledger.  the `xrpl-py` library simplifies the hardgest aspects of the xrp ledger interactions, such as serialization and transaction signing, by providing native python methods and models for the [xrp ledger transactions](https://xrpl.org/transaction-formats.html)

2.  `import wx`

the `wxpython` library is a cross-platform guideline user interface toolkit for python, it allows programmers to create programs with robuts, highly functional graphical user interfaces, simply.  it is implemented as a set of python extension modules that wrap the guii comoonents of the popular [`wxWidget`](https://github.com/wxWidgets/wxWidgets) cross platform library which is implemented in cpp.

3.  `class TWaXLFrame(wx.Frame)`

this class is a subclass of the wx.Frame class, it is the base of the user interface.  the `main()` we will construct an object called `frame` with the default constructor, the parameter we are passing is the `JSON_RPC_URL` which will be the `rippletest.net`

4.  `def __init__(self, url)`

this is the constructor for the TWaXLFrame class, it is called when the object is created, and will take the string literal `https://s.altnet.rippletest.net:51234/` as the first passby reference value parameter.

5.  `wx.Frame.__init__(self, None, title="TWaXL", size=wx.size(400, 400))`

`wx.Frame` is the base class for all top-level windows, it is the parent class of all other window classes.  the title will populate at the top of the window.

6.  `self.client = xrpl.clients.JsonRpcClient(url)`

this declaraction creates a new instance of the `JsonRpcClient` class which is used to send `JSON-RPC` requests to the xrp ledger server at the specified `url`.  in classic pythonic programming `self` keyword refers to the instance of the class that the method `JsonRpcClient()` method is being called on.  by creating this instance of the `JsonRpcClient` class, you are grated access to send requests to the xrp ledger server.  this is a `sync` meaning syncronous client for interacting the rippled `JSON RPC` the request returns the response.

`@param     url str literal = https://s.altnet.rippletest.net:51234/`
`@return    The Response for the given Request such is the case with the ledger method`

7.  `main_panel = wx.Panel(self)`

this is a wx.Panel widget, it is a simple container that can be used to group other widgets.  it is the parent class of all other widgets, and is the base class for all other panel classes.  it is used to maintain the `wx.StaticText` widget.

8.  `self.ledger_info = wx.StaticText(main_panel, label=self.get_validated_ledger())`

declaring the public member variable `ledger_info` as a `wx.StaticText` widget, it will be used to display the text to the user.  the `label` parameter will be the `self.get_validated_ledger()` method which will return the latest validated ledger index. 

9.  `def get_validated_ledger(self)`

when the default constructor is executed and `self.ledger_info` attempts to become defined the parameter for `wx.StaticText` will contain the `label` which is an embedded declaration for `get_validated_ledger()` invokation.  the member method will utilize try catch blocks in order to request a reponse from the ledger at `ledger_index="validated"`.

10.  `try:`

the `try` block will attempt to execute the code within the block, if an exception is raised, the `except` block will be executed.

11.  `response = self.client.request(xrpl.models.requests.Ledger(ledger_index="validated"))`

-  `self.client`

the `self.client` is an instance of the `JsonRpcClient` class, which is used to interact with the xrp ledger using the JSON-PRC protocol.


-  `self.client.request()`  the request method of the `JsonRpcClient` class is used to send the `JSON-RPC` requests to the XRP ledger server and recieve responses.

-  `xrpl.models.requests.Ledger`  the specific request being sent is an instance of the `xrpl.models.requests.Ledger` class which requests information about a specific ledger on the XRP Ledger network.

-  `Ledger(ledger_index="validated")`  the `ledger_index` parameter is set to `validated` which insinuates that the request is specifically for the latest validated ledger on the network. 

-  `response`  finally the `=` assignment operates instantiates the return value of the `self.client.request(xrpl.models.requests.Ledger(ledger_index="validated"))` call.  this variable contains the main information returned by the server and the content of the response will be contingent on the specific request being made, however it will typically be returned in `JSON` format and will have to be parsed and processed in some way by calling the program.

12.  `except Exception as e`

the `except` block will be executed if an exception is raised in the `try` block.  the `Exception` class is the base class for all built-in exceptions, it is the base class for all exceptions that are not explicitly handled by the `except` block.  the `as` keyword is used to bind the exception to a variable, in this case `e`.  want to learn more about exceptions in python?  check out this [link](https://morganbergen.notion.site/exceptions-691ce799ff384a77bbf8c924c1ad25c3) and run it in your program to see expectations on output.

13.  `return f"Failed to get validated ledger from server. ({e})"`

if an exception is caught then the TWaXLFrame container will have the string indicated that the validated ledger from the server could not be reached.  `e` in this case will be the error message

14  `if response.is_successful():`

the `is_successful()` method is a method of the `xrpl.models.requests.Ledger` class, it is used to determine if the request was successful.  if the request was successful then the `if` block will be executed.

15.  `return f"\n\n\t\tLatest validated ledger index: {response.result['ledger_index']}"`

the `response.result` is a dictionary that contains the response from the server, the `ledger_index` key will contain the latest validated ledger index.

16.  `else:`

if the `if` block was not executed then the `else` block will be executed.

17.  `return f"Server returned an error:  {response.result['error_message']}"`

18.  `if __name__ == "__main__":`

the `if __name__ == "__main__":` block is used to execute the `main()` function when the program is run.  the `__name__` variable is a built-in variable that is set to the name of the module.  if the module is being run directly by the interpreter, the `__name__` variable will be set to the string literal `__main__`.  if the module is being imported from another module, the `__name__` variable will be set to the name of the module.

19.  `JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"`

the `JSON_RPC_URL` variable is a string literal that contains the url for the xrp ledger server.

20.  `app = wx.App()`

the `wx.App()` class is the main application object.  it is used to initialize the wxPython application, and create the top-level window.  it is the first object that should be created when using wxPython.  the `app` variable is an instance of the `wx.App()` class.

21.  `frame = TWaXLFrame(JSON_RPC_URL)`

the `frame` variable is an instance of the `TWaXLFrame` class, it is the main window of the application.

22.  `frame.Show()`

the `Show()` method is a method of the `wx.Frame` class, it is used to show the frame on the screen.

23.  `app.MainLoop()`

the `MainLoop()` method is a method of the `wx.App` class, it is used to start the main event loop.  the main event loop is the main loop of the application, it is used to process events and dispatch them to the appropriate event handlers.  the main event loop is started by calling `MainLoop()` and is terminated by calling `ExitMainLoop()`.

# background

1.  transaction reference

a transaction is the only way to cause changes in the xrp ledger.  transaction outcomes are only [final](https://xrpl.org/finality-of-results.html) if signed, submitted, and accepted into the validated ledger version following the consensus process.  some ledger rules also generate [pseudo-transactions](https://xrpl.org/pseudo-transaction-types.html), these are never submitted or signed, however they are required to be accepted by the network consensus protocol.  transactions that fail are also included in ledger becaus ethey modify balances of the xrp to pay for the ani-spam transaction cost.

2.  pseudo-transactions

pseudo-transactions are never submitted by users, nor are they propagated through the network.  instead a server may choose to inject pseudo-transctions in a proposed ledger directly according to specific protocol rule.  if enough servers propose the exect same pseudo-transaction, the consensus process approves it and the pseudo-transaction is inluded in that ledger's transaction data
