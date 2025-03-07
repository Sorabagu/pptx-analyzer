import wx

class ProgressDialog(wx.Dialog):
    def __init__(self, parent, title="Analyse en cours"):
        super().__init__(parent, title=title, size=(400, 150), style=wx.DEFAULT_DIALOG_STYLE)

        self.panel = wx.Panel(self)
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        # Texte explicatif
        self.info_text = wx.StaticText(self.panel, label="Analyse des fichiers en cours...\nVeuillez patienter.")
        self.vbox.Add(self.info_text, 0, wx.ALIGN_CENTER | wx.TOP, 15)

        # Barre de progression
        self.progress_bar = wx.Gauge(self.panel, range=100, size=(350, 25))
        self.vbox.Add(self.progress_bar, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        # Ajout au panel
        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)

    def update_progress(self, value):
        """Met à jour la barre de progression."""
        self.progress_bar.SetValue(value)
