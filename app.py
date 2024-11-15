from modules.browser import launch_secure_browser

if __name__ == "__main__":
    launch_secure_browser()

from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_talisman import Talisman
from modules.vpn import connect_vpn, disconnect_vpn, VPN_PROVIDERS
from modules.dns_encryption import setup_dns, apply_tracker_blocking
from modules.email_manager import generate_disposable_email
from modules.password_manager import save_password, retrieve_password
from modules.user import User

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Replace with a secure key
Talisman(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

# Simulated User Database
users = {
    "admin": User(id=1, username="admin", password="password123")
}

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.id == int(user_id):
            return user
    return None

# Routes
@app.before_request
def redirect_https():
    if request.is_secure:
        url = request.url.replace("https://", "http://", 1)
        return redirect(url, code=301)

@app.route('/')
def index():
    return "Welcome to the Secure Browser!"

@app.route('/favicon.ico')
def favicon():
    return '', 204  # Return no content for favicon requests

@app.route('/')
@login_required
def dashboard():
    return render_template("dashboard.html", username=current_user.username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/vpn', methods=['GET', 'POST'])
@login_required
def vpn_module():
    if request.method == 'POST':
        action = request.form.get('action')
        provider = request.form.get('provider')
        if action == 'connect' and provider:
            status = connect_vpn(provider)
        elif action == 'disconnect':
            status = disconnect_vpn()
        else:
            status = "Invalid action or provider not selected."
        return jsonify({"status": status})
    return render_template("vpn.html", providers=VPN_PROVIDERS.keys())

@app.route('/browser', methods=['GET', 'POST'])
@login_required
def launch_browser():
    if request.method == 'POST':
        from modules.browser import launch_secure_browser
        try:
            launch_secure_browser()
        except Exception as e:
            return f"Error launching secure browser: {e}", 500
    return render_template("browser.html", message="Click 'Launch Browser' to start the secure browser.")

@app.route('/dns', methods=['POST'])
@login_required
def dns_module():
    provider = request.form.get("dns_provider", "Cloudflare")
    result = setup_dns(provider)
    return jsonify({"status": result})

@app.route('/block_trackers', methods=['POST'])
@login_required
def block_trackers():
    result = apply_tracker_blocking()
    return jsonify({"status": result})

@app.route('/email', methods=['GET'])
@login_required
def email_module():
    email = generate_disposable_email()
    return jsonify({"disposable_email": email})

@app.route('/password_manager', methods=['GET', 'POST'])
@login_required
def password_manager():
    if request.method == 'POST':
        account = request.form.get('account')
        password = request.form.get('password')
        save_password(account, password)
        return jsonify({"status": "Password saved successfully"})
    return render_template("password_manager.html")

@app.route('/retrieve_password', methods=['POST'])
@login_required
def retrieve_password_route():
    account = request.form.get('account')
    password = retrieve_password(account)
    return jsonify({"account": account, "password": password})

if __name__ == '__main__':
    app.run(port=5050, debug=True, ssl_context=('cert.pem', 'key.pem'))
