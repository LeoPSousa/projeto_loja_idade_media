# config.py
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    """Configurações base (comuns a todos os ambientes)."""
    SECRET_KEY = os.getenv("SECRET_KEY", "chave_padrao") #Não esqueça de criar a SECRET_KEY no .env
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False #Exemplo, se usar banco

class DevelopmentConfig(Config):
    """Configurações para desenvolvimento."""
    DEBUG=True
    # SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"

class ProductionConfig(Config):
    """Configurações para produção."""   
    DEBUG=False
    # SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") # banco real na nuvem