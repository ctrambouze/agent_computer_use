"""
Fonctions utilitaires pour controler Notepad
"""

import subprocess
import time
import pyautogui
import pyperclip

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.2


def is_notepad_running():
    """Verifie si Notepad est en cours d'execution"""
    result = subprocess.run(
        ['tasklist', '/FI', 'IMAGENAME eq notepad.exe'],
        capture_output=True, text=True
    )
    return 'notepad.exe' in result.stdout


def ouvrir_notepad():
    """Ouvre Notepad"""
    subprocess.Popen(['notepad.exe'])
    time.sleep(1)
    return True


def focus_notepad():
    """Met Notepad au premier plan"""
    if not is_notepad_running():
        ouvrir_notepad()
        return True

    ps_cmd = '''
    Add-Type -AssemblyName Microsoft.VisualBasic
    $notepad = Get-Process notepad -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($notepad) {
        [Microsoft.VisualBasic.Interaction]::AppActivate($notepad.Id)
    }
    '''
    subprocess.run(['powershell', '-Command', ps_cmd], capture_output=True)
    time.sleep(0.3)
    return True


def ecrire_texte(texte):
    """Ecrit du texte dans Notepad"""
    focus_notepad()
    time.sleep(0.3)
    pyperclip.copy(texte)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)
    return True


def effacer_tout():
    """Efface tout le contenu"""
    focus_notepad()
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.1)
    pyautogui.press('delete')
    time.sleep(0.2)
    return True


def sauvegarder(chemin=None):
    """Sauvegarde le fichier (Ctrl+S ou Ctrl+Shift+S pour nouveau)"""
    focus_notepad()
    time.sleep(0.3)

    if chemin:
        # Sauvegarder sous
        pyautogui.hotkey('ctrl', 'shift', 's')
        time.sleep(0.5)
        pyperclip.copy(chemin)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.2)
        pyautogui.press('enter')
        time.sleep(0.5)
    else:
        # Sauvegarder
        pyautogui.hotkey('ctrl', 's')
        time.sleep(0.3)
    return True


def fermer_notepad(sauvegarder_avant=False):
    """Ferme Notepad"""
    if not is_notepad_running():
        return True

    focus_notepad()
    time.sleep(0.3)
    pyautogui.hotkey('alt', 'f4')
    time.sleep(0.5)

    # Si dialogue de sauvegarde apparait
    if not sauvegarder_avant:
        # Appuyer sur "Ne pas enregistrer" (Alt+N en francais)
        pyautogui.hotkey('alt', 'n')
        time.sleep(0.3)

    return True


def nouveau_fichier():
    """Cree un nouveau fichier (Ctrl+N)"""
    focus_notepad()
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'n')
    time.sleep(0.5)
    return True


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python notepad_utils.py ouvrir")
        print("  python notepad_utils.py ecrire <texte>")
        print("  python notepad_utils.py effacer")
        print("  python notepad_utils.py sauvegarder [chemin]")
        print("  python notepad_utils.py fermer")
        print("  python notepad_utils.py test")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "ouvrir":
        ouvrir_notepad()
        print("Notepad ouvert")
    elif cmd == "ecrire" and len(sys.argv) > 2:
        ecrire_texte(" ".join(sys.argv[2:]))
        print("Texte ecrit")
    elif cmd == "effacer":
        effacer_tout()
        print("Contenu efface")
    elif cmd == "sauvegarder":
        chemin = sys.argv[2] if len(sys.argv) > 2 else None
        sauvegarder(chemin)
        print("Fichier sauvegarde")
    elif cmd == "fermer":
        fermer_notepad()
        print("Notepad ferme")
    elif cmd == "test":
        print("Test Notepad...")
        print("1. Ouvrir...")
        ouvrir_notepad()
        time.sleep(1)
        print("2. Ecrire...")
        ecrire_texte("Test automatique depuis Python!")
        time.sleep(1)
        print("3. Fermer sans sauvegarder...")
        fermer_notepad(sauvegarder_avant=False)
        print("SUCCES!")
    else:
        print(f"Commande inconnue: {cmd}")
