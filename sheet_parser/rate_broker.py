import requests
import xmltodict as xd

from datetime import datetime

def get_rub_rate(currency) -> dict:
	# https://www.cbr.ru/scripts/XML_daily.asp?date_req=24/05/2022 - 24/05/2022 date
	url = f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={datetime.now().date().strftime('%d/%m/%Y')}"
	response = requests.get(url=url)
	d = xd.parse(response.content)
	for v in d['ValCurs']['Valute']:
		if v['CharCode'] == 'USD':
			v['NumCode'] = int(v['NumCode'].replace(',', '.'))
			v['Value'] = float(v['Value'].replace(',', '.'))
			v['Nominal'] = int(v['Nominal'])
			return v