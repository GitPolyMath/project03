import json
import requests
import os
import time
from pymongo import MongoClient
from database_connection import mongoconn
from dotenv import load_dotenv

## NoSQL DB세팅 ## 
# -> 데이터가 API를 통해서 대량으로 가져오다보니, 가공해서 적재를 할 수 없음 #

load_dotenv() # take enviroment variables from .env

## MongoDB 적재할 계정정보 입력 ##

coll = mongoconn()

######################################################################################################


## 총 관광코스: 433개이지만, 너무 큰 데이터가 될거 같아 서울근교 중심으로 데이터 추출
## 서울 근교관광지: 52~78,
seoul_id_list=[]

for i in range(52,73):
    seoul_id_list.append(i)
for i in range(74,79):
    seoul_id_list.append(i)

## 2020 ~ 2022년 5,6,7월 데이터를 추출
cur_date_list=[]

## 2020년도부터 순차적으로 적재 진행
cur_date = 20220501
print(cur_date)
for _ in range(53):
    if cur_date == 20220531:
        cur_date_list.append(cur_date) ## 마지막날 리스트에 넣고
        cur_date = (cur_date-30)+100 ## 초기 세팅 진행(일자는 빼고, 월은 증가 )
    # elif cur_date == 20220630:
    #     cur_date_list.append(cur_date)
    #     cur_date =  (cur_date-29)+100
    else:
        cur_date_list.append(cur_date)
        cur_date += 1


#  제출 때 주석처리 풀고!! 
# skey = os.environ.get('SKEY')
# url = 'http://apis.data.go.kr/1360000/TourStnInfoService/getTourStnVilageFcst'
# for seoul_tour_id in seoul_id_list:
#     time.sleep(10)
#     for c_date in cur_date_list:
#         params ={'serviceKey' : f'{skey}', 'pageNo' : '1', 'numOfRows' : '100', 'dataType' : 'JSON', 'CURRENT_DATE' : f'{c_date}', 'HOUR' : '24', 'COURSE_ID' : f'{seoul_tour_id}' }
#         response = requests.get(url, params=params)
#         time.sleep(3) ## 10초 동안 requests 멈춤
#         print(response)
#         curseArea = json.loads(response.content)
#         coll.insert_one(curseArea) ## MongoDB 데이터 적재
#         print(f"{curseArea}")
    