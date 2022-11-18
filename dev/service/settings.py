from pathlib import Path
from jija import config
from jija import drivers


config.DatabaseConfig(
    host='db',
    database='test_base',
    password='0000',
)

config.StructureConfig(
    project_path=Path(__file__).parent
)


config.DriversConfig(
    database=drivers.JijaOrmDriver
)


from jija.contribute.auth import config as auth_config

auth_config.AuthConfig(
    secret_key=b'*' * 32
)


#
# config.NetworkConfig(
#     port=8081
# )


