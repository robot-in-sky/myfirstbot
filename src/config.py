from pathlib import Path

APP_NAME = "visa_agent_bot"
APP_VERSION = "0.1.0"

SRC_DIR = Path(__file__).parent.resolve()
ROOT_DIR = SRC_DIR.parent
ENV_FILE_PATH = Path(ROOT_DIR).joinpath("env/.env")
