class NetworkConfig:
    host = '0.0.0.0'
    port = 8080

    def __init__(self, *, host='0.0.0.0', port=8080):
        NetworkConfig.host = host
        NetworkConfig.port = port
