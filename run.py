import os
import sys
import signal
import subprocess, shlex

try:
	# Run Google Sheets sync
	google_sheets_sync = subprocess.Popen(
		shlex.split(f'{sys.executable} sheet_parser.py'))
	# Run telegram notifier
	telegram_notifier = subprocess.Popen(
		shlex.split(f'{sys.executable} telegram_notifier_job.py'))
	# Changing directory for run django site
	os.chdir(os.path.join(os.getcwd(), 'info_site'))
	django_site = subprocess.Popen(
		shlex.split(f'{sys.executable} manage.py runserver 0.0.0.0:8000'))
	django_site.wait()
	google_sheets_sync.wait()
	telegram_notifier.wait()
except KeyboardInterrupt:
	os.killpg(os.getpgid(django_site.pid), signal.SIGTERM)
	os.killpg(os.getpgid(google_sheets_sync.pid), signal.SIGTERM)
	os.killpg(os.getpgid(telegram_notifier.pid), signal.SIGTERM)
