print(">>> Running run.py...")
from app import create_app

app = create_app()

if __name__ == "__main__":
    print(">>> Running Flask App...")
    app.run(debug=True, host="0.0.0.0", port=5000)