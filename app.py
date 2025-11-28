from flask import Flask, request, jsonify
from services.user_service import UserService
from repositories.postgres_user_repo import PostgresUserRepository
import traceback

app = Flask(__name__)

# Инициализация зависимостей
repo = PostgresUserRepository()
service = UserService(repo)

@app.route('/health')
def health():
    return {"status": "ok"}

@app.route('/users', methods=['POST'])
def register_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
        
    try:
        user = service.register_user(data['name'], data['email'])
        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at.isoformat()
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print("=== ERROR DETAILS ===")
        print(traceback.format_exc())
        print("=====================")
        return jsonify({"error": f"Internal error: {str(e)}"}), 500

@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = service.list_all_users()
        return jsonify([{
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "created_at": u.created_at.isoformat()
        } for u in users])
    except Exception as e:
        print("=== ERROR DETAILS ===")
        print(traceback.format_exc())
        print("=====================")
        return jsonify({"error": f"Internal error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)