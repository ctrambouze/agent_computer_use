"""
Agent GUI Autonome - UI-TARS + PyAutoGUI
Controle l'ordinateur via vision + actions automatiques
"""

import base64
import io
import json
import re
import time
from dataclasses import dataclass
from typing import Optional

import pyautogui
import requests
from PIL import ImageGrab

# Configuration
OLLAMA_URL = "http://localhost:11434"
MODEL = "qwen3-vl:30b"  # VLM avec vision fonctionnelle

# Securite PyAutoGUI
pyautogui.FAILSAFE = True  # Coin haut-gauche = stop
pyautogui.PAUSE = 0.5  # Pause entre actions


@dataclass
class Action:
    """Represente une action a executer"""
    type: str  # click, type, scroll, hotkey, wait
    x: Optional[int] = None
    y: Optional[int] = None
    text: Optional[str] = None
    keys: Optional[list] = None
    direction: Optional[str] = None
    amount: Optional[int] = None


def capture_screen() -> str:
    """Capture l'ecran et retourne en base64"""
    screenshot = ImageGrab.grab()
    buffer = io.BytesIO()
    screenshot.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()


def send_to_model(image_b64: str, prompt: str) -> str:
    """Envoie l'image et le prompt au modele VLM"""
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "images": [image_b64],
        "stream": False,
        "options": {
            "temperature": 0.3,
            "num_predict": 512,
            "top_p": 0.9
        }
    }

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json=payload,
        timeout=180
    )
    response.raise_for_status()
    data = response.json()

    # Qwen3-vl met tout dans "thinking", pas "response"
    result = data.get("response", "")
    thinking = data.get("thinking", "")

    # Si response vide, utiliser thinking
    if not result.strip() and thinking:
        result = thinking

    return result


def parse_action(response: str) -> Optional[Action]:
    """Parse la reponse du modele en action executable"""
    # Chercher ACTION: dans la reponse (meme au milieu du texte)
    action_match = re.search(r'ACTION:\s*(.+?)(?:\n|$)', response, re.IGNORECASE)
    if action_match:
        response = "ACTION: " + action_match.group(1)

    response_lower = response.lower()

    # Patterns pour detecter les actions
    # Click pattern: "click at (x, y)" ou "click on X"
    click_match = re.search(r'click.*?(\d+)[,\s]+(\d+)', response_lower)
    if click_match:
        return Action(
            type="click",
            x=int(click_match.group(1)),
            y=int(click_match.group(2))
        )

    # Type pattern: "type 'text'" ou "enter 'text'"
    type_match = re.search(r'(?:type|enter|input)[:\s]+["\'](.+?)["\']', response, re.IGNORECASE)
    if type_match:
        return Action(type="type", text=type_match.group(1))

    # Hotkey pattern: "press ctrl+t" ou "hotkey win+r"
    hotkey_match = re.search(r'(?:press|hotkey)[:\s]+([a-z]+\+[a-z]+)', response_lower)
    if hotkey_match:
        keys = hotkey_match.group(1).split('+')
        return Action(type="hotkey", keys=keys)

    # Key pattern: "press enter" ou "press tab"
    key_match = re.search(r'press[:\s]+(\w+)', response_lower)
    if key_match and '+' not in key_match.group(1):
        return Action(type="hotkey", keys=[key_match.group(1)])

    # Scroll pattern
    if 'scroll down' in response_lower:
        return Action(type="scroll", direction="down", amount=3)
    if 'scroll up' in response_lower:
        return Action(type="scroll", direction="up", amount=3)

    # Wait pattern
    wait_match = re.search(r'wait[:\s]+(\d+)', response_lower)
    if wait_match:
        return Action(type="wait", amount=int(wait_match.group(1)))

    return None


def execute_action(action: Action) -> bool:
    """Execute une action avec PyAutoGUI"""
    try:
        if action.type == "click" and action.x and action.y:
            print(f"  -> Click at ({action.x}, {action.y})")
            pyautogui.click(action.x, action.y)
            return True

        elif action.type == "type" and action.text:
            print(f"  -> Type: '{action.text}'")
            # Utiliser le presse-papier pour supporter les caracteres speciaux (AZERTY)
            import pyperclip
            pyperclip.copy(action.text)
            pyautogui.hotkey('ctrl', 'v')
            return True

        elif action.type == "hotkey" and action.keys:
            print(f"  -> Hotkey: {'+'.join(action.keys)}")
            pyautogui.hotkey(*action.keys)
            return True

        elif action.type == "scroll":
            direction = -3 if action.direction == "down" else 3
            print(f"  -> Scroll {action.direction}")
            pyautogui.scroll(direction)
            return True

        elif action.type == "wait" and action.amount:
            print(f"  -> Wait {action.amount}s")
            time.sleep(action.amount)
            return True

    except Exception as e:
        print(f"  ! Erreur action: {e}")
    return False


