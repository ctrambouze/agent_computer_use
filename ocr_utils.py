"""
Fonctions utilitaires OCR pour detection de texte avec coordonnees
Utilise EasyOCR pour trouver des elements textuels a l'ecran
"""

import time
from PIL import ImageGrab
import easyocr

# Initialiser le reader une seule fois (cache)
_reader = None


def get_reader():
    """Retourne le reader EasyOCR (initialise une seule fois)"""
    global _reader
    if _reader is None:
        print("Initialisation EasyOCR (premiere fois)...")
        _reader = easyocr.Reader(['fr', 'en'], gpu=True)
    return _reader


def capture_screen():
    """Capture l'ecran complet"""
    return ImageGrab.grab()


def find_text_on_screen(search_text, screenshot=None, case_sensitive=False):
    """
    Trouve un texte a l'ecran et retourne ses coordonnees

    Args:
        search_text: Texte a chercher
        screenshot: Image PIL (capture l'ecran si None)
        case_sensitive: Sensible a la casse

    Returns:
        dict avec {x, y, confidence, text} ou None si pas trouve
    """
    if screenshot is None:
        screenshot = capture_screen()

    # Sauvegarder temporairement pour OCR
    temp_path = "temp_ocr.png"
    screenshot.save(temp_path)

    reader = get_reader()
    results = reader.readtext(temp_path)

    search_lower = search_text.lower() if not case_sensitive else search_text

    for (bbox, text, conf) in results:
        text_compare = text.lower() if not case_sensitive else text

        # Chercher le texte (peut etre partiel)
        if search_lower in text_compare:
            # bbox = [[x1,y1], [x2,y1], [x2,y2], [x1,y2]]
            x1, y1 = bbox[0]
            x2, y2 = bbox[2]
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            return {
                'x': center_x,
                'y': center_y,
                'confidence': conf,
                'text': text,
                'bbox': bbox
            }

    return None


def find_all_text_on_screen(screenshot=None, min_confidence=0.3):
    """
    Trouve tous les textes a l'ecran

    Returns:
        Liste de dicts {x, y, confidence, text, bbox}
    """
    if screenshot is None:
        screenshot = capture_screen()

    temp_path = "temp_ocr.png"
    screenshot.save(temp_path)

    reader = get_reader()
    results = reader.readtext(temp_path)

    texts = []
    for (bbox, text, conf) in results:
        if conf >= min_confidence:
            x1, y1 = bbox[0]
            x2, y2 = bbox[2]
            texts.append({
                'x': int((x1 + x2) / 2),
                'y': int((y1 + y2) / 2),
                'confidence': conf,
                'text': text,
                'bbox': bbox
            })

    return texts


def click_on_text(search_text, case_sensitive=False):
    """
    Trouve un texte et clique dessus

    Returns:
        True si clique effectue, False sinon
    """
    import pyautogui
    pyautogui.FAILSAFE = False

    result = find_text_on_screen(search_text, case_sensitive=case_sensitive)

    if result:
        print(f"Texte trouve: '{result['text']}' a ({result['x']}, {result['y']})")
        pyautogui.click(result['x'], result['y'])
        return True
    else:
        print(f"Texte '{search_text}' non trouve")
        return False


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python ocr_utils.py find <texte>  - trouve un texte")
        print("  python ocr_utils.py click <texte> - trouve et clique")
        print("  python ocr_utils.py all           - liste tous les textes")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "find" and len(sys.argv) > 2:
        search = " ".join(sys.argv[2:])
        print(f"Recherche: '{search}'")
        result = find_text_on_screen(search)
        if result:
            print(f"TROUVE: '{result['text']}' a ({result['x']}, {result['y']}) conf={result['confidence']:.2f}")
        else:
            print("Non trouve")

    elif cmd == "click" and len(sys.argv) > 2:
        search = " ".join(sys.argv[2:])
        print(f"Recherche et clic: '{search}'")
        success = click_on_text(search)
        print("OK" if success else "ECHEC")

    elif cmd == "all":
        print("Scan de l'ecran...")
        texts = find_all_text_on_screen()
        print(f"\n{len(texts)} textes trouves:")
        for t in texts:
            print(f"  '{t['text']}' -> ({t['x']}, {t['y']})")
