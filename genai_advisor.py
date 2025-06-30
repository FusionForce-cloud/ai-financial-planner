from openai import OpenAI, RateLimitError
import time

def get_budget_advice(income, expense, goal, api_key):
    client = OpenAI(api_key=api_key)

    prompt = f"""
    The user has a monthly income of ₹{income} and spends ₹{expense}. They want to save ₹{goal}.
    Please provide 3 personalized, actionable financial tips to help meet the savings goal.
    """

    for attempt in range(3):  # Retry up to 3 times
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content
        except RateLimitError:
            wait = (2 ** attempt) * 3  # 3s, 6s, 12s
            time.sleep(wait)
        except Exception as e:
            return f"❌ Error from OpenAI: {str(e)}"

    return "⚠️ OpenAI rate limit reached. Please try again later."
