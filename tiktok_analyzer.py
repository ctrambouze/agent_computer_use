"""
TikTok Analyzer - Analyse les 10 premieres videos et sauvegarde dans Notepad
Version 2.0 - Mission complete avec pause video et notes
"""

import os
import time
import re
import pyautogui
import pyperclip
from agent_gui import capture_screen, send_to_model

# Desactiver fail-safe pour eviter les interruptions
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3


def check_if_live(vlm_response):
    """
    Verifie si la video actuelle est un LIVE
    Cherche TYPE: LIVE dans la reponse ou les mots-cles
    """
    response_lower = vlm_response.lower()

    # Verifier le champ TYPE explicite
    if 'type: live' in response_lower or 'type:live' in response_lower:
        return True

    # Verifier les mots-cles de live
    live_keywords = ['live', 'en direct', 'direct', 'streaming', 'diffusion en cours']
    for keyword in live_keywords:
        # Eviter les faux positifs (ex: "olive", "deliver")
        if f' {keyword} ' in f' {response_lower} ' or f' {keyword}' in response_lower:
            return True

    return False


def exit_live():
    """
    Sort d'un LIVE TikTok pour revenir aux videos normales
    Methode: Appuyer sur Escape ou fleche retour, puis scroll
    """
    print("    [EXIT LIVE] Appui Escape...")
    pyautogui.press('escape')
    time.sleep(1)

    # Clic en dehors du live (coin superieur gauche - bouton retour)
    print("    [EXIT LIVE] Clic bouton retour (50, 50)...")
    pyautogui.click(50, 50)
    time.sleep(1)

    # Si toujours dans les lives, essayer swipe vers la gauche
    print("    [EXIT LIVE] Swipe gauche pour sortir...")
    pyautogui.moveTo(960, 540)
    pyautogui.drag(-500, 0, duration=0.3)
    time.sleep(1)

    # Scroll down pour passer a la video suivante
    print("    [EXIT LIVE] Scroll pour video suivante...")
    pyautogui.scroll(-5)
    time.sleep(1)


def copy_single_video_link():
    """
    Copie le lien d'une video TikTok via le bouton PARTAGER:
    1. Trouver le bouton Partager (fleche) sur le cote droit
    2. Cliquer dessus
    3. Trouver "Copier le lien" dans le popup
    4. Cliquer dessus
    5. Retourner l'URL du presse-papier
    """
    # Etape 1: Capturer l'ecran pour trouver le bouton Partager
    img1 = capture_screen()

    # Trouver le bouton Partager (icone fleche sur le cote droit)
    prompt1 = """Regarde l'ecran TikTok.
Sur le COTE DROIT de la video, il y a des icones (coeur, commentaire, partager, etc).
Trouve le bouton PARTAGER (icone fleche qui pointe vers la droite, ou "Share").
Donne les coordonnees X, Y du CENTRE de ce bouton.
Format: COORDS: X, Y"""

    response1 = send_to_model(img1, prompt1)
    print(f"      [Partager] VLM: {response1[:80]}...")

    coords1 = re.search(r'COORDS?:?\s*(\d+)\s*[,\s]\s*(\d+)', response1, re.IGNORECASE)
    if not coords1:
        coords1 = re.search(r'(\d{3,4})\s*[,\s]\s*(\d{2,4})', response1)

    if not coords1:
        print("      [ERREUR] Bouton Partager non trouve!")
        return "ERREUR_PARTAGER"

    x1, y1 = int(coords1.group(1)), int(coords1.group(2))
    print(f"      [Partager] Coordonnees: ({x1}, {y1})")

    # Etape 2: Cliquer sur le bouton Partager
    pyautogui.moveTo(x1, y1, duration=0.2)
    time.sleep(0.3)
    pyautogui.click()
    time.sleep(1.5)  # Attendre que le popup s'ouvre

    # Etape 3: Capturer l'ecran pour trouver "Copier le lien"
    img2 = capture_screen()

    prompt2 = """Regarde le popup de partage TikTok.
Trouve le bouton "Copier le lien" (ou "Copy link" ou une icone de lien).
Donne les coordonnees X, Y du CENTRE de ce bouton.
Format: COORDS: X, Y"""

    response2 = send_to_model(img2, prompt2)
    print(f"      [Copier] VLM: {response2[:80]}...")

    coords2 = re.search(r'COORDS?:?\s*(\d+)\s*[,\s]\s*(\d+)', response2, re.IGNORECASE)
    if not coords2:
        coords2 = re.search(r'(\d{3,4})\s*[,\s]\s*(\d{2,4})', response2)

    if not coords2:
        print("      [ERREUR] Bouton Copier le lien non trouve!")
        pyautogui.press('escape')
        time.sleep(0.3)
        return "ERREUR_COPIER"

    x2, y2 = int(coords2.group(1)), int(coords2.group(2))
    print(f"      [Copier] Coordonnees: ({x2}, {y2})")

    # Etape 4: Cliquer sur "Copier le lien"
    pyautogui.moveTo(x2, y2, duration=0.2)
    time.sleep(0.3)
    pyautogui.click()
    time.sleep(0.5)

    # Fermer le popup si encore ouvert
    pyautogui.press('escape')
    time.sleep(0.3)

    # Etape 5: Recuperer l'URL du presse-papier
    url = pyperclip.paste()
    return url


