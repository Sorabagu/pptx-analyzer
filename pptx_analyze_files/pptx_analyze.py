import os
import datetime

EXCLUDED_FOLDERS = ["C:\\Program Files", "C:\\Program Files (x86)"]

def find_pptx_files(start_dirs, max_files=500):
    """
    Recherche récursive de fichiers .pptx dans les dossiers sélectionnés.

    :param start_dirs: Liste des répertoires à analyser.
    :param max_files: Nombre maximal de fichiers à récupérer.
    :return: Liste des fichiers trouvés [(nom_fichier, chemin_complet, date_modif, taille)].
    """
    pptx_files = []
    
    def scan_directory(directory):
        """Parcourt récursivement un dossier et récupère les fichiers .pptx."""
        try:
            with os.scandir(directory) as entries:
                for entry in entries:
                    # Ignorer les dossiers système
                    if entry.is_dir(follow_symlinks=False):
                        if any(entry.path.startswith(excluded) for excluded in EXCLUDED_FOLDERS):
                            continue
                        scan_directory(entry.path)  # Récursion pour les sous-dossiers
                    elif entry.is_file() and entry.name.lower().endswith(".pptx"):
                        mod_time = entry.stat().st_mtime
                        date_modif = datetime.datetime.fromtimestamp(mod_time).strftime('%d/%m/%Y - %H:%M')
                        
                        # Récupération du poids du fichier en Mo (2 décimales)
                        file_size_mb = round(entry.stat().st_size / (1024 * 1024), 2)

                        pptx_files.append((entry.name, entry.path, date_modif, f"{file_size_mb} Mo"))
                        
                        # Stopper l'analyse si on atteint la limite
                        if len(pptx_files) >= max_files:
                            return

        except PermissionError:
            pass  # Ignorer les dossiers non accessibles

    for root_dir in start_dirs:
        scan_directory(root_dir)  # Démarrer l'analyse récursive

    return pptx_files
