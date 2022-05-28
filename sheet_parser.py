from sheet_parser.app import *

if __name__ == '__main__':
	try:
		gc = pygsheets.authorize(client_secret=client_secret_file)
		sh = gc.open(gs_file)
	
		# run
		records = get_records(gc, sh)
		old_records = records.copy()
		old_rate = get_rub_rate("USD")['Value']
		# records = update_keys(records)
		# records = update_rub_rate(records)
		# print(records)
	
		# print(records[0])
		# print(records[1])
		# print(records[2])
		
		create_table(engine) # create table if not exists
		# convert gsheets for db
		records = update_keys(records)
		records = update_rub_rate(records)
		# Check if removed rows in gsheets
		old_db_data = conn.execute(google_sheets.select().with_only_columns(google_sheets.c.id)).fetchall()
		old_db_data = [i[0] for i in old_db_data]
		if len(records) < len(old_db_data):
			rows_ids_to_delete = [i for i in old_db_data if i not in [list(nr.values())[0] for nr in records]]
			q = google_sheets.delete().where(google_sheets.c.id.in_(tuple(rows_ids_to_delete)))
			conn.execute(q)
		# upset data to db
		conn.execute(upsert(google_sheets, records))
		"""
		row = records[1]
		ins = google_sheets.insert().values(
			id = row[0],
			order = row[1],
			price_usd = row[2],
			delivery_time = datetime.strptime(row[3], "%d.%m.%Y").date(),
			price_rub = 300
			)
		"""
		# ins = google_sheets.insert()
		# upd = google_sheets.update()
		# print(ins.compile().params)
		# print(data)
		# print(len(data))
	except Exception as e:
		print("Startup Error!", "\n", e)
	while True:
		time.sleep(timer)
		print("Checking data..")
		try:
			records = get_records(gc, sh)
			current_rate = get_rub_rate("USD")['Value']
			if md5_hash(str(records)) != md5_hash(str(old_records)) or current_rate != old_rate:
				old_rate = current_rate
				# Check if removed rows
				if len(records) < len(old_records):
					rows_ids_to_delete = [list(r.values())[0] for r in old_records if list(r.values())[0] not in [list(nr.values())[0] for nr in records]]
					q = google_sheets.delete().where(google_sheets.c.id.in_(tuple(rows_ids_to_delete)))
					conn.execute(q)
					
				# update old gsheets data
				old_records = records.copy()
				# convert gsheets for db
				records = update_keys(records)
				records = update_rub_rate(records)
				# upset data to db
				conn.execute(upsert(google_sheets, records))
				print("Data updated!", datetime.now())
		except Exception as e:
			print("Task Error!", "\n", e)
		
	# with open('data.txt', 'w') as f:
	# 	f.write(str(data))
