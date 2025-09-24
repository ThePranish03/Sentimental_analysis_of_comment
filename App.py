from flask import Flask, render_template, request, redirect, url_for

# The template_folder argument tells Flask where to find your HTML files.
app = Flask(__name__, template_folder='Tempelates')

# A simple "database" for demonstration purposes. In a real app,
# you would connect to a proper database.
users = {
    'test@example.com': 'password123'
}

# --- Main Website Routes ---

@app.route('/')
def home():
    """Renders the main home page."""
    return render_template('home.htm')

@app.route('/product')
def product():
    """Renders the product page (a placeholder for now)."""
    return "This is the Product Page."

@app.route('/services')
def services():
    """Renders the services page (a placeholder for now)."""
    return "This is the Services Page."

@app.route('/contact')
def contact():
    """Renders the contact page (a placeholder for now)."""
    return "This is the Contact Page."

# --- User & Legal Routes ---

# This route now handles both GET and POST requests
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Renders the login page and handles login form submission."""
    if request.method == 'POST':
        # Get data from the submitted form. The input name in login.htm is email and password.
        email = request.form.get('email')
        password = request.form.get('password')

        # Check for valid credentials (simple check against the 'users' dictionary)
        if email in users and users[email] == password:
            # If login is successful, redirect to the user-dashboard page
            return redirect(url_for('user_dashboard'))
        else:
            # If login fails, render the login page again with an error message
            error = 'Invalid email or password. Please try again.'
            return render_template('login.htm', error=error)
            
    # For a GET request, just render the login page
    return render_template('login.htm')

# This route now handles both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Renders the registration page and handles form submission."""
    if request.method == 'POST':
        # Get data from the submitted form fields.
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        organization = request.form.get('organization')
        password = request.form.get('password')

        # In a real-world application, you would add validation and save this data to a database.
        # For this example, we'll just add the new user to our dictionary.
        if email not in users:
            users[email] = password
            # After successful registration, redirect the user to the dashboard.
            return redirect(url_for('user_dashboard'))
        else:
            # Handle case where user already exists.
            error = 'This email is already registered.'
            return render_template('registerrr.htm', error=error)
    
    # For a GET request (when the page is first loaded), just render the template.
    return render_template('register.htm')  # Matches your file name `registerrr.htm`

@app.route('/terms')
def terms():
    """Renders the Terms of Service page."""
    return render_template('termsofservice.htm')

@app.route('/privacy')
def privacy():
    """Renders the Privacy Policy page."""
    return render_template('policy_privacy.htm')

@app.route('/user-dashboard')
def user_dashboard():
    """Renders the user dashboard page."""
    return render_template('user-dashboard.htm')

if __name__ == '__main__':
    app.run(debug=True)