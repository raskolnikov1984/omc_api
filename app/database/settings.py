import os


class Settings:
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "SUp3r-pass*DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
    DATABASE = os.getenv("POSTGRES_DB", "omc")


settings = Settings()
