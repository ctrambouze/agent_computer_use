"""
Fonctions utilitaires pour controler la souris
"""

import time
import pyautogui

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.1


def position():
    """Retourne la position actuelle de la souris"""
    return pyautogui.position()


def deplacer(x, y, duree=0.2):
    """Deplace la souris vers les coordonnees (x, y)"""
    pyautogui.moveTo(x, y, duration=duree)
    return True


def clic(x=None, y=None):
    """Clic gauche aux coordonnees ou a la position actuelle"""
    if x is not None and y is not None:
        pyautogui.click(x, y)
    else:
        pyautogui.click()
    time.sleep(0.1)
    return True


def clic_droit(x=None, y=None):
    """Clic droit aux coordonnees ou a la position actuelle"""
    if x is not None and y is not None:
        pyautogui.rightClick(x, y)
    else:
        pyautogui.rightClick()
    time.sleep(0.1)
    return True


def double_clic(x=None, y=None):
    """Double clic aux coordonnees ou a la position actuelle"""
    if x is not None and y is not None:
        pyautogui.doubleClick(x, y)
    else:
        pyautogui.doubleClick()
    time.sleep(0.1)
    return True


def triple_clic(x=None, y=None):
    """Triple clic (selectionne une ligne entiere)"""
    if x is not None and y is not None:
        pyautogui.tripleClick(x, y)
    else:
        pyautogui.tripleClick()
    time.sleep(0.1)
    return True


def drag(x_debut, y_debut, x_fin, y_fin, duree=0.5):
    """Glisser-deposer de (x_debut, y_debut) vers (x_fin, y_fin)"""
    pyautogui.moveTo(x_debut, y_debut)
    time.sleep(0.1)
    pyautogui.drag(x_fin - x_debut, y_fin - y_debut, duration=duree)
    return True


def drag_relatif(dx, dy, duree=0.5):
    """Glisser-deposer relatif depuis la position actuelle"""
    pyautogui.drag(dx, dy, duration=duree)
    return True


def scroll_haut(clicks=3):
    """Scroll vers le haut"""
    pyautogui.scroll(clicks)
    time.sleep(0.2)
    return True


def scroll_bas(clicks=3):
    """Scroll vers le bas"""
    pyautogui.scroll(-clicks)
    time.sleep(0.2)
    return True


def scroll_horizontal(clicks):
    """Scroll horizontal (positif = droite, negatif = gauche)"""
    pyautogui.hscroll(clicks)
    time.sleep(0.2)
    return True


def maintenir_clic():
    """Maintient le bouton gauche enfonce"""
    pyautogui.mouseDown()
    return True


def relacher_clic():
    """Relache le bouton gauche"""
    pyautogui.mouseUp()
    return True


def clic_maintenu_deplacer(x_debut, y_debut, x_fin, y_fin, duree=0.5):
    """Clic maintenu et deplace (pour selections, etc.)"""
    pyautogui.moveTo(x_debut, y_debut)
    time.sleep(0.1)
    pyautogui.mouseDown()
    pyautogui.moveTo(x_fin, y_fin, duration=duree)
    pyautogui.mouseUp()
    time.sleep(0.1)
    return True


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python mouse_utils.py position")
        print("  python mouse_utils.py deplacer <x> <y>")
        print("  python mouse_utils.py clic [x y]")
        print("  python mouse_utils.py clic_droit [x y]")
        print("  python mouse_utils.py double_clic [x y]")
        print("  python mouse_utils.py drag <x1> <y1> <x2> <y2>")
        print("  python mouse_utils.py scroll_haut/scroll_bas [clicks]")
        print("  python mouse_utils.py test")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "position":
        x, y = position()
        print(f"Position: ({x}, {y})")
    elif cmd == "deplacer" and len(sys.argv) >= 4:
        deplacer(int(sys.argv[2]), int(sys.argv[3]))
        print(f"Deplace vers ({sys.argv[2]}, {sys.argv[3]})")
    elif cmd == "clic":
        if len(sys.argv) >= 4:
            clic(int(sys.argv[2]), int(sys.argv[3]))
        else:
            clic()
        print("Clic effectue")
    elif cmd == "clic_droit":
        if len(sys.argv) >= 4:
            clic_droit(int(sys.argv[2]), int(sys.argv[3]))
        else:
            clic_droit()
        print("Clic droit effectue")
    elif cmd == "double_clic":
        if len(sys.argv) >= 4:
            double_clic(int(sys.argv[2]), int(sys.argv[3]))
        else:
            double_clic()
        print("Double clic effectue")
    elif cmd == "drag" and len(sys.argv) >= 6:
        drag(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
        print("Drag effectue")
    elif cmd == "scroll_haut":
        clicks = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        scroll_haut(clicks)
        print(f"Scroll haut {clicks}")
    elif cmd == "scroll_bas":
        clicks = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        scroll_bas(clicks)
        print(f"Scroll bas {clicks}")
    elif cmd == "test":
        print("Test Mouse Utils...")
        print("1. Position actuelle...")
        x, y = position()
        print(f"   Position: ({x}, {y})")
        print("2. Deplacer au centre ecran...")
        deplacer(960, 540)
        time.sleep(0.5)
        print("3. Scroll bas...")
        scroll_bas(2)
        time.sleep(0.5)
        print("4. Scroll haut...")
        scroll_haut(2)
        time.sleep(0.5)
        print("5. Retour position initiale...")
        deplacer(x, y)
        print("SUCCES!")
    else:
        print(f"Commande inconnue: {cmd}")
