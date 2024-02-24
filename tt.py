#!/usr/bin/env python3
from datetime import datetime, timedelta

def formatDay(date):
    return "= " + date.strftime("%b %d | %a") + " =" + "=" * 16 + " " + str(date.year)

def generate_day_list():
    num_years = 20
    current_date = datetime.today()
    for _ in range(num_years * 365):
        print(formatDay(current_date))
        current_date += timedelta(days=1)

generate_day_list() # save generated days to chronicles.txt
