from sqlalchemy import MetaData, Table, String, Integer, Column, Text, Date, Boolean
from datetime import datetime

from hashlib import md5

from .rate_broker import get_rub_rate

def get_records(gc, sh) -> list:
	wks = sh.sheet1
	recs = wks.get_all_records()

	return recs

def md5_hash(data: str):
	return md5(data.encode('utf-8')).hexdigest()
# 123
def update_rub_rate(records) -> list:
	# get rub rate in usd
	val_dict = get_rub_rate("USD")
	rub_rate_in_usd = val_dict['Value']
	rub_nominal_in_usd = val_dict['Nominal']
	# set usd=>rub
	new_records = []
	for row in records:
		price_usd = row['price_usd']
		row['price_rub'] = round(rub_rate_in_usd / rub_nominal_in_usd * float(price_usd))
		new_records.append(row)
	
	return new_records

def get_table(metadata) -> object:
	google_sheets = Table('google_sheets', metadata,
		Column('id', Integer(), index=True, unique=True, primary_key=True),
		Column('order', Integer(), nullable=False),
		Column('price_usd', Integer(), nullable=False),
		Column('delivery_time', Date(), default=datetime.now),
		Column('price_rub', Integer(), nullable=False)
		)
	return google_sheets

def create_table(engine) -> None:
	metadata = MetaData()
	google_sheets = get_table(metadata)
	metadata.create_all(engine)

def update_keys(records: list) -> dict:
	new_records = []
	for row in records:
		data = list(row.values())
		data = {
			'id': int(data[0]),
			'order': int(data[1]),
			'price_usd': int(data[2]),
			'delivery_time': datetime.strptime(data[3], "%d.%m.%Y").date(),
			'price_rub': int(0) # 
		}
		new_records.append(data)
	return new_records