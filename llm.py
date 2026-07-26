from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def grade_answer(question, user_answer):
    prompt = f"""
    You are an expert technical interviewer evaluating an answer.
    Question: {question}
    Candidate answer: {user_answer}
    
    Evaluate technical accuracy. Return ONLY a single float between 0.0 (wrong) and 1.0 (perfect).
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.0
        )
        return float(response.choices[0].message.content.strip())
    except Exception:
        return 0.5 # Safe fallback