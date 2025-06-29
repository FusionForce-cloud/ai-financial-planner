import streamlit as st
import pandas as pd
from budget_predictor import train_savings_predictor, predict_savings
from expense_categorizer import categorize_expense
from genai_advisor import get_budget_advice

st.title("💸 AI-Powered Financial Planner")

uploaded_file = st.file_uploader("Upload your transaction data (CSV)", type="csv")

# Securely load OpenAI API key
api_key = st.secrets["openai"]["api_key"] if "openai" in st.secrets else ""
if not api_key:
    api_key = st.text_input("Enter your OpenAI API Key (optional for advice)", type="password")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['Category'] = df['Description'].apply(categorize_expense)
    df['Income'] = df.apply(lambda x: x['Amount'] if x['Type'] == 'Income' else 0, axis=1)
    df['Expense'] = df.apply(lambda x: -x['Amount'] if x['Type'] == 'Expense' else 0, axis=1)

    st.subheader("📊 Data Preview")
    st.dataframe(df)

    model = train_savings_predictor(df)
    income = st.number_input("Expected Monthly Income", value=50000)
    expense = st.number_input("Expected Monthly Expense", value=30000)
    goal = st.number_input("Target Monthly Savings", value=10000)

    predicted_savings = predict_savings(model, income, expense)
    st.metric("Predicted Savings", f"₹{predicted_savings:.2f}")

    if api_key:
        advice = get_budget_advice(income, expense, goal, api_key)
        st.subheader("💬 AI Budget Advice")
        st.write(advice)

    st.bar_chart(df.groupby('Category')['Expense'].sum())
else:
    st.warning("Please upload a CSV file to continue.")
