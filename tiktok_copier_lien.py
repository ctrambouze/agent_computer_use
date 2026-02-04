"""
Script pour copier le lien d'une video TikTok
Utilise EasyOCR pour detecter "Copier le lien" dans le menu contextuel
"""

import subprocess
import time
import pyautogui
import pyperclip
from PIL import ImageGrab

from ocr_utils import find_text_on_screen
from chrome_utils import focus_chrome
from window_utils import fenetre_gauche

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.1

# URL TikTok
TIKTOK_URL = "https://www.tiktok.com"


def ouvrir_tiktok_droite():
    """Ouvre TikTok dans Chrome a droite de l'ecran"""
    print("[1] Ouverture TikTok...")
    subprocess.Popen(['cmd', '/c', 'start', 'chrome', TIKTOK_URL], shell=True)
    time.sleep(4)

    print("[2] Ancrage Chrome a droite...")
    focus_chrome()
    time.sleep(0.5)
    pyautogui.hotkey('win', 'right')
    time.sleep(0.5)
    pyautogui.press('escape')

    print("[3] Attente chargement...")
    time.sleep(5)


def copier_lien_tiktok(video_x=1200, video_y=400, max_essais=10):
    """
    Copie le lien d'une video TikTok via clic droit + OCR

    Args:
        video_x, video_y: Coordonnees du centre de la video
        max_essais: Nombre max de tentatives

    Returns:
        Le lien copie ou None
    """
    print(f"\nClic droit sur video ({video_x}, {video_y})...")

    for essai in range(1, max_essais + 1):
        print(f"\n--- Essai {essai}/{max_essais} ---")

        # Clic droit pour ouvrir le menu
        pyautogui.click(video_x, video_y)
        time.sleep(0.3)
        pyautogui.rightClick(video_x, video_y)
        time.sleep(1)

        # Chercher "Copier le lien" avec OCR
        print("Recherche 'Copier le lien' (OCR)...")
        result = find_text_on_screen("Copier le lien")

        if result:
            print(f"Trouve a ({result['x']}, {result['y']}) conf={result['confidence']:.2f}")

            # Deplacer et cliquer
            pyautogui.moveTo(result['x'], result['y'], duration=0.2)
            time.sleep(0.3)
            pyautogui.click()
            time.sleep(0.5)

            # Verifier le clipboard
            lien = pyperclip.paste()
            print(f"Clipboard: {lien}")

            if lien and "tiktok.com" in lien:
                # Verifier que c'est un vrai lien video
                if lien in ["https://www.tiktok.com", "https://www.tiktok.com/"]:
                    print("ECHEC: URL de base")
                    continue

                if "foryou" in lien.lower():
                    print("ECHEC: contient 'foryou'")
                    continue

                # SUCCES!
                print(f"\nSUCCES! Lien: {lien}")
                return lien
            else:
                print("ECHEC: pas de lien TikTok dans clipboard")
        else:
            print("'Copier le lien' non trouve")
            pyautogui.press('escape')
            time.sleep(0.5)

    print(f"\nECHEC apres {max_essais} essais")
    return None


def main():
    """Point d'entree principal"""
    import sys

    print("=" * 50)
    print("  TikTok Link Copier (OCR)")
    print("=" * 50)

    # Option: ouvrir TikTok automatiquement
    if "--open" in sys.argv:
        ouvrir_tiktok_droite()

    # Coordonnees video (par defaut: TikTok a droite de l'ecran)
    video_x = 1200
    video_y = 400

    # Lire coords depuis args si fournis
    for arg in sys.argv[1:]:
        if arg.startswith("--x="):
            video_x = int(arg.split("=")[1])
        elif arg.startswith("--y="):
            video_y = int(arg.split("=")[1])

    print(f"\nCoordonnees video: ({video_x}, {video_y})")
    print("Demarrage dans 3 secondes...")
    time.sleep(3)

    lien = copier_lien_tiktok(video_x, video_y)

    if lien:
        # Sauvegarder
        with open("tiktok_url.txt", "w") as f:
            f.write(lien)
        print(f"\nLien sauvegarde dans tiktok_url.txt")
        print(f"Lien: {lien}")
    else:
        print("\nAucun lien copie")


if __name__ == "__main__":
    main()
