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
#
# config.NetworkConfig(
#     port=8081
# )


