"""Configuración vía variables de entorno."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Ajustes de la aplicación.

    Args: ninguno (se puebla desde entorno).
    """

    database_url: str = "postgresql+psycopg://turnos:turnos@localhost:5432/turnos"
    jwt_secret: str = "cambiar-en-produccion"
    app_tz: str = "America/Argentina/Cordoba"


settings = Settings()
