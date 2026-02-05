import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_llm(prompt, expect_json=True):
    try:
        messages = [{"role": "user", "content": prompt}]

        # 🔑 REQUIRED for Groq when using json_object
        if expect_json:
            messages[0]["content"] = "Return JSON only.\n" + prompt

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
            response_format={"type": "json_object"} if expect_json else None
        )

        return response.choices[0].message.content

    except Exception as e:
        print("LLM ERROR:", e)
        return "__ERROR__"
