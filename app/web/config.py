from dataclasses import dataclass
import typing
import pathlib

import yaml

if typing.TYPE_CHECKING:
    from app.web.app import Application

@dataclass
class Config:
    username: str
    password: str


BASE_DIR = pathlib.Path(__file__).parent.parent.parent
config_path = BASE_DIR / "config" / "config.yaml"

def setup_config(app: "Application"):
    with open("config/config.yaml") as file:
        raw_config = yaml.safe_load(file)

    app.config = Config(
        username=raw_config["credentials"]["username"],
        password=raw_config["credentials"]["password"]
    )

