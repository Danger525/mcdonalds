
from flask import Flask
print("Flask imported")
app = Flask(__name__)

@app.route('/')
def home():
    return "Minimal Server Works"

if __name__ == '__main__':
    print("Starting minimal server...")
    try:
        app.run(port=5001)
    except Exception as e:
        print(f"Error: {e}")
