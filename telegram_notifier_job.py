import os
import sys
import signal
import subprocess, shlex

import time

from sheet_parser.config import tg_notify_restart_timer

try:
	while True:
		# Run telegram notifier job (restart every n time from config.ini)
		telegram_notifier_job = subprocess.Popen(
			shlex.split(f'{sys.executable} telegram_notifier.py'))
		telegram_notifier_job.wait()
		print(tg_notify_restart_timer)
		time.sleep(tg_notify_restart_timer)
		os.killpg(os.getpgid(telegram_notifier_job.pid), signal.SIGTERM)
except KeyboardInterrupt:
	os.killpg(os.getpgid(telegram_notifier_job.pid), signal.SIGTERM)
