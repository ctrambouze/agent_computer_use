"""
Mission TikTok - Script optimise
Capture le lien d'une video TikTok via OCR

CE QUI MARCHE:
- OCR sur zone TikTok uniquement (crop 0-480) pour trouver "Copier le lien"
- Clic droit au centre de la video
- Extraction du lien via clipboard

CE QUI NE MARCHE PAS (retire):
- OCR pour les petits chiffres (likes, comments) - trop petit
- VLM pour les coordonnees - invente les positions
- OCR full screen - se melange avec le texte des autres fenetres
"""

import subprocess
import time
import os
import pyautogui
import pyperclip
from PIL import ImageGrab
import easyocr

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.1

# Reader OCR (singleton)
_reader = None

def get_reader():
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(['fr', 'en'], gpu=True)
    return _reader


def ouvrir_tiktok_gauche():
    """Ouvre TikTok dans Chrome et ancre a GAUCHE"""
    print("[1] Ouverture TikTok...")
    subprocess.Popen(['cmd', '/c', 'start', 'chrome', 'https://www.tiktok.com'], shell=True)
    time.sleep(4)

    print("[2] Ancrage a gauche...")
    from chrome_utils import focus_chrome
    focus_chrome()
    time.sleep(0.5)
    pyautogui.hotkey('win', 'left')
    time.sleep(0.5)
    pyautogui.press('escape')

    print("[3] Attente chargement...")
    time.sleep(5)


def copier_lien_video(video_x=240, video_y=300):
    """
    Copie le lien de la video TikTok actuellement affichee

    Args:
        video_x, video_y: Centre de la video (TikTok a gauche = ~240, 300)

    Returns:
        Le lien ou None
    """
    # Vider clipboard
    pyperclip.copy('')

    # Clic droit sur video
    print(f"Clic droit sur ({video_x}, {video_y})...")
    pyautogui.click(video_x, video_y)
    time.sleep(0.3)
    pyautogui.rightClick(video_x, video_y)
    time.sleep(1.0)

    # Capture SEULEMENT la zone TikTok (gauche de l'ecran)
    screenshot = ImageGrab.grab()
    tiktok_zone = screenshot.crop((0, 0, 480, 600))
    tiktok_zone.save('_temp_menu.png')

    # OCR pour trouver "Copier le lien"
    reader = get_reader()
    results = reader.readtext('_temp_menu.png')

    for (bbox, text, conf) in results:
        if 'copier' in text.lower() and 'lien' in text.lower():
            x1, y1 = bbox[0]
            x2, y2 = bbox[2]
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            print(f"'Copier le lien' trouve a ({cx}, {cy})")

            # Clic
            pyautogui.moveTo(cx, cy, duration=0.2)
            time.sleep(0.2)
            pyautogui.click()
            time.sleep(0.5)

            # Recuperer lien
            lien = pyperclip.paste()

            if 'tiktok.com' in lien:
                return lien
            else:
                print("Clipboard ne contient pas de lien TikTok")
                return None

    print("'Copier le lien' non trouve")
    pyautogui.press('escape')
    return None


def sauvegarder_sur_bureau(contenu, nom_fichier="tiktok_video.txt"):
    """Sauvegarde le contenu sur le Bureau"""
    desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    filepath = os.path.join(desktop, nom_fichier)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"Fichier sauvegarde: {filepath}")
    return filepath


def mission_tiktok(compte="", likes="", comments="", partages="", contenu=""):
    """
    Mission complete: ouvre TikTok, copie le lien, sauvegarde sur le Bureau

    Args:
        compte, likes, comments, partages, contenu: Infos manuelles (OCR trop petit)
    """
    print("=" * 50)
    print("MISSION TIKTOK")
    print("=" * 50)

    # Copier le lien
    lien = copier_lien_video()

    if not lien:
        print("ECHEC: impossible de copier le lien")
        return None

    print(f"Lien: {lien}")

    # Extraire le compte du lien si pas fourni
    if not compte and '/@' in lien:
        compte = lien.split('/@')[1].split('/')[0]

    # Creer le rapport
    rapport = f"""=== TikTok Video Analysis ===

Compte: {compte}
Contenu: {contenu}

Stats:
- Likes: {likes}
- Commentaires: {comments}
- Partages: {partages}

Lien: {lien}

Date: {time.strftime('%Y-%m-%d %H:%M')}
"""

    # Sauvegarder
    nom = f"tiktok_{compte.replace('.', '_')}.txt" if compte else "tiktok_video.txt"
    filepath = sauvegarder_sur_bureau(rapport, nom)

    print("\nMISSION TERMINEE!")
    return filepath


if __name__ == "__main__":
    import sys

    # Options
    if "--open" in sys.argv:
        ouvrir_tiktok_gauche()

    # Lancer la mission
    # Les stats sont en parametre car l'OCR ne les lit pas bien (trop petit)
    mission_tiktok(
        likes=sys.argv[sys.argv.index("--likes")+1] if "--likes" in sys.argv else "",
        comments=sys.argv[sys.argv.index("--comments")+1] if "--comments" in sys.argv else "",
        partages=sys.argv[sys.argv.index("--partages")+1] if "--partages" in sys.argv else "",
        contenu=" ".join(sys.argv[sys.argv.index("--contenu")+1:]) if "--contenu" in sys.argv else ""
    )
