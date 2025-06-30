
import streamlit as st
import pandas as pd
from budget_predictor import train_savings_predictor, predict_savings
from expense_categorizer import categorize_expense
from genai_advisor import get_budget_advice
import os

st.set_page_config(page_title="AI Financial Planner", layout="centered")
st.title("💸 AI-Powered Financial Planner")

# Load API Key securely
api_key = st.secrets["openai"]["api_key"] if "openai" in st.secrets else os.getenv("OPENAI_API_KEY", "")

if not api_key:
    api_key = st.text_input("🔐 Enter your OpenAI API Key (optional for AI advice)", type="password")

st.markdown("---")
option = st.radio("📥 How would you like to provide your transaction data?", ["Upload CSV", "Enter Manually"])

# === CSV Upload ===
if option == "Upload CSV":
    uploaded_file = st.file_uploader("Upload your transaction data (.csv)", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df['Category'] = df['Description'].apply(categorize_expense)
        df['Income'] = df.apply(lambda x: x['Amount'] if x['Type'] == 'Income' else 0, axis=1)
        df['Expense'] = df.apply(lambda x: -x['Amount'] if x['Type'] == 'Expense' else 0, axis=1)

# === Manual Entry ===
elif option == "Enter Manually":
    st.subheader("📝 Enter Your Transactions")

    if 'manual_data' not in st.session_state:
        st.session_state.manual_data = []

    with st.form("manual_entry"):
        date = st.date_input("Date")
        description = st.text_input("Description")
        amount = st.number_input("Amount", value=0)
        txn_type = st.selectbox("Type", ["Income", "Expense"])
        submitted = st.form_submit_button("Add Transaction")

        if submitted:
            st.session_state.manual_data.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Description": description,
                "Amount": amount,
                "Type": txn_type
            })
            st.success("✅ Transaction added!")

    if st.session_state.manual_data:
        df = pd.DataFrame(st.session_state.manual_data)
        df['Category'] = df['Description'].apply(categorize_expense)
        df['Income'] = df.apply(lambda x: x['Amount'] if x['Type'] == 'Income' else 0, axis=1)
        df['Expense'] = df.apply(lambda x: -x['Amount'] if x['Type'] == 'Expense' else 0, axis=1)

# === Shared Logic ===
if 'df' in locals():
    st.subheader("📊 Transaction Data")
    st.dataframe(df)

    model = train_savings_predictor(df)
    income = st.number_input("💰 Expected Monthly Income", value=50000, key="income")
    expense = st.number_input("📉 Expected Monthly Expense", value=30000, key="expense")
    goal = st.number_input("🎯 Target Monthly Savings", value=10000, key="goal")

    predicted_savings = predict_savings(model, income, expense)
    st.metric("Predicted Savings", f"₹{predicted_savings:.2f}")

    if api_key:
        advice = get_budget_advice(income, expense, goal, api_key)
        st.subheader("💬 AI Budget Advice")
        st.write(advice)

    st.bar_chart(df.groupby('Category')['Expense'].sum())
else:
    st.info("Please upload a CSV file or enter at least one transaction to begin.")
