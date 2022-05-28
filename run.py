import os
import sys
import signal
import subprocess, shlex

try:
	p2 = subprocess.Popen(
		shlex.split(f'{sys.executable} sheet_parser.py'))
	os.chdir(os.path.join(os.getcwd(), 'info_site'))
	p1 = subprocess.Popen(
		shlex.split(f'{sys.executable} manage.py runserver 0.0.0.0:8000'))
	p1.wait()
	p2.wait()
except KeyboardInterrupt:
	os.killpg(os.getpgid(p1.pid), signal.SIGTERM)
	os.killpg(os.getpgid(p2.pid), signal.SIGTERM)
