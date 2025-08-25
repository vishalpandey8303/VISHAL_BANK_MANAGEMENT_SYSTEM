from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",         # Use your MySQL username
        password="",         # Your MySQL password
        database="bank_system"
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        name = request.form['name']
        balance = request.form['balance']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO accounts (name, balance) VALUES (%s, %s)", (name, balance))
        conn.commit()
        conn.close()
        return redirect('/view')
    return render_template('create_account.html')

@app.route('/view')
def view_accounts():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts")
    accounts = cursor.fetchall()
    conn.close()
    return render_template('view_accounts.html', accounts=accounts)

@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if request.method == 'POST':
        acc_id = request.form['id']
        amount = float(request.form['amount'])
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE accounts SET balance = balance + %s WHERE id = %s", (amount, acc_id))
        conn.commit()
        conn.close()
        return redirect('/view')
    return render_template('deposit.html')

@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if request.method == 'POST':
        acc_id = request.form['id']
        amount = float(request.form['amount'])
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE id = %s", (acc_id,))
        current = cursor.fetchone()
        if current and current[0] >= amount:
            cursor.execute("UPDATE accounts SET balance = balance - %s WHERE id = %s", (amount, acc_id))
            conn.commit()
        conn.close()
        return redirect('/view')
    return render_template('withdraw.html')

if __name__ == '__main__':
    app.run(debug=True)
