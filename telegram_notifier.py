import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

import requests

from sheet_parser.config import token, chat_ids, time_shift

from sheet_parser.app import google_sheets, conn

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
	
sched = BlockingScheduler()

# Add jobs to schedule for send notifications (with time shift from config)
for row in get_orders_date():
	shifted_time = datetime.datetime.combine(row['delivery_time'], 
		datetime.datetime.strptime(time_shift, "%H:%M:%S").time())
	sched.add_job(send_msg, 
		'date', 
		run_date=shifted_time, 
		args=[f"""Срок поставки прошёл для: {row['order']}"""])

sched.start()

