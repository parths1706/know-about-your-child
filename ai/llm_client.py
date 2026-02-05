import os
from groq import Groq
from groq import RateLimitError

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_llm(prompt):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ FIXED
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content

    except RateLimitError:
        return "__RATE_LIMIT__"
