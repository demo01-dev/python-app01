import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Use a secure secret key for session management
app.secret_key = os.environ.get('SECRET_KEY', 'default-super-secret-key-change-in-production')

# Mock database of users with hashed passwords
# username: admin, password: password123
USERS = {
    "admin": {
        "username": "admin",
        "name": "Administrador",
        "password_hash": generate_password_hash("password123")
    },
    "usuario": {
        "username": "usuario",
        "name": "Usuario Demo",
        "password_hash": generate_password_hash("demo2026")
    }
}

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Simple validation
        if not username or not password:
            flash('Por favor, rellena todos los campos.', 'danger')
            return render_template('login.html', username=username)
            
        user = USERS.get(username)
        if user and check_password_hash(user['password_hash'], password):
            session['user'] = {
                'username': user['username'],
                'name': user['name']
            }
            flash(f'¡Bienvenido de nuevo, {user["name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
            return render_template('login.html', username=username)
            
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash('Debes iniciar sesión para acceder al panel.', 'warning')
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=session['user'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Run locally
    app.run(host='0.0.0.0', port=5000, debug=True)
