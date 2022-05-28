import configparser
import datetime

_config = configparser.ConfigParser()
_config_file = 'config.ini'
_config.read(_config_file)

client_secret_file = _config["GOOGLE"]["client_secret_file"]
gs_file = _config["GOOGLE"]["gs_file"]

token = _config["TELEGRAM"]["token"]
chat_ids = ' '.join(_config["TELEGRAM"]["chat_ids"].split(",")).split()

alchemy_engine = _config["SQL"]["alchemy_engine"]

_timer = datetime.datetime.strptime(_config["OPTIONS"]["timer"], '%H:%M:%S').time()
# time in seconds
timer = _timer.hour*60**2 + _timer.minute*60 + _timer.second
_tg_notify_restart_timer = datetime.datetime.strptime(_config["OPTIONS"]["tg_notify_restart_timer"], '%H:%M:%S').time()
# time in seconds
tg_notify_restart_timer = _tg_notify_restart_timer.hour*60**2 + _tg_notify_restart_timer.minute*60 + _tg_notify_restart_timer.second

_tg_notify_time_shift = _config["OPTIONS"]["tg_notify_time_shift"]
# datetime object
tg_notify_time_shift = datetime.datetime.strptime(_tg_notify_time_shift, "%H:%M:%S").time()