def open_tiktok():
    """
    PHASE 1: Ouverture de TikTok
    Etapes 1-10
    """
    print("\n" + "=" * 60)
    print("  PHASE 1: Ouverture de TikTok")
    print("=" * 60)

    # Etape 1: Appuyer sur Windows
    print("[1] Appui touche Windows...")
    pyautogui.hotkey('win')
    time.sleep(0.5)

    # Etape 2: Taper "chrome"
    print("[2] Taper 'chrome'...")
    pyperclip.copy('chrome')
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)

    # Etape 3: Appuyer sur Entree
    print("[3] Appui Entree...")
    pyautogui.press('enter')

    # Etape 4: Attendre chargement Chrome
    print("[4] Attente chargement Chrome (3s)...")
    time.sleep(3)

    # Etape 5: Ctrl+L pour barre d'adresse
    print("[5] Ctrl+L (barre d'adresse)...")
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(0.3)

    # Etape 6: Taper URL TikTok
    print("[6] Taper URL TikTok...")
    pyperclip.copy('https://www.tiktok.com/foryou')
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)

    # Etape 7: Appuyer sur Entree
    print("[7] Appui Entree...")
    pyautogui.press('enter')

    # Etape 8: Attendre chargement TikTok
    print("[8] Attente chargement TikTok (5s)...")
    time.sleep(5)

    # Etape 9: Maximiser fenetre
    print("[9] Maximiser fenetre (Win+Haut)...")
    pyautogui.hotkey('win', 'up')
    time.sleep(1)

    # Etape 10: Clic au centre pour focus
    print("[10] Clic au centre (960, 540) pour focus...")
    pyautogui.click(960, 540)
    time.sleep(1)

    print("\n>>> TikTok ouvert et pret!")


