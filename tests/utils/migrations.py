from argparse import Namespace
from os import PathLike
from pathlib import Path

from alembic.config import Config
from sqlalchemy import URL, MetaData, engine_from_config, pool, text

from src.paths import ROOT_DIR


def get_alembic_config(
        file_: str | PathLike[str] = "alembic.ini",
        ini_section: str = "alembic",
        db_url: str | URL | None = None,
) -> Config:

    if not Path(file_).is_absolute():
        file_ = ROOT_DIR.joinpath(file_).resolve()

    config = Config(
        file_=file_,
        ini_section=ini_section,
        cmd_opts=Namespace(
            config=file_,
            name=ini_section,
            db_url=db_url,
            raiseerr=False,
            x=None,
        ),
    )

    script_location = config.get_main_option("script_location")
    if script_location and not Path(script_location).is_absolute():
        config_dir = Path(file_).parent
        script_location = config_dir.joinpath(script_location).resolve()
        config.set_main_option("script_location", str(script_location))

    if db_url:
        config.set_main_option("sqlalchemy.url", str(db_url))

    return config


def reset_db(config: Config) -> None:

    engine = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    metadata = MetaData()
    metadata.reflect(bind=engine)
    metadata.drop_all(bind=engine)

    statement = """DROP TABLE IF EXISTS alembic_version"""
    with engine.connect() as conn:
        conn.execute(text(statement))
        conn.commit()
