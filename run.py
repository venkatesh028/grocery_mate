from flask_jwt_extended import JWTManager

from app import create_app, db

app = create_app()

if __name__ == '__main__':
    app.run(debug=False)  # Disable debug for production
