from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__) #créer l'app Flask    

    #configuration de l'URI de la bd
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mabd_stress.db'
    #configuration de la clé secrete
    app.config['SECRET_KEY']='une-cle-secrete'


    #connecter db à app
    db.init_app(app)

    #importer et enregistrer le blueprint main depuuis routes.py
    from .routes import main

    app.register_blueprint(main)

    return app