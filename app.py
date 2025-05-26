import os
from flask import Flask, render_template, request, redirect, url_for, flash
from supabase import create_client, Client
from werkzeug.utils import secure_filename
from datetime import datetime
from dotenv import load_dotenv  # <-- Add this import

load_dotenv()  # <-- This loads variables from .env into os.environ

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "fallback-secret-key")

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
app.config['UPLOAD_FOLDER'] = "uploads"
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
SUPABASE_TABLE = "transactions"  # Replace with your actual table name
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/", methods=["GET"])
def index():
    transactions = supabase.table(SUPABASE_TABLE).select("*").execute().data
    return render_template("index.html", transactions=transactions)
@app.route("/dashboard")
def dashboard():
    # Fetch all transactions from Supabase
    res = supabase.table("transactions").select("*").execute()
    if not res.data:
        products = []
    else:
        transactions = res.data
        # Group by product
        product_dict = {}
        for tr in transactions:
            product = tr.get("product", "Unknown")
            if product not in product_dict:
                product_dict[product] = {"transactions": [], "total_sale": 0, "total_expense": 0}
            product_dict[product]["transactions"].append(tr)
            if tr["type"] == "sale":
                product_dict[product]["total_sale"] += tr.get("amount", 0) or 0
            elif tr["type"] == "expense":
                product_dict[product]["total_expense"] += tr.get("amount", 0) or 0

        # Prepare product list with profit/loss calculation
        products = []
        for product, info in product_dict.items():
            profit = info["total_sale"] - info["total_expense"]
            products.append({
                "name": product,
                "transactions": info["transactions"],
                "total_sale": info["total_sale"],
                "total_expense": info["total_expense"],
                "profit": profit,
                "status": "Profit" if profit > 0 else ("Break-even" if profit == 0 else "Loss"),
            })

    return render_template("dashboard.html", products=products)

@app.route('/add-transaction', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        trans_type = request.form.get('type')
        description = request.form.get('description', '')
        amount = request.form.get('amount', '')
        date = request.form.get('date', '')
        voice_text = request.form.get('voice_text', '')
        receipt_url = None

        # Save uploaded image if provided
        if 'receipt' in request.files:
            file = request.files['receipt']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                receipt_url = filepath

        # Prepare data for Supabase
        data = {
            "type": trans_type,
            "product": description, 
            "description": description,
            "amount": float(amount) if amount else None,
            "date": date,
            "voice_text": voice_text if voice_text else None,
            "receipt_url": receipt_url
        }
        res = supabase.table(SUPABASE_TABLE).insert(data).execute()
        if res.data:
            flash("Transaction saved!", "success")
        else:
            flash(f"Error saving: {res.error}", "danger")
        return redirect(url_for('add_transaction'))

    return render_template('add_transaction.html')
@app.route('/delete-transaction/<id>', methods=['POST'])
def delete_transaction(id):
    res = supabase.table("transactions").delete().eq("id", id).execute()
    if res.data is not None:  # Success if .data is a list/dict
        flash("Transaction deleted!", "success")
    else:
        flash("Failed to delete transaction.", "danger")
    return redirect(request.referrer or url_for('dashboard'))
if __name__ == '__main__':
    app.run(debug=True)