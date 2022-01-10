from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGO_DSN: str
    DUCK_DUCK_GO_APT_ENDPOINT: str

    class Config:
        case_sensitive = True
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
