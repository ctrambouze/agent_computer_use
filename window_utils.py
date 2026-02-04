"""
Fonctions utilitaires pour controler les fenetres Windows
"""

import subprocess
import time
import pyautogui

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.2


def lister_fenetres():
    """Liste toutes les fenetres ouvertes avec titre"""
    ps_cmd = '''
    Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | Select-Object ProcessName, MainWindowTitle | Format-Table -AutoSize
    '''
    result = subprocess.run(['powershell', '-Command', ps_cmd], capture_output=True, text=True)
    return result.stdout


def focus_fenetre(nom_process=None, titre=None):
    """Met une fenetre au premier plan par nom de process ou titre"""
    if nom_process:
        ps_cmd = f'''
        Add-Type -AssemblyName Microsoft.VisualBasic
        $proc = Get-Process -Name "{nom_process}" -ErrorAction SilentlyContinue | Where-Object {{$_.MainWindowTitle -ne ""}} | Select-Object -First 1
        if ($proc) {{
            [Microsoft.VisualBasic.Interaction]::AppActivate($proc.Id)
        }}
        '''
    elif titre:
        ps_cmd = f'''
        Add-Type -AssemblyName Microsoft.VisualBasic
        $proc = Get-Process | Where-Object {{$_.MainWindowTitle -like "*{titre}*"}} | Select-Object -First 1
        if ($proc) {{
            [Microsoft.VisualBasic.Interaction]::AppActivate($proc.Id)
        }}
        '''
    else:
        return False

    subprocess.run(['powershell', '-Command', ps_cmd], capture_output=True)
    time.sleep(0.3)
    return True


def minimiser_fenetre():
    """Minimise la fenetre active (Win+Down)"""
    pyautogui.hotkey('win', 'down')
    time.sleep(0.3)
    return True


def maximiser_fenetre():
    """Maximise la fenetre active (Win+Up)"""
    pyautogui.hotkey('win', 'up')
    time.sleep(0.3)
    return True


def restaurer_fenetre():
    """Restaure la fenetre active a sa taille normale"""
    # Si maximisee, Win+Down restaure
    pyautogui.hotkey('win', 'down')
    time.sleep(0.3)
    return True


def fermer_fenetre():
    """Ferme la fenetre active (Alt+F4)"""
    pyautogui.hotkey('alt', 'f4')
    time.sleep(0.5)
    return True


def minimiser_tout():
    """Minimise toutes les fenetres (Win+D)"""
    pyautogui.hotkey('win', 'd')
    time.sleep(0.5)
    return True


def basculer_fenetre():
    """Bascule entre les fenetres (Alt+Tab)"""
    pyautogui.hotkey('alt', 'tab')
    time.sleep(0.3)
    return True


def fenetre_gauche():
    """Ancre la fenetre a gauche (Win+Left)"""
    pyautogui.hotkey('win', 'left')
    time.sleep(0.3)
    return True


def fenetre_droite():
    """Ancre la fenetre a droite (Win+Right)"""
    pyautogui.hotkey('win', 'right')
    time.sleep(0.3)
    return True


def fermer_application(nom_process):
    """Force la fermeture d'une application par nom de process"""
    subprocess.run(['taskkill', '/IM', f'{nom_process}.exe', '/F'], capture_output=True)
    time.sleep(0.5)
    return True


def ouvrir_gestionnaire_taches():
    """Ouvre le Gestionnaire de taches (Ctrl+Shift+Esc)"""
    pyautogui.hotkey('ctrl', 'shift', 'escape')
    time.sleep(1)
    return True


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python window_utils.py lister")
        print("  python window_utils.py focus <process|titre>")
        print("  python window_utils.py minimiser")
        print("  python window_utils.py maximiser")
        print("  python window_utils.py fermer")
        print("  python window_utils.py minimiser_tout")
        print("  python window_utils.py basculer")
        print("  python window_utils.py gauche/droite")
        print("  python window_utils.py kill <process>")
        print("  python window_utils.py test")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "lister":
        print(lister_fenetres())
    elif cmd == "focus" and len(sys.argv) > 2:
        focus_fenetre(nom_process=sys.argv[2])
        print(f"Focus sur {sys.argv[2]}")
    elif cmd == "minimiser":
        minimiser_fenetre()
        print("Fenetre minimisee")
    elif cmd == "maximiser":
        maximiser_fenetre()
        print("Fenetre maximisee")
    elif cmd == "fermer":
        fermer_fenetre()
        print("Fenetre fermee")
    elif cmd == "minimiser_tout":
        minimiser_tout()
        print("Toutes fenetres minimisees")
    elif cmd == "basculer":
        basculer_fenetre()
        print("Bascule Alt+Tab")
    elif cmd == "gauche":
        fenetre_gauche()
        print("Fenetre ancree a gauche")
    elif cmd == "droite":
        fenetre_droite()
        print("Fenetre ancree a droite")
    elif cmd == "kill" and len(sys.argv) > 2:
        fermer_application(sys.argv[2])
        print(f"Application {sys.argv[2]} fermee")
    elif cmd == "test":
        print("Test Window Utils...")
        print("1. Ouvrir Notepad...")
        subprocess.Popen(['notepad.exe'])
        time.sleep(1)
        print("2. Maximiser...")
        maximiser_fenetre()
        time.sleep(1)
        print("3. Ancrer a gauche...")
        fenetre_gauche()
        time.sleep(1)
        print("4. Fermer...")
        fermer_fenetre()
        time.sleep(0.5)
        # Au cas ou dialogue sauvegarde
        pyautogui.hotkey('alt', 'n')
        print("SUCCES!")
    else:
        print(f"Commande inconnue: {cmd}")
