import webview
from threading import Thread
from flask import Flask, jsonify

# Flask app
app = Flask(__name__)

@app.route('/browser', methods=['POST'])
def secure_browser():
    """
    Flask endpoint to trigger the secure browser.
    """
    try:
        print("Trigger received to launch the browser...")
        window.load_url("https://example.com")  # Update the URL dynamically
        return jsonify({"status": "success", "message": "Browser launching..."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

def launch_flask():
    """
    Start the Flask app on a specified port.
    """
    print("Starting Flask app...")
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False, threaded=True)

def launch_secure_browser():
    """
    Initialize the secure browser and start Flask in a background thread.
    """
    # Create the browser window on the main thread
    print("Initializing secure browser...")
    global window
    window = webview.create_window("Secure Browser", "about:blank")  # Blank until loaded

    # Start Flask in a background thread
    flask_thread = Thread(target=launch_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Start the PyWebView loop in the main thread
    print("Starting webview...")
    webview.start(gui='qt')  # Ensure the correct backend is installed

if __name__ == "__main__":
    launch_secure_browser()
