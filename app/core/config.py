from pydantic_settings import BaseSettings, SettingsConfigDict

# Use .env file or environment variables to replace the default values of Config
class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "FastAPI"
    debug: bool = False

    # Database
    db_user: str = ""
    db_password: str = ""
    db_url: str = "sqlite:///./test.db"

    # SQLAlchemy
    sql_echo: str = ""


config = Config()
