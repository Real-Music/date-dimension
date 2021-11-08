import pandas as pd
from typing import List, Dict

names_of_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
names_of_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                   'November', 'December']


def create_date_dimension(start_year: int, stop_year: int) -> List[Dict]:
    start_date = f'{start_year}-01-01'
    stop_date = f'{stop_year}-12-31'

    # check if start year is not greater than stop year
    if start_year > stop_year:
        raise Exception(f'start_year: {start_year} can not be greater than stop year')

    # create a pd datetime object
    start_date_ts = pd.to_datetime(start_date)
    stop_date_ts = pd.to_datetime(stop_date)

    # generate date from start and stop date timestamp and rename index
    date_df = pd.DataFrame(index=pd.date_range(start_date_ts, stop_date_ts))
    date_df.index.name = 'full_date'

    # engineering
    days_names = {index: index + 1 for index, name in enumerate(names_of_days)}

    date_df['date_full_name'] = date_df.index.strftime('%B %d %Y')
    date_df['date_key'] = date_df.index.strftime('%Y%m%d')

    date_df['year'] = date_df.index.year
    date_df['is_leap_year'] = date_df.index.is_leap_year

    date_df['month_number'] = date_df.index.month
    date_df['month_name'] = date_df.index.strftime('%B')

    date_df['year_week'] = date_df.index.isocalendar().week
    date_df['day_of_week'] = date_df.index.dayofweek.map(days_names.get)

    date_df['day_of_month'] = date_df.index.day
    date_df['day_of_year'] = date_df.index.dayofyear

    date_df['day_name'] = date_df.index.strftime('%A')
    date_df['is_working_day'] = date_df['day_of_week'].apply(lambda day: True if day <= 5 else False)

    date_df['quarter'] = date_df.index.quarter
    date_df['year_half'] = date_df.index.month.map(lambda mth: 1 if mth < 7 else 2)

    date_df.reset_index(inplace=True)
    return list(date_df.tail().T.to_dict().values())
