import psycopg2
import os
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression
from dotenv import load_dotenv

load_dotenv()

def postgreconn_ml():

    ## 가공된 데이터 RDBMS 적재 ##
    host = os.environ.get('ML_HOST')
    user = os.environ.get('ML_USER')
    password = os.environ.get('ML_PASSWORD')
    database = os.environ.get('ML_DATABASE')

    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cur = connection.cursor()

    return connection, cur

## 데이터베이스에서 데이터 추출 ##
climate_list = []
conn, cur = postgreconn_ml()

cur.execute("SELECT * FROM histclimate")

date_data = cur.fetchall()
for value in date_data:
    climate_list.append(value)

df = pd.DataFrame(climate_list, columns=['year', 'month', 'day', 'th'])

train_year = (df['year'] < 2020) ## 19년치 데이터
test_year = (df['year'] >= 2021) ## 1년치

interval = 3  # 3의 배수만큼 반복


## 최근 3일 데이터를 입력받으며 기온을 예측
def make_data(data):
    x = []
    y = []
    temps = list(data['th'])
    for i in range(len(temps)):
        if i < interval: continue # 1,2,3
        y.append(temps[i]) # 4부터 y리스트에 추가됨
        xa = []
        for p in range(interval):
            d = i + p - interval # i=4 + p=0 -3 -> 1 / 4 + 1 -3 -> 2 / 4 + 2 -3 -> 3
            xa.append(temps[d]) # 위에서 나온 1이 추가됨, 2, 3 추가됨(본인 날짜 기준 이전 3개)
        x.append(xa)
    return(x, y)

train_x, train_y = make_data(df[train_year])
test_x, test_y = make_data(df[test_year])

## 학습 후 결과 확인
lr = LinearRegression()
lr.fit(train_x, train_y) # 학습진행
predict_y = lr.predict(test_x) # test 데이터를 넣어서 예측해보기

print("예측스코어: ",lr.score(test_x,test_y))


## 학습한 모델을 pickle 부호화 진행 ##
with open('model.pkl','wb') as model_file:
    pickle.dump(lr, model_file)