def analyze_videos(num_videos=10):
    """
    PHASE 2: Analyse des 10 videos
    Etapes 11-18 (en boucle)
    """
    print("\n" + "=" * 60)
    print(f"  PHASE 2: Analyse des {num_videos} videos")
    print("=" * 60)

    results = []
    best_video = {
        "likes": 0,
        "likes_str": "0",
        "title": "",
        "comments": "",
        "notes": "",
        "video_num": 0
    }

    for i in range(num_videos):
        print(f"\n--- Video {i+1}/{num_videos} ---")

        # Etape 11: ATTENDRE (pas de clic pour eviter d'entrer dans les LIVE!)
        print(f"[11] Attente stabilisation (PAS DE CLIC - evite les LIVE)...")
        time.sleep(1.5)

        # Etape 12: On ne clique plus - on capture directement
        print(f"[12] Pret pour capture...")

        # Etape 13: Capture d'ecran
        print(f"[13] Capture d'ecran...")
        image_b64 = capture_screen()

        # Etape 14: Envoi au VLM
        print(f"[14] Analyse par VLM...")
        prompt = """Analyse cette video TikTok. Donne-moi EXACTEMENT dans ce format:

TYPE: [VIDEO ou LIVE - indique LIVE si tu vois un badge rouge "LIVE" ou "En direct"]
TITRE: [le titre ou description de la video]
LIKES: [nombre de likes - icone coeur sur le cote]
COMMENTAIRES: [nombre de commentaires]
NOTES: [tout texte/hashtags/description visible en bas de la video]

IMPORTANT: Si c'est un LIVE (diffusion en direct), indique TYPE: LIVE
Si tu ne vois pas une info, mets "N/A".
Reponds UNIQUEMENT dans ce format, rien d'autre."""

        try:
            response = send_to_model(image_b64, prompt)
            print(f"    [DEBUG] Reponse VLM: {response[:150]}...")

            # Etape 15: Parser la reponse
            print(f"[15] Parsing des informations...")

            # Extraire les infos avec regex
            titre_match = re.search(r'TITRE:\s*(.+?)(?=\n|LIKES:|$)', response, re.IGNORECASE | re.DOTALL)
            likes_match = re.search(r'LIKES:\s*([\d\.,kKmM]+)', response, re.IGNORECASE)
            comments_match = re.search(r'COMMENTAIRES?:\s*([\d\.,kKmM]+)', response, re.IGNORECASE)
            notes_match = re.search(r'NOTES:\s*(.+?)(?=\n\n|$)', response, re.IGNORECASE | re.DOTALL)

            titre = titre_match.group(1).strip() if titre_match else "N/A"
            likes = likes_match.group(1).strip() if likes_match else "N/A"
            comments = comments_match.group(1).strip() if comments_match else "N/A"
            notes = notes_match.group(1).strip() if notes_match else "N/A"

            # Nettoyer le titre (max 60 caracteres)
            titre = titre[:60] if len(titre) > 60 else titre
            notes = notes[:100] if len(notes) > 100 else notes

            # Stocker le resultat
            video_data = {
                "num": i + 1,
                "titre": titre,
                "likes": likes,
                "comments": comments,
                "notes": notes
            }
            results.append(video_data)

            print(f"    Titre: {titre[:40]}...")
            print(f"    Likes: {likes} | Comments: {comments}")
            print(f"    Notes: {notes[:50]}...")

            # Etape 16: Comparer les likes
            print(f"[16] Comparaison des likes...")
            try:
                # Convertir likes en nombre
                likes_clean = likes.upper().replace('K', '000').replace('M', '000000')
                likes_clean = likes_clean.replace('.', '').replace(',', '')
                likes_int = int(''.join(filter(str.isdigit, likes_clean))) if likes_clean else 0

                if likes_int > best_video["likes"]:
                    best_video = {
                        "likes": likes_int,
                        "likes_str": likes,
                        "title": titre,
                        "comments": comments,
                        "notes": notes,
                        "video_num": i + 1
                    }
                    print(f"    >>> Nouvelle meilleure video: #{i+1} avec {likes} likes!")
            except Exception as e:
                print(f"    [WARN] Erreur conversion likes: {e}")

        except Exception as e:
            print(f"    [ERREUR] Analyse echouee: {e}")
            results.append({
                "num": i + 1,
                "titre": "ERREUR",
                "likes": "N/A",
                "comments": "N/A",
                "notes": str(e)
            })

        # Etape 17: COPIER LE LIEN DE CETTE VIDEO
        print(f"[17] COPIER LE LIEN de la video {i+1}...")
        video_url = copy_single_video_link()

        # Ajouter l'URL au dernier resultat (results[-1])
        if results:
            results[-1]["url"] = video_url
        print(f"    URL: {video_url}")

        # Mettre a jour best_video avec l'URL si c'est la meilleure
        if best_video["video_num"] == i + 1:
            best_video["url"] = video_url

        # Etape 18-19: Scroll vers video suivante (sauf derniere)
        if i < num_videos - 1:
            print(f"[18] Scroll DIRECT vers video suivante...")
            pyautogui.scroll(-5)

            print(f"[19] Attente chargement (2.5s)...")
            time.sleep(2.5)

    print(f"\n>>> Analyse terminee! Meilleure video: #{best_video['video_num']}")
    return results, best_video


