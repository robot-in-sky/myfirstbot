from pydantic import BaseModel
from sqlalchemy.engine import URL

DB_SYSTEM = "postgresql"
DB_DRIVER = "psycopg"

class DatabaseSettings(BaseModel):

    host: str
    port: int = 5432
    username: str
    password: str | None
    database: str

    @property
    def url(self) -> str:
        return URL.create(
            drivername=f"{DB_SYSTEM}+{DB_DRIVER}",
            username=self.username,
            password=self.password,
            port=self.port,
            host=self.host,
            database=self.database,
        ).render_as_string(hide_password=False)

    echo: bool = False
