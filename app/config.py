import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# Cargar variables desde el archivo .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY no está configurada en el archivo .env")

    # Configuración de la base de datos MySQL
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "fnapdb")
    DEFAULT_USERNAME = os.getenv("DEFAULT_USERNAME")
    DEFAULT_PASSWORD = os.getenv("DEFAULT_PASSWORD")

    # Cadena de conexión para SQLAlchemy
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Configuración de la carpeta de subida de archivos
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # Configuración de SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Crear el motor de la base de datos
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

    # Crear una sesión de la base de datos
    db_session = scoped_session(sessionmaker(bind=engine))