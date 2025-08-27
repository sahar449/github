from flask import Flask, jsonify
import mysql.connector
import os
import time

app = Flask(__name__)

# משתני סביבה (שומרים את השם MYSQL_ROOT_PASSWORD כמו שביקשת)
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('MYSQL_ROOT_PASSWORD', 'rootpass')
DB_NAME = os.environ.get('DB_NAME', 'flaskdb')


def init_db():
    """יוצר טבלה ומכניס נתונים ראשוניים"""
    try:
        with mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        ) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(50) UNIQUE NOT NULL
                )
            """)
            names = ['Sahar', 'Moshe', 'David', 'Yakov', 'Alex']
            for name in names:
                cursor.execute(
                    "INSERT IGNORE INTO users (name) VALUES (%s)", (name,)
                )
            conn.commit()
    except Exception as e:
        print(f"DB init error: {e}")
        raise


@app.route("/")
def list_users():
    """מחזיר רשימת משתמשים"""
    try:
        with mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        ) as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    """בדיקת liveness"""
    return jsonify({"status": "ok"}), 200


@app.route("/ready")
def ready():
    """בדיקת readiness (בודק חיבור ל־DB)"""
    try:
        mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        ).close()
        return jsonify({"ready": True}), 200
    except Exception as e:
        return jsonify({"ready": False, "error": str(e)}), 503


if __name__ == "__main__":
    # ממתין קצת כדי לאפשר ל־MySQL לעלות
    time.sleep(5)
    try:
        init_db()
        print("Database initialized successfully")
    except Exception as e:
        print(f"DB init error: {e}")
    app.run(host="0.0.0.0", port=5000)
