from flask import Flask, render_template
import pandas as pd
from MachineLearning import predict
import webbrowser

app = Flask(__name__)
FILE = "tracker.csv"
GRAPH_PATH = "static/images/img.jpg"

@app.route("/")

def dashboard():
    data = pd.read_csv(FILE)
    total_income = data[data['Type']=='Income']['Amount'].sum()
    total_expense = data[data['Type']=='Expense']['Amount'].sum()
    net_savings = total_income - total_expense
    last_20 = data.tail(20).to_dict(orient='records')
    predicted_savings, predicted_expense, predicted_income = predict(data)

    return render_template("main.html",
                           total_income=total_income,
                           total_expense=total_expense,
                           net_savings=net_savings,
                           predicted_income=round(predicted_income,2),
                           predicted_expense=round(predicted_expense,2),
                           predicted_savings=round(predicted_savings,2),
                           graph_file=GRAPH_PATH,
                           last_20=last_20)




def start_flask_app():
    import webbrowser, threading
    threading.Thread(target=lambda: app.run(debug=True, use_reloader=False)).start()
    webbrowser.open("http://127.0.0.1:5000/")