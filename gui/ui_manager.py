import wx
import threading
import time
from scripts.pptx_analyze_files.pptx_analyze import find_pptx_files
from scripts.pptx_search_content.pptx_search import search_in_pptx
from scripts.gui.progress_dialog import ProgressDialog

class UIManager:
    def __init__(self, main_window):
        """Gère les interactions de l'interface utilisateur."""
        self.main_window = main_window
        self.files_list = []  # Stocke les fichiers trouvés
        self.setup_events()

    def setup_events(self):
        """Associe les événements aux boutons."""
        self.main_window.scan_btn.Bind(wx.EVT_BUTTON, self.on_scan)
        self.main_window.search_btn.Bind(wx.EVT_BUTTON, self.on_search)
    
    def on_scan(self, event):
        """Affiche une boîte de dialogue pour sélectionner un dossier, puis lance l'analyse."""
        print("Bouton 'Analyser' cliqué !")

        with wx.DirDialog(self.main_window, "Sélectionnez un dossier à analyser",
                          style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as dialog:

            if dialog.ShowModal() == wx.ID_CANCEL:
                return  # L'utilisateur a annulé

            selected_dir = dialog.GetPath()
            print(f"Dossier sélectionné : {selected_dir}")

            # Désactiver les boutons pendant l'analyse
            self.main_window.scan_btn.Disable()
            self.main_window.search_btn.Disable()
            self.main_window.file_list.DeleteAllItems()

            thread = threading.Thread(target=self.run_scan, args=(selected_dir,))
            thread.start()

    def run_scan(self, directory):
        """Exécute l'analyse et met à jour l'interface."""
        wx.CallAfter(self.show_progress_dialog)

        self.files_list = find_pptx_files([directory], max_files=500)
        wx.CallAfter(self.update_ui, self.files_list)

        wx.CallAfter(self.progress_dialog.Destroy)

    def on_search(self, event):
        """Recherche un mot-clé dans les fichiers .pptx analysés."""
        keyword = self.main_window.search_input.GetValue().strip()
        if not keyword:
            wx.MessageBox("Veuillez entrer un mot-clé.", "Erreur", wx.OK | wx.ICON_WARNING)
            return

        print(f"Recherche du mot-clé : {keyword}")

        self.main_window.file_list.DeleteAllItems()  # Effacer les anciens résultats
        thread = threading.Thread(target=self.run_search, args=(keyword,))
        thread.start()

    def run_search(self, keyword):
        """Recherche le mot-clé et met à jour l'interface."""
        wx.CallAfter(self.show_progress_dialog)

        matching_files = search_in_pptx(self.files_list, keyword)
        wx.CallAfter(self.update_ui, matching_files)

        wx.CallAfter(self.progress_dialog.Destroy)

    def show_progress_dialog(self):
        """Affiche la fenêtre de progression."""
        self.progress_dialog = ProgressDialog(self.main_window)
        self.progress_dialog.ShowModal()

    def update_ui(self, pptx_files):
        """Affiche les fichiers dans la liste."""
        self.main_window.file_list.DeleteAllItems()  # Efface les anciens résultats
    
        for idx, (filename, filepath, date_modif, file_size) in enumerate(pptx_files):
            self.main_window.file_list.InsertItem(idx, filename)
            self.main_window.file_list.SetItem(idx, 1, filepath)
            self.main_window.file_list.SetItem(idx, 2, date_modif)
            self.main_window.file_list.SetItem(idx, 3, file_size)  # Affichage de la taille
    
        self.main_window.scan_btn.Enable()
        if pptx_files:
            self.main_window.search_btn.Enable()

