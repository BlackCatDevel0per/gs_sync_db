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

# Shift time
shifted_time = datetime.datetime.combine(row['delivery_time'], 
	tg_notify_time_shift)
# Add jobs to schedule for send notifications (with time shift from config)
def add_jobs() -> list:
	list_of_jobs = []
	for row in get_orders_date():
		# Add job
		job = sched.add_job(send_msg, 
			'date', 
			run_date=shifted_time, 
			args=[f"""Срок поставки прошёл для: {row['order']}"""])
		
		list_of_jobs.append(job)
		
		return list_of_jobs
		
if __name__ == '__main__':
	jobs = add_jobs()
	# Start schedule
	sched.start()
	
	# Reload jobs from db every n time from config
	while True:
		time.sleep(tg_notify_restart_timer)
		print("Telegram notifier restarted!")
		for job in jobs:
			job.remove()
		jobs = add_jobs()