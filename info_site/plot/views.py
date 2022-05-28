from django.shortcuts import render
# from django.template.response import TemplateResponse

import os
# import table model and connection
from sheet_parser.app import google_sheets, conn

def get_prices_in(rate_in: str):
    dates = []
    prices = []
    
    query = google_sheets.select().order_by(google_sheets.c.delivery_time)
    r = conn.execute(query).fetchall()

    for row in r:
        prices.append(row[rate_in])
        dates.append(row['delivery_time'].strftime("%d.%m.%Y"))
    # print(dates, prices)
    return dates, prices

def index_usd(request):
    dates, prices_usd = get_prices_in('price_usd')
    return render(request, 'plot/index.html', {
        'dates': dates,
        'prices': prices_usd,
    })


def index_rub(request):
    dates, prices_usd = get_prices_in('price_rub')
    return render(request, 'plot/index.html', {
        'dates': dates,
        'prices': prices_usd,
    })

def index(request):
    return index_usd(request)