import time
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

import requests

from sheet_parser.config import token, chat_ids, tg_notify_time_shift

from sheet_parser.app import google_sheets, conn

from sheet_parser.config import tg_notify_restart_timer

# Send nessage to telegram
def send_msg(text):
	# You can get chat_id from @chat_id_echo_bot
	for chat_id in chat_ids:
		url_req = f"""https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}"""
		r = requests.get(url_req)
		if r.status_code == 200:
			print("Sended to", chat_id)
		else:
			print("Err:", r.status_code)
			
# Get orders delivery date/time
def get_orders_date():
	q = google_sheets.select().with_only_columns(google_sheets.c.order, google_sheets.c.delivery_time)
	result = conn.execute(q).fetchall()
	return result
	
sched = BackgroundScheduler()

# Add jobs to schedule for send notifications (with time shift from config)
def add_jobs():
	for row in get_orders_date():
		# Shift time
		shifted_time = datetime.datetime.combine(row['delivery_time'], 
			tg_notify_time_shift)
		# Add job
		sched.add_job(send_msg, 
			'date', 
			run_date=shifted_time, 
			args=[f"""Срок поставки прошёл для: {row['order']}"""])
		
if __name__ == '__main__':
	jobs = add_jobs()
	# Start schedule
	sched.start()
	
	# Reload jobs from db every n time from config
	while True:
		time.sleep(tg_notify_restart_timer)
		for job in sched.get_jobs():
			job.remove()
		jobs = add_jobs()
		print("Telegram notifier restarted!")