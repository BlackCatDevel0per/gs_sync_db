import pygsheets

from sqlalchemy import create_engine
from sqlalchemy import MetaData

import time
from datetime import datetime

from .helpers import upsert

from .rate_broker import get_rub_rate

from .sql import get_records, md5_hash
from .sql import update_rub_rate, get_table
from .sql import create_table
from .sql import update_keys

from .config import client_secret_file
from .config import gs_file
from .config import alchemy_engine

from .config import timer

engine = create_engine(alchemy_engine)
conn = engine.connect()
metadata = MetaData()

google_sheets = get_table(metadata)

