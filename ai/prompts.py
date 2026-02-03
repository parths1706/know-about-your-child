def question_prompt(region, age, gender):
    return f"""
You are a child psychology expert.

Child details:
- Region: {region}
- Age: {age}
- Gender: {gender}

Generate 5–7 thoughtful questions for parents to understand:
- behavior
- emotions
- health
- social interaction
- daily habits

Questions must be age-appropriate and culturally relevant.
Return ONLY a numbered list.
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
