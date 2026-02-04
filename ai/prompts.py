def question_prompt(region, age, gender):
    return f"""
You are a world-class child psychology expert. Based on the child's details, generate 5-7 highly relevant, insightful questions to help understand the child better.

Child Details:
- Region: {region}
- Age: {age}
- Gender: {gender}

Your goal is to uncover insights about their:
- Emotional well-being
- Social development
- Daily habits and routine
- Strengths and challenges

OUTPUT REQUIREMENT:
You must return ONLY a JSON array of objects. Each object must have:
- "question": The question text (empathy-driven and supportive)
- "type": One of ["yes_no", "options", "scale"]
- "options": (Only if type is "options") A list of 3-4 possible answers.

Note: DO NOT use "text" type questions. User wants selective answers only (Yes/No, Multiple Choice, or Range/Scale).

Example Format:
[
  {{"question": "How often does your child express curiosity about new things?", "type": "scale"}},
  {{"question": "Does your child prefer playing alone or with others?", "type": "options", "options": ["Mostly alone", "Mostly with others", "A mix of both"]}}
]

Return ONLY the JSON array. Do not include any other text.
"""


def analysis_prompt(region, age, gender, answers):
    formatted_answers = "\n".join(
        [f"{k}: {v}" for k, v in answers.items()]
    )

    return f"""
You are an expert child psychologist and parenting coach.

Child Details:
Region: {region}
Age: {age}
Gender: {gender}

Parent Answers:
{formatted_answers}

Generate a detailed response with TWO SECTIONS:

1️⃣ Know About Your Child
- psychology
- behavior
- emotional development
- health & routine
- social skills

2️⃣ Parenting Tips
- how parents can support the child
- communication style
- discipline guidance
- emotional bonding
- region-aware advice

Tone: supportive, clear, professional.
"""
