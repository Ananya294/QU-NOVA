from flask import Flask
from backend.config import Config
from backend.extensions import db, login_manager, bcrypt
from backend.models.user import User
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    @login_manager.user_loader                #flask-login finds user id from session cookie
    def load_user(user_id):                   #<- calls this function
        return User.query.get(int(user_id))   #query db to retrieve user object; result -> current_user now populated w/ user object

    #user auth bp
    from backend.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    #file upload bp
    from backend.routes.upload import upload_bp
    app.register_blueprint(upload_bp)

    #mri scan analysis bp
    from backend.routes.analyze import analyze_bp
    app.register_blueprint(analyze_bp)

    #report generation bp
    from backend.routes.report import report_bp
    app.register_blueprint(report_bp)



    return app