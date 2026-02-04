# Mission en cours

## Problème initial
L'agent GUI avec VLM (qwen3-vl) ne suit pas bien les instructions - se perd en boucles répétitives.

## Solution adoptée
Fonctions directes PyAutoGUI sans VLM pour les tâches simples et répétitives.

## Fonctions créées

### chrome_utils.py (TESTE OK - 5/5 cycles)
- `ouvrir_onglet()` - ouvre un nouvel onglet Chrome (Ctrl+T)
- `fermer_onglet()` - ferme l'onglet actuel (Ctrl+W)
- `ouvrir_url(url)` - ouvre une URL dans Chrome
- `focus_chrome()` - met Chrome au premier plan
- `is_chrome_running()` - vérifie si Chrome tourne
- `launch_chrome()` - lance Chrome

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
