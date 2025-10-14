#!/usr/bin/python3

import pandas as pd
import glob
import datetime

import os
from slack_sdk import WebClient

csv_path = '/asic/projects/E/ECON_PROD_TESTING/dnoonan/econ_json_parsing/DB_scripts/CSV'
f_D = glob.glob(f'{csv_path}/econdCSV/econd_chip_test_results_{datetime.datetime.now().year}-{datetime.datetime.now().month:02d}-{datetime.datetime.now().day:02d}_*.csv')[0]
f_T = glob.glob(f'{csv_path}/econtCSV/econt_chip_test_results_{datetime.datetime.now().year}-{datetime.datetime.now().month:02d}-{datetime.datetime.now().day:02d}_*.csv')[0]


try:
    df_D = pd.read_csv(f_D,index_col=0).sort_index()
    df_D.Timestamp = pd.to_datetime(df_D.Timestamp)
    df_D['Pass'] = df_D['Pass/Fail']=='Pass'
    df_D['Fail'] = df_D['Pass/Fail']=='Fail'
    by_week_D=df_D.groupby(pd.Grouper(key='Timestamp', freq='W'))

    summary_D = by_week_D.count()[['Pass/Fail']]
    summary_D.columns = ['Total']
    summary_D['Passing'] = by_week_D.sum()['Pass']
    summary_D['Failing'] = by_week_D.sum()['Fail']
except:
    summary_D = None

try:
    df_T = pd.read_csv(f_T,index_col=0).sort_index()
    df_T.Timestamp = pd.to_datetime(df_T.Timestamp)
    df_T['Pass'] = df_T['Pass/Fail']=='Pass'
    df_T['Fail'] = df_T['Pass/Fail']=='Fail'
    by_week_T=df_T.groupby(pd.Grouper(key='Timestamp', freq='W'))

    summary_T = by_week_T.count()[['Pass/Fail']]
    summary_T.columns = ['Total']
    summary_T['Passing'] = by_week_T.sum()['Pass']
    summary_T['Failing'] = by_week_T.sum()['Fail']
except:
    summary_T = None

if summary_T is None and summary_D is None:
    print('NO DATA')
    client = WebClient(token=token)

    result = client.chat_postMessage(channel = "cms-econ-asic",
                                     text = 'No chip test results found from past week.',
                                     username = "Bot User")

elif summary_T is None:
    print('NO DATA for ECONT, copying structure from ECOND')
    summary_T = summary_D.copy(deep=True)
    summary_T.loc[:,:] = 0
    summary = summary_D.merge(summary_T,how='outer',left_index=True,right_index=True,suffixes=('_ECOND','_ECONT')).fillna(0).astype(int)
elif summary_D is None:
    print('NO DATA for ECOND, copying structure from ECONT')
    summary_D = summary_T.copy(deep=True)
    summary_D.loc[:,:] = 0
    summary = summary_D.merge(summary_T,how='outer',left_index=True,right_index=True,suffixes=('_ECOND','_ECONT')).fillna(0).astype(int)
else:
    summary = summary_D.merge(summary_T,how='outer',left_index=True,right_index=True,suffixes=('_ECOND','_ECONT')).fillna(0).astype(int)

today = datetime.datetime.now()
lastMonth=(today-datetime.timedelta(days=28))
prior = summary[summary.index<lastMonth.strftime('%Y-%m-%d')]
prior_row = prior.sum()
prior = pd.DataFrame(prior_row.rename("Prior")).T
monthlySummary = summary[summary.index>lastMonth.strftime('%Y-%m-%d 08')]

monthlySummary = pd.concat([prior,monthlySummary])

total_row = monthlySummary.sum()
totals=pd.DataFrame(total_row.rename('Total')).T
monthlySummary = pd.concat([monthlySummary,totals])
print(monthlySummary)

report = f'```\n{monthlySummary.to_string()}\n```'

token = os.environ.get("SLACK_TOKEN")
if token is None:
    print("SLACK_TOKEN is not defined as environment variable, skipping send")
else:
    client = WebClient(token=token)

    result = client.chat_postMessage(
        channel = "cms-econ-asic",
        text = report,
        username = "Bot User")


