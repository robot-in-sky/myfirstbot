import os
from argparse import Namespace
from pathlib import Path

from alembic.config import Config
from sqlalchemy import URL

from myfirstbot.definitions import ROOT_DIR

DEFAULT_CONFIG_FILE_NAME = "alembic.ini"
DEFAULT_INI_SECTION = "alembic"


def make_alembic_config(
        db_url: str | URL,
        config_file: str | os.PathLike[str] = DEFAULT_CONFIG_FILE_NAME,
        config_name: str = DEFAULT_INI_SECTION
) -> Config:

    if not Path(config_file).is_absolute():
        config_file = ROOT_DIR.joinpath(config_file).resolve()

    cmd_opts = Namespace(
        config=config_file,
        name=config_name,
        db_url=db_url,
        raiseerr=False,
        x=None,
    )

    config = Config(
        file_=cmd_opts.config,
        ini_section=cmd_opts.name,
        cmd_opts=cmd_opts
    )

    script_location = config.get_main_option("script_location")
    if not Path(script_location).is_absolute():
        config_dir = Path(config_file).parent
        script_location = config_dir.joinpath(script_location).resolve()
        config.set_main_option("script_location", str(script_location))

    config.set_main_option("sqlalchemy.url", cmd_opts.db_url)

    return config

