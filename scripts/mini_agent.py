#!/usr/bin/env python3
"""Mini-agent minimal : un LLM + un outil + une boucle.

Démontre la différence entre un simple appel LLM et un agent :
le modèle décide d'appeler un outil, reçoit le résultat, et itère
jusqu'à produire une réponse finale.

Usage :
    LLM_BASE_URL=... LLM_API_KEY=... LLM_MODEL=... python3 mini_agent.py
"""
import json
import os
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

# --- 1. L'outil ----------------------------------------------------------
# Un outil = une fonction + sa description (pour que le modèle sache l'utiliser).


def get_current_time(timezone: str) -> str:
    """Renvoie l'heure actuelle dans le fuseau horaire demandé (ex: Europe/Paris)."""
    return datetime.now(ZoneInfo(timezone)).strftime("%H:%M:%S (%A)")


TOOLS = {
    "get_current_time": {
        "description": "Renvoie l'heure actuelle dans un fuseau horaire (ex: 'Europe/Paris', 'Asia/Tokyo').",
        "call": get_current_time,
    }
}

# --- 2. L'appel au modèle ------------------------------------------------
# Le modèle ne sait pas l'heure qu'il est (ses données d'entraînement sont figées).
# Il doit donc appeler un outil pour le découvrir.


def call_model(messages: list) -> dict:
    """Appelle un LLM compatible OpenAI et renvoie son message de réponse."""
    req = urllib.request.Request(
        f"{BASE_URL}/chat/completions",
        data=json.dumps(
            {
                "model": MODEL,
                "messages": messages,
                "tools": [
                    {
                        "type": "function",
                        "function": {
                            "name": name,
                            "description": t["description"],
                            "parameters": {
                                "type": "object",
                                "properties": {"timezone": {"type": "string"}},
                            },
                        },
                    }
                    for name, t in TOOLS.items()
                ],
                "tool_choice": "auto",
            }
        ).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


# --- 3. La boucle --------------------------------------------------------
# C'est LA différence avec un simple appel LLM : on itère.


def run(question: str, max_turns: int = 6) -> None:
    messages = [{"role": "user", "content": question}]
    for turn in range(1, max_turns + 1):
        resp = call_model(messages)["choices"][0]["message"]
        messages.append(resp)  # on garde tout l'historique

        if resp.get("tool_calls"):
            for tc in resp["tool_calls"]:
                name = tc["function"]["name"]
                args = json.loads(tc["function"]["arguments"])
                print(f"[tour {turn}] le modèle appelle l'outil {name}({args})")
                result = TOOLS[name]["call"](**args)
                messages.append(
                    {"role": "tool", "tool_call_id": tc["id"], "content": result}
                )
                print(f"[tour {turn}] résultat de l'outil : {result}")
        else:
            print(f"[tour {turn}] réponse finale : {resp['content']}")
            break


if __name__ == "__main__":
    BASE_URL = os.environ["LLM_BASE_URL"]
    API_KEY = os.environ["LLM_API_KEY"]
    MODEL = os.environ.get("LLM_MODEL", "deepseek/deepseek-v4-pro")
    run("Quelle heure est-il à Tokyo ? Et à Paris ?")
