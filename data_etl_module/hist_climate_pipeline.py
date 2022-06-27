import time
import pandas as pd
import numpy as np
from database_connection import postgreconn_ml


def daily_climate(year):
    ## csv 데이터 불러오기 
    df = pd.read_csv(f"hist_climate\{year}_climate_daily.csv", encoding='CP949')

    ## 필요한 컬럼만 가져옴
    df = df[['일시','평균기온(°C)']]

    # columns 네이밍 변경
    df.rename(columns={'일시':'date', '평균기온(°C)':'th'}, inplace=True)

    # year(연), month(월), day(일)로 데이터 추가 컬럼 제작
    # date컬럼을 datetime 형식으로 변경
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df = df[['year', 'month','day','th']]

    return df

df_02 = daily_climate(2002)
df_03 = daily_climate(2003)
df_04 = daily_climate(2004)
df_05 = daily_climate(2005)
df_06 = daily_climate(2006)
df_07 = daily_climate(2007)
df_08 = daily_climate(2008)
df_09 = daily_climate(2009)
df_10 = daily_climate(2010)
df_11 = daily_climate(2011)
df_12 = daily_climate(2012)
df_13 = daily_climate(2013)
df_14 = daily_climate(2014)
df_15 = daily_climate(2015)
df_16 = daily_climate(2016)
df_17 = daily_climate(2017)
df_18 = daily_climate(2018)
df_19 = daily_climate(2019)
df_20 = daily_climate(2020)
df_21 = daily_climate(2021)

df = pd.concat([df_02, df_03, df_04, df_05, df_06, df_07, df_08, df_09, df_10, df_11, df_12, df_13, df_14, df_15, df_16, df_17, df_18, df_19,df_20, df_21])

conn, cur = postgreconn_ml()
time.sleep(5)

hist = []

for y, m, d, t in zip(df['year'], df['month'], df['day'], df['th']):
    hist.append((y,m,d,t))

## table 생성
cur.execute("DROP TABLE IF EXISTS HistClimate;")
cur.execute("""CREATE TABLE HistClimate
                year DATE,
                month DATE,
                day DATE,
                temperature INTEGER
""")
for hist_cli in hist:
    cur.execute("""INSERT INTO VALUES (%s, %s, %s, %s);""", hist_cli)
conn.commit()


