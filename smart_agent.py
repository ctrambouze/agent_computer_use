"""
Smart Agent avec Memoire Persistante
Memorise les actions reussies et les reutilise
"""

import json
import os
import re
import time
import pyautogui
import pyperclip
from agent_gui import capture_screen, send_to_model, parse_action, execute_action

# Config
MEMORY_FILE = os.path.join(os.path.dirname(__file__), "memory.json")
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3


def load_memory():
    """Charge la memoire depuis le fichier JSON"""
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"missions": []}


def save_memory(memory):
    """Sauvegarde la memoire dans le fichier JSON"""
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)


def find_matching_mission(mission_text, memory):
    """Cherche une mission similaire dans la memoire"""
    mission_lower = mission_text.lower()

    best_match = None
    best_score = 0

    for saved_mission in memory.get("missions", []):
        score = 0
        # Verifier les keywords
        for keyword in saved_mission.get("keywords", []):
            if keyword.lower() in mission_lower:
                score += 1

        # Verifier le nom
        if saved_mission["name"].lower() in mission_lower:
            score += 2

        if score > best_score:
            best_score = score
            best_match = saved_mission

    # Retourner seulement si score suffisant
    if best_score >= 1:
        return best_match
    return None


def extract_url(text):
    """Extrait une URL ou nom de site du texte"""
    # Chercher une URL complete
    url_match = re.search(r'https?://[^\s]+', text)
    if url_match:
        return url_match.group()

    # Chercher un domaine
    domain_match = re.search(r'(\w+\.(com|fr|org|net|io|co))', text, re.IGNORECASE)
    if domain_match:
        return "https://" + domain_match.group()

    return None


def execute_memorized_steps(mission_text, steps):
    """Execute une serie d'etapes memorisees"""
    print(f"\n[MEMOIRE] Execution de {len(steps)} etapes memorisees...")

    for i, step in enumerate(steps):
        action_type = step["action"]
        params = step.get("params", [])

        # Remplacer les variables
        if "$URL" in str(params):
            url = extract_url(mission_text)
            if url:
                params = [p.replace("$URL", url) if isinstance(p, str) else p for p in params]

        if "$TEXT" in str(params):
            # Extraire le texte entre guillemets
            text_match = re.search(r'["\']([^"\']+)["\']', mission_text)
            if text_match:
                params = [p.replace("$TEXT", text_match.group(1)) if isinstance(p, str) else p for p in params]

        print(f"  [{i+1}] {action_type} {params}")

        try:
            if action_type == "hotkey":
                pyautogui.hotkey(*params)
            elif action_type == "type":
                pyperclip.copy(params[0])
                pyautogui.hotkey('ctrl', 'v')
            elif action_type == "click":
                pyautogui.click(params[0], params[1])
            elif action_type == "scroll":
                pyautogui.scroll(params[0])
            elif action_type == "wait":
                time.sleep(params[0])
            elif action_type == "press":
                pyautogui.press(params[0])

            time.sleep(0.5)
        except Exception as e:
            print(f"  ! Erreur: {e}")
            return False

    return True


def learn_from_success(mission_text, actions_taken, memory):
    """Apprend d'une mission reussie et sauvegarde dans la memoire"""
    # Creer une nouvelle entree
    keywords = [w for w in mission_text.lower().split() if len(w) > 3]

    new_mission = {
        "name": mission_text[:50],
        "keywords": keywords[:5],
        "steps": actions_taken,
        "learned": True
    }

    memory["missions"].append(new_mission)
    save_memory(memory)
    print(f"\n[MEMOIRE] Nouvelle mission apprise et sauvegardee!")


def run_smart_agent(mission_text, max_steps=15):
    """Agent intelligent avec memoire"""
    print("=" * 50)
    print("  Smart Agent avec Memoire")
    print("=" * 50)
    print(f"\nMission: {mission_text}")

    # Charger la memoire
    memory = load_memory()
    print(f"[MEMOIRE] {len(memory.get('missions', []))} missions en memoire")

    # Chercher une mission similaire
    matching = find_matching_mission(mission_text, memory)

    if matching:
        print(f"\n[MEMOIRE] Mission similaire trouvee: '{matching['name']}'")
        success = execute_memorized_steps(mission_text, matching["steps"])
        if success:
            print("\n" + "=" * 50)
            print("MISSION TERMINEE (depuis memoire)!")
            print("=" * 50)
            return True
        else:
            print("[MEMOIRE] Echec, passage au mode vision...")
    else:
        print("\n[MEMOIRE] Aucune mission similaire, mode vision active...")

    # Mode vision classique
    actions_taken = []

    system_prompt = """Tu es un agent GUI. Reponds UNIQUEMENT avec: ACTION: [commande]

COMMANDES:
- click at (X, Y)
- type "texte"
- press win/enter/tab/escape
- hotkey ctrl+l / ctrl+n / ctrl+t
- scroll down/up
- wait N
- DONE

UNE SEULE action par reponse. Apres avoir termine, dis ACTION: DONE"""

    for step in range(max_steps):
        print(f"\n--- Vision {step + 1}/{max_steps} ---")

        image_b64 = capture_screen()

        prompt = f"""{system_prompt}

MISSION: {mission_text}

Quelle est la PROCHAINE ACTION?"""

        try:
            response = send_to_model(image_b64, prompt)
            print(f"  Modele: {response[:100]}...")
        except Exception as e:
            print(f"  Erreur: {e}")
            continue

        # Verifier si termine
        if re.search(r'^ACTION:\s*DONE', response, re.IGNORECASE | re.MULTILINE):
            print("\n" + "=" * 50)
            print("MISSION TERMINEE!")
            print("=" * 50)

            # Apprendre de cette mission si nouvelles actions
            if actions_taken and not matching:
                learn_from_success(mission_text, actions_taken, memory)

            return True

        # Parser et executer
        action = parse_action(response)
        if action:
            # Enregistrer l'action pour apprentissage
            if action.type == "hotkey":
                actions_taken.append({"action": "hotkey", "params": action.keys})
            elif action.type == "type":
                actions_taken.append({"action": "type", "params": [action.text]})
            elif action.type == "click":
                actions_taken.append({"action": "click", "params": [action.x, action.y]})
            elif action.type == "scroll":
                actions_taken.append({"action": "scroll", "params": [-3 if action.direction == "down" else 3]})
            elif action.type == "wait":
                actions_taken.append({"action": "wait", "params": [action.amount]})

            execute_action(action)
            time.sleep(1)
        else:
            print("  ! Aucune action reconnue")

    print("\n! Maximum d'etapes atteint")
    return False


def show_memory():
    """Affiche le contenu de la memoire"""
    memory = load_memory()
    print("\n=== MEMOIRE DE L'AGENT ===\n")
    for i, mission in enumerate(memory.get("missions", []), 1):
        learned = " (appris)" if mission.get("learned") else ""
        print(f"{i}. {mission['name']}{learned}")
        print(f"   Keywords: {', '.join(mission.get('keywords', []))}")
        print(f"   Steps: {len(mission.get('steps', []))}")
        print()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "--memory":
            show_memory()
        else:
            mission = " ".join(sys.argv[1:])
            run_smart_agent(mission)
    else:
        print("Usage:")
        print("  python smart_agent.py \"Ta mission\"")
        print("  python smart_agent.py --memory  (voir la memoire)")
