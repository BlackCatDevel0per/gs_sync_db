import configparser

_config = configparser.ConfigParser()
_config_file = 'config.ini'
_config.read(_config_file)

client_secret_file = _config["GOOGLE"]["client_secret_file"]
gs_file = _config["GOOGLE"]["gs_file"]

alchemy_engine = _config["SQL"]["alchemy_engine"]
timer = int(_config["OPTIONS"]["timer"])
