import os
import random
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables from .env file for local development
if os.getenv('FLASK_ENV') == 'development':
    load_dotenv()

application = Flask(__name__)

# Database configuration
database_url = os.getenv('DATABASE_URL')
if not database_url:
    raise ValueError("No DATABASE_URL set for Flask application")
print(f"Database URL: {database_url}")  # Add this line to debug
application.config['SQLALCHEMY_DATABASE_URI'] = database_url
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

# Create the database tables
with application.app_context():
    db.create_all()

@application.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        card = request.form.get("card")
        amount = request.form.get("amount")
        date = request.form.get("date")
        command = request.form.get("command")
        # Generate a random reference number
        refnum = ''.join(random.choices('0123456789', k=10))  # Generates a 10-digit random number string

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
