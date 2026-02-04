# Mission en cours

## Problème initial
L'agent GUI avec VLM (qwen3-vl) ne donne pas de coordonnées pixel précises - se perd en boucles répétitives.

## Solution adoptée
- **OCR (EasyOCR)** pour détecter du texte avec coordonnées précises
- **YOLO** pour détecter des objets (personnes, etc.)
- VLM uniquement pour le raisonnement, pas pour les coordonnées

## Fonctions créées

### ocr_utils.py (NOUVEAU - TESTE OK)
- `find_text_on_screen(text)` - trouve un texte, retourne {x, y, confidence}
- `find_all_text_on_screen()` - liste tous les textes détectés
- `click_on_text(text)` - trouve et clique sur un texte
- `get_reader()` - initialise EasyOCR (cache singleton)

### tiktok_copier_lien.py (REFAIT - TESTE OK)
- `ouvrir_tiktok_droite()` - ouvre TikTok et ancre à droite
- `copier_lien_tiktok()` - clic droit + OCR pour trouver "Copier le lien"

### chrome_utils.py (TESTE OK)
- `ouvrir_onglet()` - ouvre un nouvel onglet Chrome (Ctrl+T)
- `fermer_onglet()` - ferme l'onglet actuel (Ctrl+W)
- `ouvrir_url(url)` - ouvre une URL dans Chrome
- `focus_chrome()` - met Chrome au premier plan
- `is_chrome_running()` - vérifie si Chrome tourne
- `launch_chrome()` - lance Chrome

### notepad_utils.py (TESTE OK)
- `ouvrir_notepad()` - ouvre Notepad
- `ecrire_texte(texte)` - écrit du texte
- `effacer_tout()` - efface le contenu
- `sauvegarder(chemin)` - sauvegarde le fichier
- `fermer_notepad()` - ferme Notepad
- `nouveau_fichier()` - nouveau fichier

### explorer_utils.py (TESTE OK)
- `ouvrir_explorateur(chemin)` - ouvre l'Explorateur
- `ouvrir_dossier(chemin)` - ouvre un dossier
- `naviguer_vers(chemin)` - navigue vers un chemin
- `remonter_dossier()` - remonte au parent
- `retour()` / `avant()` - navigation historique
- `nouveau_dossier()` - crée un dossier
- `rechercher(terme)` - recherche
- `fermer_explorateur()` - ferme

### window_utils.py (TESTE OK)
- `lister_fenetres()` - liste les fenêtres ouvertes
- `focus_fenetre(process/titre)` - met au premier plan
- `minimiser_fenetre()` / `maximiser_fenetre()` - redimensionner
- `fermer_fenetre()` - ferme la fenêtre active
- `minimiser_tout()` - Win+D
- `basculer_fenetre()` - Alt+Tab
- `fenetre_gauche()` / `fenetre_droite()` - ancrer
- `fermer_application(process)` - force kill

### mouse_utils.py (TESTE OK)
- `position()` - position actuelle
- `deplacer(x, y)` - déplace la souris
- `clic(x, y)` / `clic_droit(x, y)` / `double_clic(x, y)`
- `drag(x1, y1, x2, y2)` - glisser-déposer
- `scroll_haut(n)` / `scroll_bas(n)` - scroll

## Tests effectués
- [x] OCR find_text_on_screen() - OK
- [x] OCR click_on_text() - OK
- [x] YOLO détection personne - OK
- [x] Copier lien TikTok via OCR - OK
- [x] Toutes les fonctions utilitaires - OK

## Apprentissages clés

⚠️ **Les VLM ne donnent PAS de coordonnées précises !**
- qwen3-vl, UI-TARS, etc. : comprennent les images mais inventent les coordonnées
- Pour des coordonnées pixel : utiliser OCR (texte) ou YOLO (objets)

## Historique
- 2026-02-04 : Diagnostic complet, création chrome_utils.py et autres utils
- 2026-02-04 : Ajout ocr_utils.py avec EasyOCR - FONCTIONNE pour coordonnées précises
- 2026-02-04 : TikTok copier lien via OCR - SUCCES
