import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def train_savings_predictor(data):
    data['Savings'] = data['Income'] - data['Expense']
    data['Month'] = pd.to_datetime(data['Date']).dt.month
    grouped = data.groupby('Month')[['Income', 'Expense', 'Savings']].sum().reset_index()

    model = LinearRegression()
    X = grouped[['Income', 'Expense']]
    y = grouped['Savings']
    model.fit(X, y)
    return model

def predict_savings(model, income, expense):
    pred = model.predict([[income, expense]])
    return pred[0]
