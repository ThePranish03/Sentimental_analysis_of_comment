from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__, template_folder='Tempelates')
app.secret_key = 'supersecretkey'

# --- Database connection ---
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Oracle@25",
    database="sih_project"
)
cursor = db.cursor(dictionary=True)

# --- Ensure admin exists (stored only once) ---
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin123"  # Set admin password here

cursor.execute("SELECT * FROM Users WHERE email = %s", (ADMIN_EMAIL,))
if not cursor.fetchone():
    hashed_admin_password = generate_password_hash(ADMIN_PASSWORD)
    cursor.execute(
        "INSERT INTO Users (name, email, password_hash, role) VALUES (%s, %s, %s, %s)",
        ("Admin", ADMIN_EMAIL, hashed_admin_password, "admin")
    )
    db.commit()
    print("Admin user created with email:", ADMIN_EMAIL)

# --- Routes ---
@app.route('/')
def home():
    return render_template('home.htm')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Only check email here, ignore role selection
        cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password_hash'], password):
            # Save session
            session['user_id'] = user['user_id']
            session['user_role'] = user['role']
            session['user_name'] = user['name']

            # Redirect based on role
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            error = 'Invalid email or password.'
            return render_template('login.htm', error=error)
    return render_template('login.htm')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        name = f"{first_name} {last_name}".strip()
        email = request.form.get('email')
        password = request.form.get('password')
        role = 'public'  # Only public users can register

        if not name or not email or not password:
            error = "All fields are required!"
            return render_template('register.htm', error=error)

        # Check if email already exists
        cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
        if cursor.fetchone():
            error = "This email is already registered."
            return render_template('register.htm', error=error)

        # Hash password before saving
        hashed_password = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO Users (name, email, password_hash, role) VALUES (%s, %s, %s, %s)",
            (name, email, hashed_password, role)
        )
        db.commit()
        return redirect(url_for('login'))
    return render_template('register.htm')

@app.route('/admin-dashboard')
def admin_dashboard():
    if 'user_role' in session and session['user_role'] == 'admin':
        cursor.execute("SELECT * FROM Policies")
        policies = cursor.fetchall()
        return render_template('admin_dashboard.htm', name=session['user_name'], policies=policies)
    return redirect(url_for('login'))

@app.route('/user-dashboard')
def user_dashboard():
    if 'user_role' in session and session['user_role'] != 'admin':
        return render_template('user_dashboard.htm', name=session['user_name'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- Run App ---
if __name__ == '__main__':
    app.run(debug=True)
