from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    number_of_requests: int
    total_time: int
    ip_address: str = "127.0.0.1"
    port: int = 8000
    endpoint: str = "DDos_test"

    model_config = SettingsConfigDict(env_file=".env")
