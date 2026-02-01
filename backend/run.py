import os
import sys

print("Run.py started")

try:
    from app import create_app
    print("App Factory imported")

    config_name = os.getenv('FLASK_CONFIG') or 'default'
    app = create_app(config_name)
    print(f"App created with config: {config_name}")

    if __name__ == '__main__':
        print("Starting Flask server...")
        # socketio.run(app, debug=True, port=5000)
        app.run(debug=True, port=5000) # Fallback to standard Flask
except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    import traceback
    traceback.print_exc()
