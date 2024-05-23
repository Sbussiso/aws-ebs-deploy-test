import json
from flask import Flask, render_template, request

application = Flask(__name__)

@application.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        card = request.form.get("card")
        amount = request.form.get("amount")
        date = request.form.get("date")
        command = request.form.get("command")
        refnum = request.form.get("card")

        transactions = {
            "card": card, 
            "amount": amount, 
            "date": date, 
            "command": command, 
            "refnum": refnum
        }

        # Save the transaction details to a JSON file
        with open("transactions.json", "a") as f:
            json.dump(transactions, f)
            f.write("\n")  # Write each transaction on a new line

        return render_template("form2.html", response=transactions)

    return render_template("form.html")

if __name__ == "__main__":
    application.run(debug=True, host="0.0.0.0", port=5000)
