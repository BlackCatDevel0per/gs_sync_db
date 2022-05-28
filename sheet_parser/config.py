import configparser

_config = configparser.ConfigParser()
_config_file = 'config.txt'
_config.read(_config_file)

client_secret_file = _config["GOOGLE"]["client_secret_file"]
gs_file = _config["GOOGLE"]["gs_file"]

token = _config["TELEGRAM"]["token"]
chat_ids = ' '.join(_config["TELEGRAM"]["chat_ids"].split(",")).split()

alchemy_engine = _config["SQL"]["alchemy_engine"]
timer = int(_config["OPTIONS"]["timer"])
time_shift = _config["OPTIONS"]["time_shift"]
