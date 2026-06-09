from flask import Flask
from database.db import init_db

from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.admin_routes import admin_bp
from routes.interview_routes import interview_bp
from routes.api_routes import api_bp

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "secret123"

init_db()

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(interview_bp)
app.register_blueprint(api_bp)

@app.route("/test")
def test():
    return "App is working"

if __name__ == "__main__":
    app.run(debug=True)