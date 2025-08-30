import os
class Settings:
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "changeme")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

settings = Settings()
