from flask import Flask
from flask_jwt_extended import JWTManager
from .db import db, init_db
from .auth import bp as auth_bp
from .api import bp as api_bp
from .admin import bp as admin_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

init_db(app)
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(api_bp)
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    app.run(port=4000, debug=True)
