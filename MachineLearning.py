import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

FILE = "tracker.csv"
data = pd.read_csv(FILE)

def predict(data):

        data = data.drop(columns=["Day", "Description", "Category"])
        data['SignedAmount'] = data['Amount'] * data['Type'].map({'Income': 1, 'Expense': -1})

        monthly = data.groupby(['Year', 'Month', 'Type'])['Amount'].sum().reset_index()
        monthly_pivot = monthly.pivot(index=['Year', 'Month'], columns='Type', values='Amount').fillna(0).reset_index()

        monthly_pivot['Month_num'] = range(1, len(monthly_pivot) + 1)
        monthly_pivot['Savings'] = monthly_pivot['Income'] - monthly_pivot['Expense']

        # print(monthly_pivot)

        X = monthly_pivot[['Month_num']]
        y_income = monthly_pivot['Income']
        X_train, X_test, y_train, y_test = train_test_split(X, y_income, test_size=0.33, random_state=42)

        LR_income = LinearRegression()
        LR_income.fit(X_train, y_train)

        y_expense = monthly_pivot['Expense']
        X_train, X_test, y_train, y_test = train_test_split(X, y_expense, test_size=0.33, random_state=42)

        LR_expense = LinearRegression()
        LR_expense.fit(X_train, y_train)

        next_month = pd.DataFrame(
            {"Month_num": [monthly_pivot['Month_num'].max() + 1]}
        )
        predicted_income = LR_income.predict(next_month)[0]
        predicted_expense = LR_expense.predict(next_month)[0]
        predicted_savings = predicted_income - predicted_expense

        # print("Predicted In:", predicted_income)
        # print("Predicted Exe:", predicted_expense)
        # print("Predicted Sav:", predicted_savings)

        return predicted_savings,predicted_expense,predicted_income
