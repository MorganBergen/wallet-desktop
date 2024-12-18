import xrpl
import wx
import asyncio
from threading import Thread

class XRPLMonitorThread(Thread):

    def __init__(self, url, gui):
        Thread.__init__(self, daemon = True)
        self.gui = gui
        self.url = url
        self.loop = asyncio.get_event_loop()
        self.loop.set_debug(True)

    def run(self):
        self.loop.run_forever()

    async def watch_xrpl(self):
        try:
            async with xrpl.asyncio.clients.AsyncWebsocketClient(self.url) as self.client:
                await self.on_connected()
                async for message in self.client:
                    mtype = message.get("type")
                    if mtype == "ledgerClosed":
                        wx.CallAfter(self.gui.update_ledger, message)
        except Exception as e:
            print(f"XRPL connection error: {e}")


    async def on_connected(self):
        response = await self.client.request(xrpl.models.requests.Subscribe(
            streams=["ledger"]
        ))
        wx.CallAfter(self.gui.update_ledger, response.result)

class TWaXLFrame(wx.Frame):

    def __init__(self, url):
        wx.Frame.__init__(self, None, title="TWaXDL", size=wx.Size(800, 400))
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

    def run_bg_job(self, job):
        task = asyncio.run_coroutine_threadsafe(job, self.worker.loop)

    def update_ledger(self, message):
        close_time_iso = xrpl.utils.ripple_time_to_datetime(message["ledger_time"]).isoformat()
        self.ledger_info.SetLabel(f"latest validated ledger:\n"
                                  f"ledger index: {message['ledger_index']}\n"
                                  f"ledger hash: {message['ledger_hash']}\n"
                                  f"close time: {close_time_iso}")

if __name__ == "__main__":
    WS_URL = "wss://s.altnet.rippletest.net:51233"
    app = wx.App()
    frame = TWaXLFrame(WS_URL)
    frame.Show()
    app.MainLoop()