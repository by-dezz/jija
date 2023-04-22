from pathlib import Path
from jija import config

from jija.contrib.swagger.driver import SwaggerDriver
from jija.contrib.auth.config import AuthConfig


config.StructureConfig(
    project_path=Path(__file__).parent
)

config.NetworkConfig(
    port=8081
)

config.DriversConfig(
    docs=SwaggerDriver(),
)

AuthConfig(
    secret_key=b'*' * 32
)
