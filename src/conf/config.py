from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    sqlalchemy_database_url: str = Field(..., env='SQLALCHEMY_DATABASE_URL')
    secret_key: str = Field(..., env='SECRET_KEY')
    algorithm: str = Field(..., env='ALGORITHM')
    mail_username: str = Field(..., env='MAIL_USERNAME')
    mail_password: str = Field(..., env='MAIL_PASSWORD')
    mail_from: str = Field(..., env='MAIL_FROM')
    mail_port: int = Field(..., env='MAIL_PORT')
    mail_server: str = Field(..., env='MAIL_SERVER')
    redis_host: str = Field('localhost', env='REDIS_HOST')
    redis_port: int = Field(6379, env='REDIS_PORT')

    @validator('*')
    def check_not_empty(cls, v):
        if isinstance(v, str) and not v:
            raise ValueError('Value cannot be empty')
        return v

    @validator('mail_port')
    def check_mail_port(cls, v):
        if not 0 < v < 65536:
            raise ValueError('Mail port must be between 1 and 65535')
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()