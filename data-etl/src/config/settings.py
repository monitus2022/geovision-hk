from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://user:password@localhost:5432/geovision"
    data_api_url: str = "https://data.gov.hk/en-data/api/3/action/package_show?id=hk-landsd-openmap-landsd-building"
    geojson_url: str = "https://static.csdi.gov.hk/csdi-webpage/download/51d63757e2675874af80eef94afb6a35/geojson"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
