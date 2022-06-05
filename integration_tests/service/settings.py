from jija import config

SECRET_KEY = b'Thdrtd  two  length  bytes  key.'


config.DatabaseConfig(
    host='db',
    database='test_base',
    password='0000',
)


config.StructureConfig(
    # python_path='../../venv/scripts/python.exe'
)


config.NetworkConfig(
    port=8081
)