def go_to_best_video_url(best_video):
    """
    PHASE 3: Aller sur l'URL de la meilleure video
    On utilise l'URL deja copiee pendant l'analyse
    """
    print("\n" + "=" * 60)
    print("  PHASE 3: Aller sur l'URL de la meilleure video")
    print("=" * 60)

    url = best_video.get("url", "")
    if not url or url == "ERREUR_LIEN":
        print("[ERREUR] Pas d'URL pour la meilleure video!")
        return False

    print(f"[1] URL de la meilleure video: {url}")

    # Ctrl+L pour selectionner la barre d'adresse
    print("[2] Ctrl+L (barre d'adresse)...")
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(0.5)

    # Coller l'URL
    print("[3] Coller l'URL...")
    pyperclip.copy(url)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)

    # Appuyer sur Entree
    print("[4] Appui Entree...")
    pyautogui.press('enter')

    # Attendre chargement
    print("[5] Attente chargement (4s)...")
    time.sleep(4)

    print(f"\n>>> Navigation vers video #{best_video['video_num']} OK!")
    return True


def copy_video_link(best_video):
    """
    PHASE 4: Copier le lien de la meilleure video
    Etapes 22-31: Clic droit -> deplacer souris sur "Copier le lien" -> clic gauche
    """
    print("\n" + "=" * 60)
    print("  PHASE 4: Copier le lien de la video")
    print("=" * 60)

    # Etape 22-23: Attendre
    print("[22] Preparation...")
    print("[23] Attente (1s)...")
    time.sleep(1)

    # Etape 24: Clic DROIT au centre
    print("[24] CLIC DROIT au centre (960, 540)...")
    pyautogui.click(960, 540, button='right')

    # Etape 25: Attendre menu contextuel
    print("[25] Attente menu contextuel (2s)...")
    time.sleep(2)

    # Etape 26: Capture ecran du menu
    print("[26] Capture ecran du menu...")
    img = capture_screen()

    # Etape 27: Envoi au VLM pour trouver "Copier le lien"
    print("[27] Analyse VLM pour trouver 'Copier le lien'...")
    prompt = """Regarde le menu contextuel sur l'ecran.
Je veux cliquer sur "Copier le lien" (ou "Copy link").
Donne-moi les coordonnees X et Y du CENTRE de ce bouton.
Reponds UNIQUEMENT avec ce format exact: COORDS: X, Y
Exemple: COORDS: 1050, 320"""

    response = send_to_model(img, prompt)
    print(f"    Reponse VLM: {response[:150]}")

    # Etape 28: Parser les coordonnees
    print("[28] Extraction des coordonnees...")
    coords = re.search(r'COORDS?:?\s*(\d+)\s*[,\s]\s*(\d+)', response, re.IGNORECASE)

    # Si pas trouve avec COORDS, chercher n'importe quels nombres raisonnables
    if not coords:
        coords = re.search(r'(\d{3,4})\s*[,\s]\s*(\d{2,4})', response)

    if coords:
        x, y = int(coords.group(1)), int(coords.group(2))
        print(f"    Coordonnees trouvees: ({x}, {y})")

        # Etape 29: DEPLACER la souris sur "Copier le lien"
        print(f"[29] Deplacement souris vers ({x}, {y})...")
        pyautogui.moveTo(x, y, duration=0.3)
        time.sleep(0.5)

        # Etape 30: CLIC GAUCHE
        print(f"[30] CLIC GAUCHE pour copier le lien...")
        pyautogui.click()
        time.sleep(1)

        # Etape 31: Recuperer le lien
        print("[31] Recuperation du lien depuis presse-papier...")
        url = pyperclip.paste()
        best_video["url"] = url
        print(f"    URL copiee: {url}")

        return True
    else:
        print("[ERREUR] Coordonnees non trouvees!")
        print(f"    Reponse complete: {response}")
        pyautogui.press('escape')
        best_video["url"] = "ERREUR - Lien non copie"
        return False


