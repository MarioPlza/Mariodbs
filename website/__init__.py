from flask import Flask

def create_app():
    app = Flask(__name__)
    #Secure cookies and sesion data
    app.config['SECRET_KEY']='adsaFGFAGGASSfd'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    return app

