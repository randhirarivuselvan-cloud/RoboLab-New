from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "RoboLab"
    company_name: str = "SynapseX Robotics & Technologies"
    secret_key: str = "development-only-change-me"
    database_path: str = "database/robolab.db"
    allowed_origins: str = "http://127.0.0.1:8000,http://localhost:8000"
    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = "http://127.0.0.1:8000/api/auth/google/callback"
    openai_api_key: str = ""
    openai_model: str = "gpt-4.1-mini"
    stripe_secret_key: str = ""
    stripe_monthly_price_id: str = ""
    stripe_annual_price_id: str = ""
    stripe_success_url: str = "http://127.0.0.1:8000/?payment=success"
    stripe_cancel_url: str = "http://127.0.0.1:8000/?payment=cancelled"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def origins(self):
        return [x.strip() for x in self.allowed_origins.split(",") if x.strip()]

settings = Settings()
