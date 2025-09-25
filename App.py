from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__, template_folder='Tempelates')
app.secret_key = 'supersecretkey'

# --- Admin Credentials (Only these can access admin dashboard) ---
ADMIN_EMAIL = "parthkahane44@gmail.com"
ADMIN_PASSWORD = "P@rthk24"  # Consider moving to environment variables for production

# --- Database connection ---
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="P@rthk24",
    database="sih_project"
)
cursor = db.cursor(dictionary=True)

# --- Ensure admin exists in database ---
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

        # Check if credentials match the specific admin (case-insensitive email)
        if email.lower().strip() == ADMIN_EMAIL.lower() and password == ADMIN_PASSWORD:
            # Admin login - set admin session
            cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
            admin_user = cursor.fetchone()
            
            session['user_id'] = admin_user['user_id']
            session['user_role'] = 'admin'
            session['user_name'] = admin_user['name']
            
            return redirect(url_for('admin_dashboard'))
        
        # For all other users (including wrong admin credentials)
        cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password_hash'], password):
            # Valid user but not admin - redirect to user dashboard
            session['user_id'] = user['user_id']
            session['user_role'] = 'public'  # Force role to public for non-admin
            session['user_name'] = user['name']
            
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
        
        # Prevent registration with admin email (case-insensitive)
        if email.lower().strip() == ADMIN_EMAIL.lower():
            error = "This email is reserved and cannot be used for registration."
            return render_template('register.htm', error=error)

        if not name or not email or not password:
            error = "All fields are required!"
            return render_template('register.htm', error=error)

        # Check if email already exists
        cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
        if cursor.fetchone():
            error = "This email is already registered."
            return render_template('register.htm', error=error)

        # Hash password before saving - all registered users are 'public'
        hashed_password = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO Users (name, email, password_hash, role) VALUES (%s, %s, %s, %s)",
            (name, email, hashed_password, 'public')
        )
        db.commit()
        return redirect(url_for('login'))
        
    return render_template('register.htm')

@app.route('/admin-dashboard')
def admin_dashboard():
    # Double check: session role must be admin AND current session user must be the specific admin
    if ('user_role' in session and 
        session['user_role'] == 'admin' and 
        'user_id' in session):
        
        # Additional verification: check if the logged-in user is actually the admin
        cursor.execute("SELECT * FROM Users WHERE user_id = %s AND email = %s", 
                      (session['user_id'], ADMIN_EMAIL))
        admin_user = cursor.fetchone()
        
        if admin_user:
            cursor.execute("SELECT * FROM Policies")
            policies = cursor.fetchall()
            return render_template('admin_dashboard.htm', name=session['user_name'], policies=policies)
    
    # If not proper admin, redirect to user dashboard or login
    if 'user_id' in session:
        return redirect(url_for('user_dashboard'))
    else:
        return redirect(url_for('login'))

@app.route('/user-dashboard')
def user_dashboard():
    if 'user_id' in session:
        # Even if someone has admin role but isn't the specific admin, treat as regular user
        cursor.execute("SELECT * FROM Users WHERE user_id = %s", (session['user_id'],))
        user = cursor.fetchone()
        
        if user and user['email'] == ADMIN_EMAIL:
            # If somehow the admin ended up here, redirect to admin dashboard
            return redirect(url_for('admin_dashboard'))
            
        return render_template('user_dashboard.htm', name=session['user_name'])
    
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- Run App ---
if __name__ == '__main__':
    app.run(debug=True)