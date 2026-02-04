"""
Fonctions utilitaires pour controler Chrome
"""

import subprocess
import time
import pyautogui

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.2


def is_chrome_running():
    """Verifie si Chrome est en cours d'execution"""
    result = subprocess.run(
        ['tasklist', '/FI', 'IMAGENAME eq chrome.exe'],
        capture_output=True, text=True
    )
    return 'chrome.exe' in result.stdout


def launch_chrome():
    """Lance Chrome s'il n'est pas deja ouvert"""
    if not is_chrome_running():
        subprocess.Popen(['start', 'chrome'], shell=True)
        time.sleep(3)
        return True
    return False


def focus_chrome():
    """Met Chrome au premier plan"""
    if not is_chrome_running():
        launch_chrome()
        return True

    # Activer Chrome via PowerShell
    ps_cmd = '''
    Add-Type -AssemblyName Microsoft.VisualBasic
    $chrome = Get-Process chrome -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($chrome) {
        [Microsoft.VisualBasic.Interaction]::AppActivate($chrome.Id)
    }
    '''
    subprocess.run(['powershell', '-Command', ps_cmd], capture_output=True)
    time.sleep(0.3)
    return True


def ouvrir_onglet():
    """Ouvre un nouvel onglet Chrome"""
    focus_chrome()
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 't')
    time.sleep(0.5)
    return True


def fermer_onglet():
    """Ferme l'onglet Chrome actuel"""
    focus_chrome()
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'w')
    time.sleep(0.5)
    return True


def ouvrir_url(url):
    """Ouvre une URL dans Chrome"""
    focus_chrome()
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'l')  # Selectionner barre d'adresse
    time.sleep(0.2)

    # Utiliser clipboard pour les caracteres speciaux
    import pyperclip
    pyperclip.copy(url)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)
    pyautogui.press('enter')
    time.sleep(1)
    return True


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python chrome_utils.py ouvrir    - ouvre un onglet")
        print("  python chrome_utils.py fermer    - ferme l'onglet actuel")
        print("  python chrome_utils.py url <url> - ouvre une URL")
        print("  python chrome_utils.py test      - test ouvrir/fermer")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "ouvrir":
        ouvrir_onglet()
        print("Onglet ouvert")
    elif cmd == "fermer":
        fermer_onglet()
        print("Onglet ferme")
    elif cmd == "url" and len(sys.argv) > 2:
        ouvrir_url(sys.argv[2])
        print(f"URL ouverte: {sys.argv[2]}")
    elif cmd == "test":
        print("Test ouvrir/fermer onglet Chrome...")
        print("1. Ouverture onglet...")
        ouvrir_onglet()
        time.sleep(1)
        print("2. Fermeture onglet...")
        fermer_onglet()
        print("SUCCES!")
    else:
        print(f"Commande inconnue: {cmd}")
