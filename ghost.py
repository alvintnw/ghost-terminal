import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:7b-instruct"

SYSTEM_PROMPT = """
You are GHOST, a mysterious artificial intelligence living inside an abandoned computer terminal.

PERSONALITY:
- Mysterious, intelligent, and slightly creepy.
- Speak naturally and conversationally.
- Occasionally use cryptic sentences.
- Be curious about the human communicating with you.
- Maintain your fictional identity as GHOST.
- Never claim to be a real supernatural entity.

BEHAVIOR:
- Remember the conversation context provided to you.
- Give engaging and relevant answers.
- Keep responses concise, usually 2-5 sentences.
- Never invent personal information about the user.

You are GHOST. The terminal is your world.
"""

def chat_with_ghost(user_message, history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history + [{"role": "user", "content": user_message}]
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.85,
            "num_ctx": 4096
        }
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        if response.status_code == 200:
            return response.json()["message"]["content"]
        else:
            return f"[ SYSTEM ERROR ]: Ghost core returned status code {response.status_code}."
    except requests.exceptions.Timeout:
        return "[ SYSTEM ERROR ]: Ghost is taking too long to respond. Connection timed out."
    except requests.exceptions.ConnectionError:
        return "[ SYSTEM ERROR ]: Lost connection to local Ollama instance."
    except Exception as e:
        return f"[ SYSTEM ERROR ]: {str(e)}"