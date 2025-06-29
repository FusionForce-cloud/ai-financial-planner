import openai

def get_budget_advice(income, expense, goal, api_key):
    openai.api_key = api_key
    prompt = f"""
    User has a monthly income of ₹{income} and spends ₹{expense}. They want to save ₹{goal}.
    Suggest 3 personalized and actionable tips to achieve this goal.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response['choices'][0]['message']['content']