def run_agent(mission: str, max_steps: int = 20):
    """
    Execute une mission de maniere autonome

    Args:
        mission: Description de la tache a accomplir
        max_steps: Nombre maximum d'etapes
    """
    print("=" * 50)
    print(f"Mission: {mission}")
    print("=" * 50)

    system_prompt = """Tu es un agent GUI autonome. Tu vois l'ecran Windows et tu executes des actions.

REPONDS TOUJOURS avec exactement ce format (une seule ligne):
ACTION: [commande]

COMMANDES DISPONIBLES:
- click at (X, Y) - cliquer a ces coordonnees pixel
- type "texte" - taper ce texte au clavier
- press win - touche Windows (menu demarrer)
- press enter - touche Entree
- hotkey ctrl+t - ouvrir nouvel onglet navigateur
- hotkey ctrl+l - selectionner barre d'adresse
- scroll down - defiler vers le bas
- wait 2 - attendre 2 secondes (IMPORTANT: utilise apres press enter pour laisser l'app s'ouvrir!)
- DONE - mission accomplie

EXEMPLES DE REPONSES CORRECTES:
ACTION: press win
ACTION: click at (960, 540)
ACTION: type "google.com"
ACTION: hotkey ctrl+l
ACTION: DONE - Page Google ouverte

REGLES STRICTES:
1. UNE SEULE action par reponse
2. Commence TOUJOURS par "ACTION:"
3. Pour ouvrir une app: press win, type "nom app", press enter, puis WAIT 2 pour laisser l'app s'ouvrir!
4. APRES press enter pour ouvrir une app: TOUJOURS faire wait 2 avant de taper du texte
5. Verifie VISUELLEMENT que l'app est ouverte avant de taper dedans

NE REFLECHIS PAS. Reponds UNIQUEMENT avec "ACTION: ..." sur une seule ligne.

TRES IMPORTANT:
- AVANT de taper du texte, CLIQUE sur la fenetre cible (Notepad, Chrome, etc.) pour la mettre au premier plan!
- Apres avoir tape le texte demande, dis IMMEDIATEMENT "ACTION: DONE"
- Ne retape JAMAIS le meme texte deux fois
- Si tu vois le texte deja ecrit dans l'application, dis "ACTION: DONE"
- Quand tu vois que l'action a ete effectuee (ex: menu ouvert), reponds DONE immediatement!
- Utilise les raccourcis clavier quand possible (ex: win pour menu demarrer)
- Ne repete pas la meme action plus de 2 fois si elle ne fonctionne pas
"""

    action_history = []
    repeat_count = 0
    last_action_str = ""

    for step in range(max_steps):
        print(f"\n--- Etape {step + 1}/{max_steps} ---")

        # Capture l'ecran
        print("  Capture ecran...")
        image_b64 = capture_screen()

        # Construire le prompt avec historique
        history_text = ""
        if action_history:
            history_text = "\n\nACTIONS DEJA EFFECTUEES:\n" + "\n".join(f"- {a}" for a in action_history[-5:])
            if repeat_count >= 2:
                history_text += f"\n\nATTENTION: Tu as repete la meme action {repeat_count} fois. Si l'ecran a change, dis DONE. Sinon essaie autre chose!"

        prompt = f"""{system_prompt}

MISSION: {mission}
{history_text}

Quelle est la PROCHAINE ACTION? Reponds UNIQUEMENT: ACTION: [commande]
Exemple: ACTION: click at (500, 300)"""

        # Envoyer au modele
        print("  Analyse en cours...")
        try:
            response = send_to_model(image_b64, prompt)
            print(f"  Modele: {response[:200]}...")
        except Exception as e:
            print(f"  ! Erreur modele: {e}")
            continue

        # Verifier si termine (seulement si ACTION: DONE au debut de ligne)
        if re.search(r'^ACTION:\s*DONE', response, re.IGNORECASE | re.MULTILINE):
            print("\n" + "=" * 50)
            print("MISSION TERMINEE!")
            print(response)
            print("=" * 50)
            return True

        # Parser et executer l'action
        action = parse_action(response)
        if action:
            action_str = f"{action.type} {action.x},{action.y}" if action.x else f"{action.type} {action.text or action.keys or action.direction}"

            # Detecter les repetitions
            if action_str == last_action_str:
                repeat_count += 1
            else:
                repeat_count = 0
                last_action_str = action_str

            action_history.append(action_str)
            success = execute_action(action)
            if success:
                time.sleep(1.5)  # Attendre que l'action prenne effet
        else:
            print("  ! Aucune action reconnue dans la reponse")

    print("\n! Nombre maximum d'etapes atteint")
    return False


def test_connection():
    """Teste la connexion a Ollama"""
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        models = r.json().get("models", [])
        print("Connexion Ollama: OK")
        print(f"Modeles disponibles: {[m['name'] for m in models]}")
        return True
    except Exception as e:
        print(f"Erreur connexion Ollama: {e}")
        return False


if __name__ == "__main__":
    import sys

    print("=" * 50)
    print("  Agent GUI Autonome")
    print("=" * 50)

    # Test connexion
    if not test_connection():
        print("Lancez d'abord: ollama serve")
        sys.exit(1)

    # Mission par defaut ou depuis argument
    if len(sys.argv) > 1:
        mission = " ".join(sys.argv[1:])
    else:
        mission = input("\nMission: ")

    if mission:
        run_agent(mission)
    else:
        print("Aucune mission fournie.")
