from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import sqlite3
from database import get_db_connection, init_db
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize database on startup
init_db()

# Helper function to check if user is logged in
def is_logged_in():
    return 'user_id' in session

# Helper function to require login
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    if is_logged_in():
        return redirect(url_for('dashboard'))
    return render_template("index.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')
        
        # Hash the password
        password_hash = generate_password_hash(password)
        
        # Insert into database
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                (username, email, password_hash)
            )
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists.', 'danger')
            return render_template('register.html')
        finally:
            conn.close()
    
    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and password are required.', 'danger')
            return render_template('login.html')
        
        # Query database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route("/logout")
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route("/dashboard")
@login_required
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM events WHERE user_id = ? ORDER BY due_date ASC',
        (session['user_id'],)
    )
    events = cursor.fetchall()
    conn.close()
    
    return render_template('dashboard.html', events=events)

@app.route("/event/create", methods=['GET', 'POST'])
@login_required
def create_event():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        location = request.form.get('location')
        due_date = request.form.get('due_date')
        status = request.form.get('status', 'pending')
        
        if not title or not due_date:
            flash('Title and due date are required.', 'danger')
            return render_template('create_event.html')
        
        # Insert event into database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO events (user_id, title, description, location, due_date, status)
               VALUES (?, ?, ?, ?, ?, ?)''',
            (session['user_id'], title, description, location, due_date, status)
        )
        conn.commit()
        conn.close()
        
        flash('Event created successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('create_event.html')

@app.route("/event/<int:event_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        location = request.form.get('location')
        due_date = request.form.get('due_date')
        status = request.form.get('status')
        
        if not title or not due_date:
            flash('Title and due date are required.', 'danger')
            return redirect(url_for('edit_event', event_id=event_id))
        
        cursor.execute(
            '''UPDATE events 
               SET title = ?, description = ?, location = ?, due_date = ?, status = ?, updated_at = CURRENT_TIMESTAMP
               WHERE id = ? AND user_id = ?''',
            (title, description, location, due_date, status, event_id, session['user_id'])
        )
        conn.commit()
        conn.close()
        
        flash('Event updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    # GET request - fetch event details
    cursor.execute('SELECT * FROM events WHERE id = ? AND user_id = ?', (event_id, session['user_id']))
    event = cursor.fetchone()
    conn.close()
    
    if not event:
        flash('Event not found.', 'danger')
        return redirect(url_for('dashboard'))
    
    return render_template('edit_event.html', event=event)

@app.route("/event/<int:event_id>/delete", methods=['POST'])
@login_required
def delete_event(event_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM events WHERE id = ? AND user_id = ?', (event_id, session['user_id']))
    conn.commit()
    conn.close()
    
    flash('Event deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    # Only enable debug mode in development
    # In production, use a WSGI server like gunicorn
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode)
