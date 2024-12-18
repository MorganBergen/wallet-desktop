#  gui and xrpl connection
import xrpl
import wx
import asyncio
from xrpl.asyncio.clients import AsyncWebsocketClient
from xrpl.models.requests import Ledger

class TWaXLFrame(wx.Frame):
    
    def __init__(self, url):
        wx.Frame.__init__(self, None, title="TWaXL", size = wx.Size(800, 400))
        self.url = url
        main_panel = wx.Panel(self)
        self.ledger_info = wx.StaticText(main_panel, label = "fetching ledger info...")

    async def get_validated_ledger(self):
        async with AsyncWebsocketClient(self.url) as client:
            try:
                response = await client.request(Ledger(ledger_index="validated"))

                if response.is_successful():
                    return f"latest validated ledger: {response.result['ledger_index']}"
                else:
                    return f"server resulted in an error: {response.result['error_message']}"

            except Exception as e:
                return f"failed to get validated ledger from server. ({e})"
            
    async def update_ledger_info(self):
        ledger_info = await self.get_validated_ledger()
        wx.CallAfter(self.ledger_info.SetLabel, ledger_info)

if __name__ == "__main__":
    JSON_RPC_URL = "wss://s.altnet.rippletest.net:51233/"
    app = wx.App()
    frame = TWaXLFrame(JSON_RPC_URL)
    frame.Show()
    asyncio.run(frame.update_ledger_info())
    app.MainLoop()