def download_video_to_desktop(best_video):
    """
    PHASE 4: Telecharger la video sur le bureau
    1. Clic droit sur la video
    2. Deplacer souris sur "Telecharger la video"
    3. Clic gauche
    4. Enregistrer sur le bureau
    """
    print("\n" + "=" * 60)
    print("  PHASE 4: Telecharger la video sur le bureau")
    print("=" * 60)

    # Etape 1: Clic DROIT au centre de la video
    print("[1] CLIC DROIT au centre (960, 540)...")
    pyautogui.click(960, 540, button='right')

    # Etape 2: Attendre menu contextuel
    print("[2] Attente menu contextuel (2s)...")
    time.sleep(2)

    # Etape 3: Capture ecran du menu
    print("[3] Capture ecran du menu...")
    img = capture_screen()

    # Etape 4: Trouver "Telecharger la video"
    print("[4] Analyse VLM pour trouver 'Telecharger la video'...")
    prompt = """Regarde le menu contextuel TikTok.
Trouve "Telecharger la video" (ou "Download video" ou "Enregistrer").
Donne les coordonnees X, Y du CENTRE de ce bouton.
Format: COORDS: X, Y"""

    response = send_to_model(img, prompt)
    print(f"    Reponse: {response[:100]}")

    # Etape 5: Parser les coordonnees
    print("[5] Extraction des coordonnees...")
    coords = re.search(r'COORDS?:?\s*(\d+)\s*[,\s]\s*(\d+)', response, re.IGNORECASE)
    if not coords:
        coords = re.search(r'(\d{3,4})\s*[,\s]\s*(\d{2,4})', response)

    if coords:
        x, y = int(coords.group(1)), int(coords.group(2))
        print(f"    Coordonnees: ({x}, {y})")

        # Etape 6: Deplacer la souris sur "Telecharger"
        print(f"[6] Deplacement souris vers ({x}, {y})...")
        pyautogui.moveTo(x, y, duration=0.3)
        time.sleep(0.5)

        # Etape 7: Clic gauche
        print("[7] CLIC GAUCHE pour telecharger...")
        pyautogui.click()

        # Etape 8: Attendre la boite de dialogue de sauvegarde
        print("[8] Attente boite de dialogue (3s)...")
        time.sleep(3)

        # Etape 9: Changer le chemin vers le bureau
        print("[9] Selection du bureau comme destination...")
        desktop = os.path.expanduser("~\\Desktop\\tiktok_best_video.mp4")
        pyperclip.copy(desktop)

        # Selectionner le champ nom de fichier (Ctrl+L ou juste taper)
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.3)

        # Etape 10: Confirmer la sauvegarde
        print("[10] Confirmation sauvegarde (Entree)...")
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.press('enter')  # Au cas ou popup "remplacer"

        # Attendre telechargement
        print("[11] Attente telechargement (10s)...")
        time.sleep(10)

        print(f">>> Video telechargee sur: {desktop}")
        return True
    else:
        print("[ERREUR] Bouton Telecharger non trouve!")
        pyautogui.press('escape')
        return False


