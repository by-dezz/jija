from jija import config

SECRET_KEY = b'Thdrtd  two  length  bytes  key.'


config.DatabaseConfig(
    host='db',
    database='test_base',
    password='0000',
)


config.StructureConfig(
    project_dir='/app'
    # python_path='../../venv/scripts/python.exe'
)
print(config.StructureConfig.PROJECT_PATH.system)

config.NetworkConfig(
    port=8081
)

