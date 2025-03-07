# 📂 PPTX Analyzer
![pptx-analyzer](https://img.shields.io/badge/version-1.0-blue?style=for-the-badge) 
![Platform](https://img.shields.io/badge/platform-Windows-blue?style=for-the-badge)
![PPTX Analyzer](https://img.shields.io/badge/Python-3.9-blue?style=for-the-badge&logo=python)
![wxPython](https://img.shields.io/badge/wxPython-UI-red?style=for-the-badge)

## 📌 Présentation

**PPTX Analyzer** est un logiciel puissant permettant de **scanner, analyser et rechercher du texte** dans des fichiers PowerPoint `.pptx`.  
Grâce à son **interface moderne et intuitive**, il offre une navigation fluide et une recherche avancée sur le contenu des fichiers.

---

## ✨ **Fonctionnalités**

✅ **Analyse des fichiers `.pptx`** dans un dossier sélectionné (incluant les sous-dossiers).  
✅ **Affichage des fichiers trouvés** avec leur nom, chemin, **date de modification** et **taille**.  
✅ **Recherche avancée** : possibilité de **rechercher du texte à l'intérieur des fichiers `.pptx`**.  
✅ **Ouverture directe des fichiers** via l'application PowerPoint par défaut.  
✅ **Interface utilisateur moderne** avec un design sombre sous wxPython.  
✅ **Installation facile** grâce à un **setup .exe généré avec Inno Setup**.  

---

## 🚀 **Installation et Exécution**

### **🔹 1. Exécutable Windows (Version compilée)**
Si tu veux juste **utiliser le logiciel sans coder**, télécharge le fichier `PPTX_Analyzer_Setup.exe` et **installe-le**.

### **🔹 2. Exécution depuis le code source**
#### **📌 Prérequis**
- **Windows 10/11**
- **Python 3.9**
- **pip** installé

#### **📌 Installation des dépendances**
Clone le projet et installe les dépendances :
```bash
git clone https://github.com/ton-github/pptx-analyzer.git
cd pptx-analyzer
pip install -r requirements.txt
```
