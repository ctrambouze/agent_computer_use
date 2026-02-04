"""
Fonctions utilitaires pour controler l'Explorateur Windows
"""

import subprocess
import time
import os
import pyautogui
import pyperclip

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.2


def ouvrir_explorateur(chemin=None):
    """Ouvre l'Explorateur Windows, optionnellement a un chemin specifique"""
    if chemin:
        chemin = os.path.abspath(chemin)
        subprocess.Popen(['explorer', chemin])
    else:
        subprocess.Popen(['explorer'])
    time.sleep(1)
    return True


def ouvrir_dossier(chemin):
    """Ouvre un dossier specifique"""
    return ouvrir_explorateur(chemin)


def focus_explorateur():
    """Met l'Explorateur au premier plan"""
    ps_cmd = '''
    Add-Type -AssemblyName Microsoft.VisualBasic
    $explorer = Get-Process explorer -ErrorAction SilentlyContinue | Where-Object {$_.MainWindowTitle -ne ""} | Select-Object -First 1
    if ($explorer) {
        [Microsoft.VisualBasic.Interaction]::AppActivate($explorer.Id)
    }
    '''
    subprocess.run(['powershell', '-Command', ps_cmd], capture_output=True)
    time.sleep(0.3)
    return True


def naviguer_vers(chemin):
    """Navigue vers un chemin dans l'explorateur ouvert"""
    focus_explorateur()
    time.sleep(0.3)

    # Ctrl+L pour selectionner la barre d'adresse
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(0.3)

    # Taper le chemin
    pyperclip.copy(os.path.abspath(chemin))
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)
    pyautogui.press('enter')
    time.sleep(1)
    return True


def remonter_dossier():
    """Remonte au dossier parent (Alt+Up)"""
    focus_explorateur()
    time.sleep(0.3)
    pyautogui.hotkey('alt', 'up')
    time.sleep(0.5)
    return True


def retour():
    """Retour arriere (Alt+Left)"""
    focus_explorateur()
    time.sleep(0.3)
    pyautogui.hotkey('alt', 'left')
    time.sleep(0.5)
    return True


def avant():
    """Avancer (Alt+Right)"""
    focus_explorateur()
    time.sleep(0.3)
    pyautogui.hotkey('alt', 'right')
    time.sleep(0.5)
    return True


def actualiser():
    """Actualiser (F5)"""
    focus_explorateur()
    time.sleep(0.3)
    pyautogui.press('f5')
    time.sleep(0.5)
    return True


def nouveau_dossier():
    """Cree un nouveau dossier (Ctrl+Shift+N)"""
    focus_explorateur()
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'shift', 'n')
    time.sleep(0.5)
    return True


def rechercher(terme):
    """Lance une recherche (Ctrl+E ou Ctrl+F)"""
    focus_explorateur()
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'e')
    time.sleep(0.3)
    pyperclip.copy(terme)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)
    pyautogui.press('enter')
    time.sleep(1)
    return True


def fermer_explorateur():
    """Ferme la fenetre Explorateur active"""
    focus_explorateur()
    time.sleep(0.3)
    pyautogui.hotkey('alt', 'f4')
    time.sleep(0.5)
    return True


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python explorer_utils.py ouvrir [chemin]")
        print("  python explorer_utils.py naviguer <chemin>")
        print("  python explorer_utils.py remonter")
        print("  python explorer_utils.py rechercher <terme>")
        print("  python explorer_utils.py fermer")
        print("  python explorer_utils.py test")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "ouvrir":
        chemin = sys.argv[2] if len(sys.argv) > 2 else None
        ouvrir_explorateur(chemin)
        print("Explorateur ouvert")
    elif cmd == "naviguer" and len(sys.argv) > 2:
        naviguer_vers(sys.argv[2])
        print(f"Navigation vers {sys.argv[2]}")
    elif cmd == "remonter":
        remonter_dossier()
        print("Remonte au dossier parent")
    elif cmd == "rechercher" and len(sys.argv) > 2:
        rechercher(sys.argv[2])
        print(f"Recherche: {sys.argv[2]}")
    elif cmd == "fermer":
        fermer_explorateur()
        print("Explorateur ferme")
    elif cmd == "test":
        print("Test Explorateur...")
        print("1. Ouvrir Documents...")
        ouvrir_explorateur(os.path.expanduser("~\\Documents"))
        time.sleep(2)
        print("2. Remonter au parent...")
        remonter_dossier()
        time.sleep(1)
        print("3. Fermer...")
        fermer_explorateur()
        print("SUCCES!")
    else:
        print(f"Commande inconnue: {cmd}")
