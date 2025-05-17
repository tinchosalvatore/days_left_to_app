from flask import Flask
from dotenv import load_dotenv
from db import db
import os

load_dotenv()


app = Flask(
    __name__,
    static_folder='../frontend/static',
    template_folder='../frontend/templates'
    )

# Cargar variables de entorno   

database_path = os.getenv('DATABASE_PATH', '')
database_name = os.getenv('DATABASE_NAME', '')

os.makedirs(database_path, exist_ok=True)  # Asegura que la carpeta exista

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(database_path, database_name)}"

db.init_app(app)

from routes import *  # Importa rutas después de configurar app y db

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))