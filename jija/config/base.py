class BaseConfig:
    SECRET_KEY = None
    PORT = None

    def __init__(self, secret_key, port=8080):
        BaseConfig.SECRET_KEY = secret_key
        BaseConfig.PORT = port
