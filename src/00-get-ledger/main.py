'''
@file           main.py
@date           Tue Feb 14 08:17:52 CST 2023
@author         morgan bergen
@brief          the following scirpt will display a single window that returns a formatted string
                stating the latest validated ledger index on the xrp ledger testnet

@description    the init will instantiate the TWaXLFrame class and define a self.client variable
                as a JSON-RPC client using the method .JsonRpcClient(url) member method
                from the xrpl-py library.  this method connects to a public testnet server
                "https://s.altnet.rippletest.net:51234/" using the ledger method to get this data
                meanwhile it creates a wx.Frame subclass as the base of the user interface
                this class makes a window the user can see with a wx.StaticText widget to 
                display text to the user and a wx.Panel to maintain that widget
'''

import xrpl
import wx

class TWaXLFrame(wx.Frame):

    def __init__(self, url):
        wx.Frame.__init__(self, None, title="morgan's xrp ledger validated index viewer", size=wx.Size(400, 200))
        self.client = xrpl.clients.JsonRpcClient(url)

        main_panel = wx.Panel(self)
        self.ledger_info = wx.StaticText(main_panel, label=self.get_validated_ledger())

    def get_validated_ledger(self):
        try:
            response = self.client.request(xrpl.models.requests.Ledger(ledger_index="validated"))

        except Exception as e:
            return f"Failed to get validated ledger from server. ({e})"

        if response.is_successful():
            return f"\n\n\t\tLatest validated ledger index: {response.result['ledger_index']}"
        else:
            return f"Server returned an error:  {response.result['error_message']}"


if __name__ == "__main__":
    # json rpc client url is here
    JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
    app = wx.App()
    frame = TWaXLFrame(JSON_RPC_URL)
    frame.Show()
    app.MainLoop()
