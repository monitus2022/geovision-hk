import psycopg
from src.config.settings import settings


def get_connection():
    return psycopg.connect(settings.database_url)


def load_to_staging(data):
    pass


def replace_table():
    pass
