from flask import Flask, render_template, request, redirect, url_for
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime
import os
import requests
from werkzeug.utils import secure_filename

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home page - show products

@app.route('/add-sale', methods=['GET', 'POST'])
def add_sale():
    if request.method == 'POST':
        product = request.form['product']
        amount = float(request.form['amount'])

        # Handle image upload
        receipt_url = None
        if 'receipt' in request.files:
            file = request.files['receipt']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                receipt_url = f"/static/uploads/{filename}"

        supabase.table("sales").insert({
            "product": product,
            "amount": amount,
            "receipt_url": receipt_url
        }).execute()

        return redirect(url_for('dashboard'))

    return render_template("add_sale.html")


@app.route('/add-expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        description = request.form['description']
        amount = float(request.form['amount'])
        receipt_file = request.files.get('receipt')

        receipt_url = None
        if receipt_file and receipt_file.filename:
            filename = secure_filename(receipt_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            receipt_file.save(file_path)
            receipt_url = url_for('static', filename='uploads/' + filename, _external=True)

        # Insert into Supabase
        expense_data = {
            'description': description,
            'amount': amount,
            'receipt_url': receipt_url
        }
        supabase.table('expenses').insert(expense_data).execute()
        return redirect(url_for('dashboard'))

    return render_template('add_expense.html')


@app.route('/', methods=['GET', 'POST'])
def dashboard():
    # Optional: Use request.args or request.form to get filter inputs
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    sales_query = supabase.table('sales')
    expenses_query = supabase.table('expenses')

    if start_date and end_date:
        sales_query = sales_query.gte('date', start_date).lte('date', end_date)
        expenses_query = expenses_query.gte('date', start_date).lte('date', end_date)

    sales_data = sales_query.select('*').execute().data
    expense_data = expenses_query.select('*').execute().data

    return render_template('dashboard.html', sales=sales_data, expenses=expense_data)



if __name__ == '__main__':
    app.run(debug=True)

