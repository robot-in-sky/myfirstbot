from pathlib import Path

APP_DIR = Path(__file__).parent.resolve()
ROOT_DIR = APP_DIR.parent

ENVFILE_PATH = Path(ROOT_DIR).joinpath("env/.env")
ENVFILE_ENCODING = "utf-8"
ENVFILE_DELIMITER = "_"

DB_SYSTEM = "postgresql"
DB_DRIVER = "psycopg"
