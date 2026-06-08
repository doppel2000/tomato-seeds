import os
import shutil
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    # REPERTOIRE DE DONNÉES DÉDIÉ
    db_dir = "/home/nonroot/data"
    db_path = os.path.join(db_dir, "tomato_seeds.db")  
    tmp_db_path = "/tmp/instance/tomato_seeds.db"

    # Python crée le dossier s'il n'existe pas -> Droits parfaits pour nonroot !
    if not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)

    # Initialisation de la DB dans le volume s'il est vide
    if not os.path.exists(db_path) or os.path.getsize(db_path) == 0:
        if os.path.exists(tmp_db_path):
            shutil.copy2(tmp_db_path, db_path)
            print("Base de données tomato_seeds.db initialisée avec succès !")
        else:
            print(f"Erreur critique : {tmp_db_path} est introuvable.")

    # Simple default config
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', 'dev-key-tomato-seeds'),
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', f'sqlite:///{db_path}'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # Initialize extensions
    from app.extensions import db, migrate
    db.init_app(app)

    # Import models to register them with metadata
    from app.models.tomato import TomatoVariety, Person

    migrate.init_app(app, db)

    # Register blueprints
    from app.blueprints.main import main_bp
    app.register_blueprint(main_bp)

    return app
