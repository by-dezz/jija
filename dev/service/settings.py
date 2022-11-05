from pathlib import Path

from jija import config
# from jija.utils.path import Path

SECRET_KEY = b'Thdrtd  two  length  bytes  key.'


config.DatabaseConfig(
    host='db',
    database='test_base',
    password='0000',
)



config.StructureConfig(
    project_path=Path(__file__).parent
    # python_path='../../venv/scripts/python.exe'
)

# config.NetworkConfig(
#     port=8081
# )

