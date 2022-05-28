# install requirements
```
pip install -r requirements.txt
```

# first edit/create config.ini
```
[GOOGLE]
client_secret_file = client_secret.json

gs_file = test_sheet

[TELEGRAM]
token = 1234567890:abcdefghijklmnopqrstuvwxyz---------
chat_ids = -1234567890098, 1234567890

[SQL]
alchemy_engine = postgresql+psycopg2://admin:passwd@localhost/db_name

[OPTIONS]
timer = 01:00:00
tg_notify_restart_timer = 01:00:00
tg_notify_time_shift = 01:00:00
```

to get client_secret.json and sheets.googleapis.com-python.json file create google api token (read pygsheets docs)
more info: https://pygsheets.readthedocs.io/en/stable/authorization.html

in gs_file paste your sheet name from google drive/sheets
# sqlalchemy engine example:
```
alchemy_engine = postgresql+psycopg2://username:password@host/db_name
```

run
```
# parser
python sheet_parser.py
# site
python sheet_parser/manage.py runserver
```