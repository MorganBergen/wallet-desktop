#  getting started using python library

walks through the basics of building an xrp ledger connected application using [`xrpl-py`](https://github.com/XRPLF/xrpl-py), a pure python library to interact with the xrp ledger using native python models and methods.  this tutorial is intended for beginners and should take no longer than 30 minutes to complete.

####  learning goals

basic building blocks of xrp ledger based applications

how to connect to the xrp ledger using `xrpl-py`

how to get an account on the [testnet](https://xrpl.org/resources/dev-tools/xrp-faucets) using `xrpl-py`

how to use the `xrpl-py` library to look up information about an account on the xrp ledger

how to put these steps together to create a python app

####  requirements

the `xrpl-py` library supports > python 3.7 and later

####  installation

the `xrpl-py` cab be installed with `pip3 install xrpl-py`

####  start building

when you're working with the xrp ledger, there are a few things you'll need to manage, whether you're adding xrp to your account, integrating with the decentralized exchange, or issuing tokens.  this tutorial walks you through basic patterns common to getting started with all of these use cases and provides sample code for implementing them.  here are the basic steps you'll need to cover for almost any xrp ledger project

[1.  connect to the xrp ledger](#1--connect-to-the-xrp-ledger)  
[2.  get an account](#2--get-an-account)  
[3.  query the xrp ledger](#3--query-the-xrp-ledger)    
[4.  putting it all together](#4--putting-it-all-together)  

####  1.  connect to the xrp ledger

in order to make queries and submit transactions, you need to connect to the xrp ledger.  to do this with `xrpl-py`, use the [`xrpl.clients.module`](https://xrpl-py.readthedocs.io/en/latest/source/xrpl.clients.html)


```Python
#  Define the network client
from xrpl.clients import JsonRpcClient

JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"

client = JsonRpcClient(JSON_RPC_URL)
```

####  connect to the production xrp ledger

the sample code previously shows how to connect to the testnet, which is a parallel network for testing where the money has no real value.  when you're ready to integrate with the production xrp ledger, you'll need to connect to the mainnet. 

(option 1)  by installing the core server (`rippled`) and running a node yourself.  the core server connects to the mainnet by default, but you can change the configuration to use testnet or devnet.  there are good reasons to run your own core server.  if you run your own server you can connect to it as follows

```Python
from xrpl.clients import JsonRpcClient

JSON_RPC_URL = "http://localhost:5005/"

client = JsonRpcClient(JSON_RPC_URL)
```

(option 2)  by using one of the available public servers.

```Python
from xrpl.clients import JsonRpcClient

JSON_RPC_URL = "https://s2.ripple.com:51234/"

client = JsonRpcClient(JSON_RPC_URL)
```

####  2.  get an account

to store value and execute transactions on the xrp ledger, you need an account:  a set of keys and an address that's been funded with enough xrp to meet account reserve.  the address is the identifier of your account and you use the private key to sign transactions that you submit to the xrp ledger.

for testing and development purpose, you can use the xrp faucets to generate keys and fund the account on the testnet or devnet.  for production purposes, you should take care to store your keys and set up a secure signing method.  another difference in production is that xrp has real worth, so you can't get it for free from a faucet.  

to create and fund an account on the testnet, `xrpl-py` provides the `generate_faucet_wallet` method

```Python
#  create a wallet using the testnet faucet
#  https://xrpl.org/xrp-testnet-faucet.html

from xrpl.wallet import generate_faucet_wallet

test_wallet = generate_faucet_wallet(client, debug=True)

print(test_wallet)

'''
print output

public_key:: 022FA613294CD13FFEA759D0185007DBE763331910509EF8F1635B4F84FA08AEE3
private_key:: -HIDDEN-
classic_address: raaFKKmgf6CRZttTVABeTcsqzRQ51bNR6Q
'''
```

####  using the account  

in this tutorial we only query details about the generated account from the xrp ledger, but you can use the values in the `Wallet` instance to prepare, sign, and submit transactions with `xrpl-py`

####  prepare 

to prepare the transaction

```Python
#  prepare payment

from xrpl.models.transactions import Payment

from xrpl.utils import xrp_to_drops

my_tx_payment = Payment(
    account = test_account,
    amount = xrp_to_drops(22),
    destination = "rPT1Sjq2YGrBMTttX4GZHjKu9dyfzbpAYe",
)
```

####  sign and submit

to sign and submit the transaction

```Python
#  sign and submit the transaction

from xrpl.transaction import submit_and_wait

tx_response = submit_and_wait(my_tx_payment, client, test_wallet)
```

####  derive an x-address

you can use `xrpl-py`'s `xrpl.core.addresscodec` module to derive an x-address from the `Wallet.address` field

```Python
#  derive an x-address from the classic address
#  https://xrpaddress.info/

from xrpl.core import addresscodec

test_xaddress = addresscodec.classic_address_to_xaddress(test_account, tag = 12345, is_test_network = True)

print("\nclassic address:\n\n", test_account)

print("x-address:\n\n", test_xaddress)
```

the x-address format packs the address and destination tag into a more user friendly value

####  3.  query the xrp ledger

you can query the xrp ledger to get information about a specific account, a specific transaction, the state of the current or historical ledger, and the xrp ledger's decentralized exchange.  you need to make these queries, among other reasons, to look up account info to follow best practice for reliable transaction submission.

here we use the `xrpl-py`'s `xrpl.account` module to look up information about the account we got in the previous step

```Python
#  look up account info
from xrpl.models.requests.account_info import AccountInfo
import json

acct_info = AccountInfo(
    account = test_account.classic_address,
    ledger_index = "validated",
    strict = True,
)

response = client.request(acct_info)
result = response.result

print("response.status:", response.status)

print(json.dumps(response.result, indent = 4, sort_keys = True))
```

####  4.  putting it all together

using these building blocks we can create a python app that,

1.  gets an account on the testnet
2.  connects to the xrp ledger
3.  looks up and prints information about the account you created

```Python
#  define the network client
from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet
from xrpl.core import addresscodec
from xrpl.models.requests.account_info import AccountInfo
import json

#  define network client
JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
client = JsonRpcClient(JSON_PRC_URL)

#  create a wallet using the testnet faucet https://xrpl.org/xrp-testnet-faucet.html
test_wallet = generate_faucet_wallet(client, debug=True)

#  initialize an account str from the wallet
test_account = test_wallet.classic_address

#  derive x address from the classic address https://xrpaddress.info/
test_xaddress = addresscodec.classic_address_to_xaddress(test_account, tag = 12345, is_test_network = True)
print("nclassic address:", test_account)
print("x-address:", test_xaddress)

#  lookup account info about your account
acct_info = AccountInfo(
    account = test_account,
    ledger_index = "validated",
    strict = True,
)

response = client.request(acct_info)
result = response.result

print("response.status:", response.status)
print(json.dumps(response.result, indent = 4, sort_keys = True))

'''
expected output

Classic address:

 rnQLnSEA1YFMABnCMrkMWFKxnqW6sQ8EWk
X-address:

 T7dRN2ktZGYSTyEPWa9SyDevrwS5yDca4m7xfXTGM3bqff8
response.status:  ResponseStatus.SUCCESS
{
    "account_data": {
        "Account": "rnQLnSEA1YFMABnCMrkMWFKxnqW6sQ8EWk",
        "Balance": "1000000000",
        "Flags": 0,
        "LedgerEntryType": "AccountRoot",
        "OwnerCount": 0,
        "PreviousTxnID": "5A5203AFF41503539D11ADC41BE4185761C5B78B7ED382E6D001ADE83A59B8DC",
        "PreviousTxnLgrSeq": 16126889,
        "Sequence": 16126889,
        "index": "CAD0F7EF3AB91DA7A952E09D4AF62C943FC1EEE41BE926D632DDB34CAA2E0E8F"
    },
    "ledger_current_index": 16126890,
    "queue_data": {
        "txn_count": 0
    },
    "validated": false
}
'''
```

####  interpreting the response

the response fields that you want to inspect in most cases are `account_data.Sequence`, `account_data.Balance`, and `validated`.

`account_data.Sequence` -  this is the sequence number of the next valid transaction for the account.  you need to specify the sequence number when you prepare transactions.  with `xrpl-py`, you can use the `get_next_valid_seq_number` to get this automatically from the xrp ledger.

`account_data.Balance` -  the account's balance of the xrp in drops. you can use this to confirm that you have enough xrp to send (if you're making a payment) and to meet the current transaction cost for a given transaction.

`validated` -  indicates whether the returned data is from a validated ledger.  when inspecting transactions, it's important to confirm that the results are final before further processing the transaction.  if `validated` is `true`, then you know for sure the results won't change.

--------------------------------------------------

#  build a desktop wallet app

0.  install dependencies
1.  hello world
2.  show ledger updates
3.  display an account
4.  show account's transactions
5.  send xrp
6.  domain verification and polish

####  0.  install dependencies

this tutorial depends on various programming libraries.  before you start, you should install all of them.  `pip3 install --upgrade xrpl-py WxPython requests toml`

`xrpl-py` - the client library for the xrp ledger

`wxPython` - cross platform graphical toolkit

`Requests` -  a library for making http requests

`toml` - a library for parsing toml formatted files

the `requests` and `toml` libraries are only needed for the domain verification in step 6, but you can install them now while you're installing other dependencies.


####  1.  hello world

app that combines hello world equivalents for the xrp ledger and wxpython programming

```Python
import xrpl
import wx

class TWaXLFrame(wx.Frame):
  
  def __init__(self, url):
    wx.Frame.__init__(self, None, title="TWaXL", size=wx.Size(800, 400))
    self.client = xrpl.clients.JsonRpcClient(url)
    main_panel = wx.Panel(self)
    self.ledger_info = wx.StaticText(main_panel, label = self.get_validated_ledger())

  def get_validated_ledger(self):
    try:
      response = self.client.request(xrpl.models.requests.Ledger(
        ledger_index="validated"
      ))
    
    except Exception as e:
      return f"failed to get validated ledger from sever ({e})"

    if response.is_successful():
      return f"latest validated ledger: {response.result['ledger_index']}"
    
    else:
      return f"server returned an error: {response.result['error_message']}"

if __name__ == "__main__":
  JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
  app = wx.App()
  frame = TWaXLFrame(JSON_RPC_URL)
  frame.Show()
  app.MainLoop()
```

after running the script, it display a single window that shows the latest validated ledger index on the xrp ledger testnet.  under the hood, the code makes a json-rpc client, connects to the testnet server, and uses the ledger method to get this information.  meanwhile it creates a `wx.Frame` subclass as the base as the base of the user interface.  this class amkes a window the user can see with a `wx.StaticText` widget to display text to the user, and a `wx.Panel` to hold that widget.

####  2.  show ledger updates

the first step only shows the latest validated ledger at the time you open it, the text displayed never changes unless you close the app and reopen it.  the actual xrp ledger is constantly making forward progress, so a more useful app would show it updating in real time.

if you want to updates (for example, waiting to see when new transaction have been confirmed), then you need to change the architecture of your app slightly.  for reasons specific to python, it's best to use two threads, a `gui` thread to handle user input and display and a `worker` thread for xrp ledger network connectivity.  the operating system can switch quickly between the two threads at any time, so the use interface can remain responsive while the background thread waits on information from the network that may take a while to arrive.  the main challenge with threads is that you have to be careful not to access data from one thread that another thread is in the middle of changing.  a straightforward way to do this is to design your program so that each thread has variables it "owns" and doesn't write to the other thread's variables.  in this program each thread is its own class, so each thread should only write to its own class attributes (anything starting with `self`).  when the threads need to communicate, they use specific "thread-safe" methods of communication 

`asyncio.run_coroutine_threadsafe()` - for `gui` thread to `worker` thread communication

`wx.CallAfter()` - for `worker` thread to `gui` thread communication

to make full use of the xrp ledger's ability to push messages to the client, use `xrpl-py`'s `AsyncWebsocketClient` instead of `JsonRpcClient`.  this lets you subscribe to updates using asynchronous routines, while also performing other request/response operations in response to various events such as user input.

add these imports at the top of the file

```Python
import asyncio
from threading import Thread
```

then, the code for the monitor thread is as follows (put this in the same file as the rest of the app)

```Python

class XRPLMonitorThread(Thread):
  
  '''
  a worker thread to watch for new ledger events and pass the info back to 
  the main frame to be shown in the ui.  using a thread lets us maintain the
  responsiveness of the ui while doing work in the background
  note for thread safety, this thread should treat self.gui as read only to 
  modify the gui, use wx.CallAfter(...)
  '''
  def __init__(self, url, gui):
    Thread.__init__(self, daemon=True)  
    self.gui = gui
    self.url = url
    self.loop = asyncio.new_event_loop()
    asyncio.set_event_loop(self.loop)
    self.loop.set_debug(True)

  '''
  this thread runs a never ending event loop that monitors messages 
  coming from xrpl, sending them to the gui thread when necessary, and also
  handles making requests to the xrpl when the gui prompts them
  '''
  def run(self):
    self.loop.run_forever()

  '''
  this is the task that opens the connection to the xrpl, then handles incoming 
  subscription messages by dispatching them to the appropriate part of the gui
  '''
  async def watch_xrpl(self):
    async with xrpl.asyncio.clients.AsyncWebsocketClient(self.url) as self.client:
      await self.on_connected()
      async for message in self.client:
        mtype = message.get("type")
        if mtype == "ledgerClosed":
          wx.CallAfter(self.gui.update_ledger, message)

  '''
  set up initial subscriptions and populate the gui with data from the ledger on 
  startup.  requires that self.client be connected first
  set up a subscription for the new ledger
  the immediate response contains details for the last validated ledger
  we can use this to fill in that area of the gui without waiting for a new ledger to close
  '''
  async def on_connected(self):
    response = await self.client.request(xrpl.models.requests.Subscribe(
      streams=["ledger"]
    ))
    wx.CallAfter(self.gui.update_ledger, response.result)
```

this code defines a `Thread` subclass for the worker.  when the thread starts, it sets up an event loop, which waits for async tasks to be created and run.  the code uses `asyncio` debug mode so that the console shows any errors that occur in the async tasks.

the `watch_xrpl()` function is an example of such a task which the gui thread starts when its ready:
it connects to the xrp ledger, then calls the subscribe method to be notified whenever a new ledger is validated.  it uses the immediate response and all later subscription stream messages to trigger updates of the gui.

>  <p style="color:green"><code>tip</code></p>  
> 
>  define worker jobs like this usage `async def` instead of `def` so that
>  you can use the `await` keyword in them; you need to use `await` to get the response
>  to the `AsyncWebsocketClient.request()` method.  normally you would also need to use `await`
>  or something similar to get the response from any function you define with `async def`, but 
>  in this app, the `run_bg_job()` helper takes care of that in a different way

update the code for the main thread and gui frame to look like this

```Python

class TWaXLFrame(wx.Frame):

  def __init__(self, url):
    wx.Frame.__init__(self, None, title="TWaXL", size=wx.Size(800, 400))
    self.build_ui()
    self.worker = XRPLMonitorThread(url, self)
    self.worker.start()
    self.run_bg_job(self.worker.watch_xrpl())
  
  def build_ui(self):
    main_panel = wx.Panel(self)
    self.ledger_info = wx.StaticText(main_panel, label="Not connected")
    main_sizer = wx.BoxSizer(wx.VERTICAL)
    main_sizer.Add(self.ledger_info, 1, flag=wx.EXPAND|wx.ALL, border=5)
    main_panel.SetSizer(main_sizer)
  
  '''
  schedules a job to run asynchronously in the xrpl worker thread
  the job should be a future for example from calling an async function
  '''
  def run_bg_job(self, job):
    task = asyncio.run_coroutine_threadsafe(job, self.worker.loop)

  '''
  process a ledger subscription message to update the ui with information about the latest validated ledger
  '''
  def update_ledger(self, message):
    close_time_io = xrpl.utils.ripple_time_to_datetime(message["ledger_time"]).isoformat()
    self.ledger_info.SetLabel(f"latest validated ledger:\n"
                              f"ledger index: {message['ledger_index']}\n"
                              f"ledger hash: {message['ledger_hash']}\n"
                              f"close time: {close_time_iso}")

```

the part that build the gui has been moved to a separate method, `build_ui(self)`.  this helps to divide the code into chunks that are easier to understand, because the `__init__()` constructor has other work to do now, too:  it starts the worker thread, and give it its first job.  the gui setup also now uses a sizer to control placement of the text within the frame.

>  <p style="color:green"><code>tip</code></p>  
>
>  in this tutorial, all the gui code is written by hand but you may find it easier to create
>  powerful gui's using a build tool such as [`wxGlade`](https://wxglade.sourceforge.net) 
>  separating the gui code from the constructor may make it easier to switch to this type of approach later

there is a new helper method, `run_bg_job()`, which runs an asynchronous function (defined with `async def`) in the worker thread.  use this method any time you want the worker thread to interact with the xrp ledger network

instead of a `get_validated_ledger()` method, the gui class now has an `update_ledger()` method, which takes an object in the format of a ledger stream message and displays some of that information to the user.  the worker thread calls this method using `wx.CallAfter()` whenever it gets a `ledgerClosed` event from the ledger.

finally change the code to start the app (at the end of the file) slightly

```Python
if __name__ == "__main__":
  WS_URL = "wss://s.altnet.rippletest.net:51233"
  app = wx.App()
  frame = TWaXLFrame(WS_URL)
  frame.Show()
  app.MainLoop()
```

since the app uses a websocket client instead of the json rpc client now, the code has to use a websocket url to connect

>  <p style="color:green"><code>tip</code></p>  
>
>  if you run your own rippled server, you can connect to it using `wss://localhost:6006` as the url.  you can also use the websocket urls of public servers to connect to the mainnet or other networks.

####  3.  display an account

now that you have a working ongoing connection to the xrp ledger, it's time to start adding some "wallet" functionality that lets you manage an individual account.  for this step, you should prompt the user to input their address or master seed, then use that to display information about their account including how much xrp is set aside for the reserve requirement.

the prompt is a [popup dialog](https://xrpl.org/assets/python-wallet-3-enter.e101d4b952280998e99e6a24d1bd5feb1cd56792b8a734f87f1fa1b63145d867.ac57e6ef.png). after the user inputs the prompt, the updated gui looks like [this](https://xrpl.org/assets/python-wallet-3-main.1536465b77a1719e4e30f4592b2c8cdee0d33dce3ca7308c9e9df9b8f8912da5.ac57e6ef.png)

when you do math on xrp amounts, you should use the `Decimal` class so that you don't get rounding errors. add this to the top of the file with the other imports

`from decimal import Decimal`

in the `XRPLMonitorThread` class, rename and update the `watch_xrpl()` method as follows

```Python
'''
this is thge task that opens the connection to the xrpl, then handles incoming subscription messages
by dispatching them to the appropriate part of the gui
'''
async def watch_xrpl_account(self, address, wallet=None):
  self.account = address
  self.wallet = wallet

  async with xrpl.asyncio.clients.AsyncWebsocketClient(self.url) as self.client:
    await self.on_connect()
    async for message in self.client:
      mtype = message.get("type")
      if mtype == "ledgerClosed":
        wx.CallAfter(self.gui.update_ledger, message)
      elif mtype == "transaction":
        response = await self.client.request(xrpl.models.requests.AccountInfo(
          account = self.account,
          ledger_index = message["ledger_index"]
        ))
        wx.CallAfter(self.gui.update_account, response.result["account_data"])
```

the newly renamed `watch_xrpl_account()` method now takes an address and optional wallet and saves them for later.  the gui thread provides these based on user input.  this method also adds a new case for transaction stream messages.  when it sees a new transaction, the worker does not yet do anything with the transaction itself, but it uses that as a trigger to get the account's latest xrp balance and other info using the `account_info` method.  when that response arrives, the worker passes the account data to the gui for display.

still the `XRPLMonitorThread` class, update the `on_connected()` method as follows

```Python
'''
set up initial subscriptions and populate the gui with data from the ledger on startup
requires that self.client be connected first
'''
async def on_connected(self):
  
  '''
  set up 2 subscriptions - 
  all new ledgers and any new transactions that affect the chosen account
  '''
  response = await self.client.request(xrpl.models.requests.Subscribe(
    streams=["ledger"],
    accounts=[self.account]
  ))

  '''
  the immediate response contains details for the last validated ledger
  we can use this to fill in that area of the gui without waiting for a new ledger to close
  '''
  wx.CallAfter(self.gui.update_ledger, response.result)

  '''
  get starting values for account info
  '''
  response = await self.client.request(xrpl.models.requests.AccountInfo(
    account = self.account,
    ledger_index = "validated"
  ))
  
  '''
  this most often happens if the account in question doesn't exist on the network we're connected to
  better handling would be to use wx.CallAfter to display an error dialog in the gui and possibly
  allow the user to try inputting a different account
  '''
  if not response.is_successful():
    print("got error from server:", response)
    exit(1)
  
  wx.CallAfter(self.gui.update_account, response.result["account_data"])
```

the `on_connected()` method now subscribes to transactions for the provided account and the ledger stream too.  furthermore, it now calls `account_info` on startup, and passes the response to the gui for display.

the new gui has a lot more fields that need to be laid out in two dimensions.  the following subclass of `wx.GridBagSizer` provides a quick way to do so, setting the appropriate padding and sizing values for a two dimensional list of widgets.  add this code to the same file:

```Python
'''
helper class for adding a bunch of items uniformly to a gridbagsizer
'''
class AutoGridBagSizer(wx.GridBagSizer):

  def __init__(self, parent):
    wx.GridBagSizer.__init__(self, vgap = 5, hgap = 5)
    self.parent = parent

  '''
  given a two dimensional iterable `ctrls`, add all the items in a grid top to bottom, left to right
  with each inner iterable being a row.  set the total number of columns based on the longest iterable
  '''
  def BulkAdd(self, ctrls):
    flags = wx.EXPAND|wx.ALL|wx.RESERVE_SPACE_EVEN_IF_HIDDEN|wx.ALIGN_CENTER_VERTICAL
    for x, row in enumerate(ctrls):
      for y, ctrl in enumerate(row):
        self.Add(ctrl, (x, y), flag = flags, border = 5)
    
    self.parent.SetSizer(self)

```

update the `TWaXLFrame` constructor as follows

```Python
def __init__(self, url, test_network = True):
  
  wx.Frame.__init__(self, None, title = "TWaXL", size = wx.Size(800, 400))

  self.test_network = test_network

  #  the leger's current reserve setting, to be filled later
  self.reserve_base = None
  self.reserve_inc = None

  self.build_ui()

  #  pop up to ask user for their account -------------------------
  address, wallet = self.prompt_for_account()                      
                                                                   
  #  start background thread for update from the ledger -----------
  self.worker = XRPLMonitorThread(url, self)
  self.worker.start()
  self.run_bg_job(self.worker.watch_xrpl_account(address, wallet))

```

now the constructor takes a boolean to indicate whether it's connecting to a test network.  if you provide a mainnet url, you should also pass `False`.  it uses this to encode and decode x-address and warn if they're intended for a different network.  it also calls a new method, `prompt_for_account()` to get an address and wallet, and passes those to the renamed `watch_xrpl_account()` background job.

update the `build_ui()` method definition as follows

```Python
'''
called during __init__ to set up all the gui components
'''

    def build_ui(self):
        '''
        Called during __init__ to set up all the GUI components.
        '''
        main_panel = wx.Panel(self)

        self.acct_info_area = wx.StaticBox(main_panel, label="Account Info")

        lbl_address = wx.StaticText(self.acct_info_area, label="Classic Address:")
        self.st_classic_address = wx.StaticText(self.acct_info_area, label="TBD")
        lbl_xaddress = wx.StaticText(self.acct_info_area, label="X-Address:")
        self.st_x_address = wx.StaticText(self.acct_info_area, label="TBD")
        lbl_xrp_bal = wx.StaticText(self.acct_info_area, label="XRP Balance:")
        self.st_xrp_balance = wx.StaticText(self.acct_info_area, label="TBD")
        lbl_reserve = wx.StaticText(self.acct_info_area, label="XRP Reserved:")
        self.st_reserve = wx.StaticText(self.acct_info_area, label="TBD")

        aia_sizer = AutoGridBagSizer(self.acct_info_area)
        aia_sizer.BulkAdd( ((lbl_address, self.st_classic_address),
                           (lbl_xaddress, self.st_x_address),
                           (lbl_xrp_bal, self.st_xrp_balance),
                           (lbl_reserve, self.st_reserve)) )

        self.ledger_info = wx.StaticText(main_panel, label="Not connected")

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.acct_info_area, 1, flag=wx.EXPAND|wx.ALL, border=5)
        main_sizer.Add(self.ledger_info, 1, flag=wx.EXPAND|wx.ALL, border=5)
        main_panel.SetSizer(main_sizer)
```

this adds a `wx.StaticBox` with several new widgets, then uses the `AutoGridBagSizer` (defined above) to lay them out in 2x4 grid within the box.  these new widgets are all static text to display details of the account, through some of them start with placeholder text.  since they require data from the ledger, you have to wait for the worker thread to send that data back.

chnage the font weight of the static text to bold

>   <p style="font-weight: bold; color:orange">⚠️</p>
>   <p style="font-weight: bold; color:orange">WARNING</p>
>
>  change the font weight of the static text to bold
>


<p style="font-weight: bold"><code>code</code></p>
<p style="font-weight: bold; color:orange"><code>code</code></p>
<p style="font-weight: bold; color:green"><code>code</code></p>





####  development environment

building and running application in a containerized environment.  
a container is a standard unit of software that packages up code and 
dependencies and runs them in an isolated environment.

`docker init`

```bash
~/wallet-desktop
❯ docker init

Welcome to the Docker Init CLI!

This utility will walk you through creating the following files with sensible defaults for your project:
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

Let's get started!

? What application platform does your project use?  [Use arrows to move, type to filter]
  Go - suitable for a Go server application
> Python - suitable for a Python server application
  Node - suitable for a Node server application
  Rust - suitable for a Rust server application
  ASP.NET Core - suitable for an ASP.NET Core application
  PHP with Apache - suitable for a PHP web application
  Java - suitable for a Java application that uses Maven and packages as an uber jar
  Other - general purpose starting point for containerizing your application
  Don't see something you need? Let us know!

  ? What application platform does your project use? Python
  ? What version of Python do you want to use? (3.10.11) 
  ? What port do you want your app to listen on? 8000
  ? What is the command you use to run your app (e.g., gunicorn 'myapp.example:app' --bind=0.0.0.0:8000)? python main.py

✔ Created → .dockerignore
✔ Created → Dockerfile
✔ Created → compose.yaml
✔ Created → README.Docker.md

✔ Created → .dockerignore
✔ Created → Dockerfile
✔ Created → compose.yaml
✔ Created → README.Docker.md

→ Your Docker files are ready!
  Review your Docker files and tailor them to your application.
  Consult README.Docker.md for information about using the generated files.

  What's next?
    Start your application by running → docker compose up --build
    Your application will be available at http://localhost:8000

  Quit
```

docker file is a text document that contains all of the commands to assemble an image.  

[`Dockerfile`](https://docs.docker.com/reference/dockerfile/)

[`docker-compose.yml`](https://docs.docker.com/reference/compose-file/)

[`README.Docker.md`](https://docs.docker.com/reference/compose-file/)

`docker init`

`docker-compose up --build`

`docker ps`

`docker exec -it <container_id_or_name> /bin/bash`


### error due to missing X display

error message `Unable to access the X Display, is $DISPLAY set properly?`

the error unable to access the x display, is $DISPLAY set properly indicates that the application is trying to access a graphical display but it cannot find one.  this is a common issue when running gui applications inside docker containers because they don't have access to the host's display by default

1.  use x11 forwarding 

you can forward the x11 display from your host to the docker container, this requires setting up your docker container to use the host's x server.

1.  run the docker container with x11 forwarding - youll need to pass the display environment variable and mount the x11 socket

`docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:rw <image_name>`

2.  allow connections to the x server

on your host machine run `xhost +local:docker` to allow local docker containers to connect to the xserver

update the `compose.yaml` file to include the display environment variable and mount the x11 socket

```yml
services:
  server:
    build:
      context: .
    ports:
      - 8000:8000
    environment:
      - DISPLAY=${DISPLAY} # pass the display environment variable to the container
    volumes:
      - /tmp/.X11-unix:/tmp/.X11-unix:rw
```

```
~/Documents/03-GitHub                                                                        02:43:57 PM
❯ xhost +local:docker
non-network local connections being added to access control list
```

`xhost + 127.0.0.1` -> `127.0.0.1 being added to access control list`

authorization for docker to connect to the x server

make sure to download and install `XQuartz` from https://www.xquartz.org

#  run commands

`xhost + 127.0.0.1`

`docker-compose up --build`

`xhost +local:docker`

