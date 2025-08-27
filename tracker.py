import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from MachineLearning import predict
from datetime import datetime
import host
import webbrowser
FILE = "tracker.csv"
save_path = "static/images/img.jpg"
data = pd.read_csv(FILE)

def add_transactions(data):

    now = datetime.now()
    year, month, day = now.year, now.month, now.day
    Category =input("Enter category (e.g. Salary, Groceries, Transport):")
    Description = input("Enter description:")
    Amount = int(input("Enter amount:"))
    Type= input("Enter type (Income/Expense): ")

    new_entry = {
        "Year": year,
        "Month": month,
        "Day": day,
        "Category": Category,
        "Description": Description,
        "Amount": Amount,
        "Type": Type
    }
    data = pd.concat([data, pd.DataFrame([new_entry])], ignore_index=True)
    data.to_csv(FILE, index=False)

def summary():

    total_income = data[data['Type'] == 'Income']['Amount'].sum()
    total_expense = data[data['Type'] == 'Expense']['Amount'].sum()
    net_savings = total_income - total_expense

    year = data.iloc[-1]["Year"]
    month = data.iloc[-1]["Month"]
    date = data.iloc[-1]["Day"]

    sav = round((1 - total_expense / total_income) * 100, 1)
    print(f"Total Income {total_income} and Total Expenditure {total_expense}, %Saved ={sav}%")
    print(f"Total net savings as of {date}/{month}/{year}= {net_savings}")


def plot_graph():

    data['SignedAmount'] = data['Amount'] * data['Type'].map({'Income': 1, 'Expense': -1})
    data['Savings'] = data['SignedAmount'].cumsum()

    sns.lineplot(data=data, x=data.index, y='Savings', marker='o', linewidth=2, color='green')
    plt.title("Savings and Transactions", fontsize=16)
    plt.xlabel("Transaction per week /income/expenditure")
    plt.ylabel("Total Savings")
    plt.tight_layout()

    plt.show()

def plot_graph_():

    data['SignedAmount'] = data['Amount'] * data['Type'].map({'Income': 1, 'Expense': -1})
    data['Savings'] = data['SignedAmount'].cumsum()

    sns.lineplot(data=data, x=data.index, y='Savings', marker='o', linewidth=2, color='green')
    plt.title("Savings and Transactions", fontsize=16)
    plt.xlabel("Transaction per week /income/expenditure")
    plt.ylabel("Total Savings")
    plt.tight_layout()


def predict_expense(data):

    predicted_savings, predicted_expense, predicted_income = predict(data)
    print("Predicted Income:", predicted_income)
    print("Predicted Exepense:", predicted_expense)
    print("Predicted Savings:", predicted_savings)


def main():

    keep_continue = True

    while keep_continue:
        option = str(input("\nOptions: [1] Add Transaction [2] Summary [3] Plot [4] Predict Expense  [5] Exit [6] Show dashboard \n -> "))

        if option == str(1):
            add_transactions(data)

        elif option == str(2):
            summary()

        elif option == str(3):
            plot_graph()

        elif option == str(4):
            predict_expense(data)

        elif option == str(5):
            keep_continue = False

        elif option == str(6):
            summary()
            plot_graph_()
            plt.savefig(save_path, format='jpg', dpi=150)
            plt.close()
            predict_expense(data)
            keep_continue = False

            host.start_flask_app()

main()
