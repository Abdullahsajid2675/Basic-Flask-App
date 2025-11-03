# Basic-Flask-App
#

from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_bcrypt import Bcrypt
from forms import UserForm, UpdateForm, RegistrationForm, LoginForm
import secrets
import os
from functools import wraps

app = Flask(__name__)

# Security Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
app.config['WTF_CSRF_TIME_LIMIT'] = 3600  # CSRF token expires in 1 hour
app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent XSS attacks
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # Session expires in 30 minutes

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///firstapp.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

# Login required decorator
def login_required(f):
    """Auto-generated: login_required."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """Auto-generated: decorated_function."""
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

with app.app_context():
    db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def set_password(self, password):
        """Hash and set password using bcrypt"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Check password against hash"""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        """Auto-generated: __repr__."""
        return f"<User {self.username}>"

class Firstapp(db.Model):
    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        """Auto-generated: __repr__."""
        return f"{self.sno} - {self.fname}"

# --- Route: / [methods=GET, POST] ---
@app.route("/", methods=['GET', 'POST'])
@login_required
def hello_world():
    """Auto-generated: hello_world."""
    form = UserForm()
    
    if form.validate_on_submit():
        try:
            # Get validated form data
            fname = form.fname.data.strip()
            lname = form.lname.data.strip()
            email = form.email.data.strip().lower()
            
            # Create new record using parameterized queries (SQLAlchemy ORM handles this)
            new_record = Firstapp(fname=fname, lname=lname, email=email)
            db.session.add(new_record)
            db.session.commit()
            
            flash('Record added successfully!', 'success')
            return redirect('/')
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while adding the record. Please try again.', 'error')
            app.logger.error(f'Database error: {str(e)}')
    
    # Display form validation errors
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field.title()}: {error}', 'error')
    
    # Get all records from database using parameterized queries
    try:
        allRecords = Firstapp.query.all()
    except Exception as e:
        allRecords = []
        flash('Error loading records from database.', 'error')
        app.logger.error(f'Database query error: {str(e)}')
    
    return render_template('index.html', form=form, allRecords=allRecords)

# --- Route: /home [methods=GET] ---
@app.route('/home')
@login_required
def home():
    """Auto-generated: home."""
    return 'Welcome to the Home Page'

# --- Route: /register [methods=GET, POST] ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Auto-generated: register."""
    form = RegistrationForm()
    
    if form.validate_on_submit():
        try:
            # Check if username or email already exists
            existing_user = User.query.filter(
                (User.username == form.username.data) | 
                (User.email == form.email.data)
            ).first()
            
            if existing_user:
                if existing_user.username == form.username.data:
                    flash('Username already exists. Please choose a different one.', 'error')
                else:
                    flash('Email already registered. Please use a different email.', 'error')
                return render_template('auth/register.html', form=form)
            
            # Create new user with hashed password
            user = User(
                username=form.username.data.strip(),
                email=form.email.data.strip().lower()
            )
            user.set_password(form.password.data)
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! You can now log in.', 'success')
            return redirect('/login')
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'error')
            app.logger.error(f'Registration error: {str(e)}')
    
    # Display form validation errors
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field.title()}: {error}', 'error')
    
    return render_template('auth/register.html', form=form)

# --- Route: /login [methods=GET, POST] ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Auto-generated: login."""
    form = LoginForm()
    
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            
            if user and user.check_password(form.password.data):
                session['user_id'] = user.id
                session['username'] = user.username
                session.permanent = True
                flash('Login successful!', 'success')
                # Redirect to the page they were trying to access, or home
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect('/')
            else:
                flash('Invalid username or password.', 'error')
                
        except Exception as e:
            flash('An error occurred during login. Please try again.', 'error')
            app.logger.error(f'Login error: {str(e)}')
    
    # Display form validation errors
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field.title()}: {error}', 'error')
    
    return render_template('auth/login.html', form=form)

# --- Route: /logout [methods=GET] ---
@app.route('/logout')
def logout():
    """Auto-generated: logout."""
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect('/login')

# --- Route: /welcome [methods=GET] ---
@app.route('/welcome')
def welcome():
    """Public welcome page"""
    if 'user_id' in session:
        return redirect('/')
    return render_template('welcome.html')

# --- Route: /public [methods=GET] ---
@app.route('/public')
def public_landing():
    """Public landing page for unauthenticated users"""
    return render_template('welcome.html')

# --- Route: /delete/<int:sno> [methods=POST] ---
@app.route('/delete/<int:sno>', methods=['POST'])
@login_required
def delete(sno):
    """Auto-generated: delete."""
    try:
        # Find the record by serial number using parameterized query
        record = Firstapp.query.filter_by(sno=sno).first()
        if record:
            db.session.delete(record)
            db.session.commit()
            flash('Record deleted successfully!', 'success')
        else:
            flash('Record not found.', 'error')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the record.', 'error')
        app.logger.error(f'Delete error: {str(e)}')
    
    return redirect('/')

# --- Route: /update/<int:sno> [methods=GET, POST] ---
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
@login_required
def update(sno):
    """Auto-generated: update."""
    # Get the record to update using parameterized query
    try:
        record = Firstapp.query.filter_by(sno=sno).first()
        if not record:
            flash('Record not found.', 'error')
            return redirect('/')
    except Exception as e:
        flash('Error accessing record.', 'error')
        app.logger.error(f'Database access error: {str(e)}')
        return redirect('/')
    
    form = UpdateForm(obj=record)
    
    if form.validate_on_submit():
        try:
            # Get validated form data
            record.fname = form.fname.data.strip()
            record.lname = form.lname.data.strip()
            record.email = form.email.data.strip().lower()
            
            db.session.commit()
            flash('Record updated successfully!', 'success')
            return redirect('/')
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the record.', 'error')
            app.logger.error(f'Update error: {str(e)}')
    
    # Display form validation errors
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field.title()}: {error}', 'error')
    
    return render_template('update.html', form=form, record=record)

# Error Handlers for Security Practice 4
# --- Error Handler for 404 ---
@app.errorhandler(404)
def not_found_error(error):
    """Auto-generated: not_found_error."""
    return render_template('errors/404.html'), 404

# --- Error Handler for 500 ---
@app.errorhandler(500)
def internal_error(error):
    """Auto-generated: internal_error."""
    db.session.rollback()
    return render_template('errors/500.html'), 500

# --- Error Handler for 403 ---
@app.errorhandler(403)
def forbidden_error(error):
    """Auto-generated: forbidden_error."""
    return render_template('errors/403.html'), 403

# --- Error Handler for 400 ---
@app.errorhandler(400)
def bad_request_error(error):
    """Auto-generated: bad_request_error."""
    return render_template('errors/400.html'), 400

# CSRF Error Handler
# --- Error Handler for CSRFError ---
@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    """Auto-generated: handle_csrf_error."""
    flash('CSRF token missing or invalid. Please try again.', 'error')
    if 'user_id' in session:
        return redirect(request.referrer or '/')
    else:
        return redirect('/login')

if __name__ == "__main__":
    # Disable debug mode in production for security
    app.run(debug=False, host='127.0.0.1', port=5000)
# === End of reworked file ===
