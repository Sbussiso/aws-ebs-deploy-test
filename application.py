import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import psycopg2

# Load environment variables from .env file
load_dotenv()

application = Flask(__name__)

# Database configuration
application.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASS']}@"
    f"{os.environ['DB_HOST']}/{os.environ['DB_NAME']}"
)
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(application)

# Define the Transaction model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(255), nullable=False)
    command = db.Column(db.String(255), nullable=False)
    refnum = db.Column(db.String(255), nullable=False)

@application.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        card = request.form.get("card")
        amount = request.form.get("amount")
        date = request.form.get("date")
        command = request.form.get("command")
        refnum = request.form.get("card")

        # Create a new transaction record
        transaction = Transaction(
            card=card, 
            amount=amount, 
            date=date, 
            command=command, 
            refnum=refnum
        )

        # Save the transaction to the database
        db.session.add(transaction)
        db.session.commit()

        return render_template("form2.html", response=transaction)

    return render_template("form.html")

if __name__ == "__main__":
    application.run(debug=True, host="0.0.0.0", port=5000)