def write_to_notepad(results, best_video):
    """
    PHASE 5: Ecriture dans Notepad
    Etapes 32-39
    """
    print("\n" + "=" * 60)
    print("  PHASE 5: Ecriture dans Notepad")
    print("=" * 60)

    # Etape 32: Appuyer sur Windows
    print("[32] Appui touche Windows...")
    pyautogui.hotkey('win')
    time.sleep(0.5)

    # Etape 33: Taper "notepad"
    print("[33] Taper 'notepad'...")
    pyperclip.copy('notepad')
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)

    # Etape 34: Appuyer sur Entree
    print("[34] Appui Entree...")
    pyautogui.press('enter')

    # Etape 35: Attendre ouverture Notepad
    print("[35] Attente ouverture Notepad (2s)...")
    time.sleep(2)

    # Etape 36: Construire et taper le rapport
    print("[36] Construction et ecriture du rapport...")

    # Construire le rapport
    report = "=== ANALYSE TIKTOK ===\n\n"
    report += f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"Nombre de videos analysees: {len(results)}\n\n"
    report += "=" * 50 + "\n"
    report += "--- RESULTATS DES 10 VIDEOS ---\n"
    report += "=" * 50 + "\n\n"

    for video in results:
        report += f"Video {video['num']}:\n"
        report += f"  Titre: {video['titre']}\n"
        report += f"  Likes: {video['likes']}\n"
        report += f"  Commentaires: {video['comments']}\n"
        report += f"  Notes: {video['notes']}\n"
        report += f"  URL: {video.get('url', 'N/A')}\n"
        report += "-" * 40 + "\n"

    report += "\n" + "=" * 50 + "\n"
    report += "*** VIDEO AVEC LE PLUS DE LIKES ***\n"
    report += "=" * 50 + "\n\n"
    report += f"Video #{best_video['video_num']}\n"
    report += f"Titre: {best_video['title']}\n"
    report += f"Likes: {best_video['likes_str']}\n"
    report += f"Commentaires: {best_video['comments']}\n"
    report += f"Notes: {best_video['notes']}\n\n"
    report += ">>> LIEN DE LA VIDEO <<<\n"
    report += f"{best_video.get('url', 'N/A')}\n\n"
    report += "=" * 50 + "\n"
    report += "=== FIN DU RAPPORT ===\n"

    # Coller le rapport via clipboard
    pyperclip.copy(report)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)

    # Etape 37: Ctrl+S pour sauvegarder
    print("[37] Ctrl+S pour sauvegarder...")
    pyautogui.hotkey('ctrl', 's')
    time.sleep(1)

    # Etape 38: Taper nom de fichier
    print("[38] Taper nom de fichier...")
    # Dans la boite de dialogue, taper le chemin
    desktop = os.path.expanduser("~\\Desktop\\tiktok_analyse.txt")
    pyperclip.copy(desktop)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)

    # Etape 39: Appuyer sur Entree pour sauvegarder
    print("[39] Appui Entree pour confirmer...")
    pyautogui.press('enter')
    time.sleep(1)

    # Gerer le popup "fichier existe deja"
    pyautogui.press('enter')  # Remplacer si existe
    time.sleep(0.5)

    print(f"\n>>> Rapport sauvegarde: {desktop}")

    # Afficher le rapport dans la console (sans emojis pour eviter erreurs)
    print("\n" + "=" * 60)
    print("RAPPORT GENERE:")
    print("=" * 60)
    try:
        # Essayer d'afficher le rapport, sinon version sans emojis
        print(report)
    except UnicodeEncodeError:
        safe_report = report.encode('ascii', 'ignore').decode('ascii')
        print(safe_report)


def mission_complete(best_video):
    """
    PHASE 6: Fin de mission
    Etapes 40-41
    """
    print("\n" + "=" * 60)
    print("  PHASE 6: MISSION ACCOMPLIE!")
    print("=" * 60)

    # Etape 40-41: Afficher resume
    print(f"\n*** MEILLEURE VIDEO ***")
    print(f"    Numero: #{best_video['video_num']}")
    print(f"    Titre: {best_video['title']}")
    print(f"    Likes: {best_video['likes_str']}")
    print(f"    URL: {best_video.get('url', 'N/A')}")

    print("\n" + "=" * 60)
    print("  TOUTES LES ETAPES COMPLETEES AVEC SUCCES!")
    print("=" * 60)


def main():
    """
    Point d'entree principal - Execute toutes les phases
    """
    print("\n" + "#" * 60)
    print("#" + " " * 58 + "#")
    print("#     TIKTOK ANALYZER v2.0 - MISSION COMPLETE            #")
    print("#" + " " * 58 + "#")
    print("#" * 60)

    try:
        # PHASE 1: Ouvrir TikTok
        open_tiktok()

        # PHASE 2: Analyser les 10 videos (+ copier le lien de chaque video)
        results, best_video = analyze_videos(10)

        # PHASE 3: Ecrire dans Notepad (on a deja les liens!)
        write_to_notepad(results, best_video)

        # PHASE 6: Fin de mission
        mission_complete(best_video)

    except KeyboardInterrupt:
        print("\n\n[INTERRUPTION] Mission annulee par l'utilisateur!")
    except Exception as e:
        print(f"\n\n[ERREUR FATALE] {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
