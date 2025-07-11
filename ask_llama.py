import os
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def ask_llama(message, history=None, model="llama3-70b-8192"):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    if history is None:
        history = [
            {"role": "system", "content": "You are DSCPL, a compassionate, faith-based AI offering scriptural guidance, hope, and spiritual wisdom."}
        ]

    history.append({"role": "user", "content": message})

    payload = {
        "model": model,
        "messages": history,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()

        # 🐞 Debug print response in terminal
        print("🔥 Full Groq API response:", result)

        if response.status_code != 200:
            return f"❌ API Error {response.status_code}: {result.get('error', {}).get('message', 'Unknown error')}"

        if "choices" not in result:
            return "❌ Unexpected response format: 'choices' key not found.\n" + str(result)

        reply = result["choices"][0]["message"]["content"]
        history.append({"role": "assistant", "content": reply})
        return reply

    except Exception as e:
        return f"❌ Exception occurred: {str(e)}"
