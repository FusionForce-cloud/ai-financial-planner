from openai import OpenAI

def get_budget_advice(income, expense, goal, api_key):
    client = OpenAI(api_key=api_key)

    prompt = f"""
    User has a monthly income of ₹{income} and spends ₹{expense}. They want to save ₹{goal}.
    Suggest 3 personalized and actionable tips to achieve this goal.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if your API key supports it
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content
