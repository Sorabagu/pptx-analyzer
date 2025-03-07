# pptx.pyw
import sys
import wx
from scripts.gui.ui_main import MainWindow

class PPTXApp(wx.App):
    def OnInit(self):
        self.frame = MainWindow(None, title="PPTX Analyzer")
        self.frame.Show()
        return True

if __name__ == "__main__":
    app = PPTXApp(False)
    app.MainLoop()
