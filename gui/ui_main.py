import wx
import wx.lib.agw.aui as aui
import os
import subprocess
from scripts.gui.ui_manager import UIManager

class MainWindow(wx.Frame):
    def __init__(self, parent, title="PPTX Analyzer"):
        super().__init__(parent, title=title, size=(1200, 700), style=wx.DEFAULT_FRAME_STYLE)

        # Définition de l'icône de la fenêtre
        icon_path = os.path.join(os.getcwd(), "img/icon.png")
        if os.path.exists(icon_path):
            self.SetIcon(wx.Icon(icon_path, wx.BITMAP_TYPE_PNG))

        # Activer le mode sombre
        self.SetBackgroundColour("#181818")

        # Ajouter la barre de menu
        self.create_menu_bar()

        # Initialisation de l'interface
        self.init_ui()

        # Initialisation du gestionnaire UI
        self.ui_manager = UIManager(self)

    def init_ui(self):
        """Initialise l'interface moderne."""
        panel = wx.Panel(self)
        panel.SetBackgroundColour("#181818")

        # --- Sizer principal ---
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # === SIDEBAR (MENU LATÉRAL) ===
        sidebar = wx.Panel(panel, size=(250, -1))
        sidebar.SetBackgroundColour("#1E1E1E")
        sidebar_sizer = wx.BoxSizer(wx.VERTICAL)

        # Logo et titre
        icon_path = os.path.join(os.getcwd(), "img/icon.png")
        if os.path.exists(icon_path):
            bmp = wx.Bitmap(icon_path, wx.BITMAP_TYPE_PNG)
            self.avatar = wx.StaticBitmap(sidebar, bitmap=bmp)
            sidebar_sizer.Add(self.avatar, 0, wx.ALIGN_CENTER | wx.TOP, 20)

        title_text = wx.StaticText(sidebar, label="PPTX Analyzer", style=wx.ALIGN_CENTER)
        title_text.SetForegroundColour(wx.Colour(255, 255, 255))
        title_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title_text.SetFont(title_font)
        sidebar_sizer.Add(title_text, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)

        # Boutons de navigation
        self.scan_btn = self.create_modern_button(sidebar, "📂 Analyser")
        self.search_btn = self.create_modern_button(sidebar, "🔎 Rechercher", enabled=False)
        self.open_btn = self.create_modern_button(sidebar, "📂 Ouvrir", enabled=False)  # Nouveau bouton

        sidebar_sizer.Add(self.scan_btn, 0, wx.EXPAND | wx.ALL, 5)
        sidebar_sizer.Add(self.search_btn, 0, wx.EXPAND | wx.ALL, 5)
        sidebar_sizer.Add(self.open_btn, 0, wx.EXPAND | wx.ALL, 5)  # Ajout du bouton ouvrir

        sidebar.SetSizer(sidebar_sizer)

        # === CONTENU PRINCIPAL ===
        content_panel = wx.Panel(panel)
        content_panel.SetBackgroundColour("#181818")

        content_sizer = wx.BoxSizer(wx.VERTICAL)

        # Barre de recherche améliorée
        search_panel = wx.Panel(content_panel)
        search_panel.SetBackgroundColour("#252525")

        self.search_input = wx.TextCtrl(search_panel, style=wx.TE_PROCESS_ENTER, size=(500, 35))
        self.search_input.SetBackgroundColour("#333")
        self.search_input.SetForegroundColour(wx.Colour(255, 255, 255))

        # Définition d'une police plus grande pour centrer verticalement
        font = wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.search_input.SetFont(font)

        self.search_input.SetHint("🔍 Rechercher dans les fichiers .pptx...")

        # Liste des fichiers trouvés (UI améliorée)
        self.file_list = wx.ListCtrl(content_panel, style=wx.LC_REPORT | wx.BORDER_NONE)
        self.file_list.InsertColumn(0, "Nom du fichier", width=250)
        self.file_list.InsertColumn(1, "Chemin", width=300)
        self.file_list.InsertColumn(2, "Date de modification", width=150)
        self.file_list.InsertColumn(3, "Taille", width=100)  # Nouvelle colonne pour la taille des fichiers

        # Style des en-têtes
        self.file_list.SetBackgroundColour("#252525")
        self.file_list.SetForegroundColour(wx.Colour(255, 255, 255))
        self.file_list.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        # Ajout des éléments à l'affichage
        content_sizer.Add(search_panel, 0, wx.EXPAND | wx.ALL, 10)
        content_sizer.Add(self.file_list, 1, wx.EXPAND | wx.ALL, 10)

        content_panel.SetSizer(content_sizer)

        # Ajout des panneaux au layout principal
        main_sizer.Add(sidebar, 0, wx.EXPAND | wx.ALL, 0)
        main_sizer.Add(content_panel, 1, wx.EXPAND | wx.ALL, 0)

        panel.SetSizer(main_sizer)

        # Gestion des événements pour activer/désactiver le bouton "Ouvrir"
        self.file_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_file_selected)
        self.file_list.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_file_deselected)
        self.open_btn.Bind(wx.EVT_BUTTON, self.on_open_file)

        # Centrage de la fenêtre
        self.Centre()

    def create_modern_button(self, parent, label, enabled=True):
        """Crée un bouton moderne stylisé."""
        btn = wx.Button(parent, label=label, size=(200, 45))
        btn.SetForegroundColour(wx.Colour(255, 255, 255))
        btn.SetBackgroundColour("#3E3E42")
        btn.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        btn.Enable(enabled)

        # Effet au survol
        btn.Bind(wx.EVT_ENTER_WINDOW, lambda event: btn.SetBackgroundColour("#4E4E52"))
        btn.Bind(wx.EVT_LEAVE_WINDOW, lambda event: btn.SetBackgroundColour("#3E3E42"))

        return btn

    def create_menu_bar(self):
        """Crée la barre de menu avec 'Fichier' et '?'."""
        menu_bar = wx.MenuBar()

        # Menu "Fichier"
        file_menu = wx.Menu()
        exit_item = file_menu.Append(wx.ID_EXIT, "Quitter\tAlt+F4")
        self.Bind(wx.EVT_MENU, self.on_quit, exit_item)

        # Menu "?"
        help_menu = wx.Menu()
        about_item = help_menu.Append(wx.ID_ABOUT, "À propos")
        self.Bind(wx.EVT_MENU, self.on_about, about_item)

        # Ajouter les menus à la barre
        menu_bar.Append(file_menu, "Fichier")
        menu_bar.Append(help_menu, "?")

        # Appliquer la barre de menu
        self.SetMenuBar(menu_bar)

    def on_quit(self, event):
        """Ferme l'application."""
        self.Close()

    def on_about(self, event):
        """Affiche une boîte de dialogue 'À propos'."""
        wx.MessageBox(
            "PPTX Analyzer v1.0\nAnalyse et recherche avancée dans les fichiers PowerPoint.",
            "À propos",
            wx.OK | wx.ICON_INFORMATION
        )

    def on_file_selected(self, event):
        """Active le bouton 'Ouvrir' lorsqu'un fichier est sélectionné."""
        self.open_btn.Enable()

    def on_file_deselected(self, event):
        """Désactive le bouton 'Ouvrir' lorsqu'aucun fichier n'est sélectionné."""
        self.open_btn.Disable()

    def on_open_file(self, event):
        """Ouvre le fichier sélectionné dans l'application par défaut."""
        selected_index = self.file_list.GetFirstSelected()
        if selected_index != -1:
            file_path = self.file_list.GetItemText(selected_index, 1)  # Récupère le chemin du fichier
            if os.path.exists(file_path):
                try:
                    subprocess.run(["start", "", file_path], shell=True)  # Ouvrir avec l'application par défaut
                except Exception as e:
                    wx.MessageBox(f"Erreur lors de l'ouverture du fichier:\n{e}", "Erreur", wx.OK | wx.ICON_ERROR)
            else:
                wx.MessageBox("Le fichier n'existe plus.", "Erreur", wx.OK | wx.ICON_WARNING)

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainWindow(None)
    frame.Show()
    app.MainLoop()
