# Mission en cours

## Problème initial
L'agent GUI avec VLM (qwen3-vl) ne suit pas bien les instructions - se perd en boucles répétitives.

## Solution adoptée
Fonctions directes PyAutoGUI sans VLM pour les tâches simples et répétitives.

## Fonctions créées

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
- [x] capture_screen() - OK
- [x] send_to_model() - OK (qwen3-vl voit l'écran)
- [x] parse_action() - OK
- [x] execute_action() - OK
- [x] ouvrir_onglet() - OK
- [x] fermer_onglet() - OK
- [x] 5 cycles ouvrir/fermer - OK

## Prochaines étapes
- [ ] Autres fonctions utilitaires si besoin
- [ ] Intégrer dans l'agent principal

## Historique
- 2026-02-04 : Diagnostic complet, création chrome_utils.py
