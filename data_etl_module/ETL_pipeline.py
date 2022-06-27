import requests
import json
import psycopg2
from dotenv import load_dotenv
from pymongo import MongoClient
from database_connection import mongoconn, postgreconn
import os

load_dotenv() ## env에 있는 환경변수 불러오기


## (1) MongoDB에 있는 JSON데이터 추출 ##
## 연결 했을 때 오류메시지 발생의 경우 클라우드 데이터베이스의 연결상태 확인하기!(홈페이지 들어가서) ##
coll = mongoconn()


## list(dict.fromkeys())를 통한 중복제거 ##

thema_list=[] ## 테마리스트
course_list=[] ## 코스지역리스트
spot_list=[] ## 명확한 장소리스트
climate_list=[] ## 기온 리스트
tour_list = [] ## 관광 리스트
i = 1

toursData = coll.find() ## MongoDB에 있는 모든 Data 추출


## (2) JSON 데이터 RDBMS에 들어갈 수 있게 Transform 진행 ##

for tour in toursData:
    try:
        values = tour['response']['body']['items']['item']
        for val in values:
            # print(val)
            if val['tm'].split(" ")[1] == '00:00':
                thema_list.append(val['thema']) ## 테마명 list로 저장
                course_list.append((val['courseId'], val['courseName'])) ## 코스명 list로 저장
                spot_list.append((val['spotAreaId'], val['spotName'])) ## 관광지명 list로 저장
                if val['tm'].split("-")[0] == '2022': ## 2022년 데이터만 list에 저장하겠다.
                    climate_list.append((i, val['th3'], val['wd'], val['ws'], val['rhm'], val['tm'].split(' ')[0] ,val['spotAreaId'])) ## 기후데이터 list로 저장
                    if val['thema'] == '문화/예술':
                        tour_list.append((1, val['courseId'], val['spotAreaId'], i)) ## 투어 list 저장
                    elif val['thema'] == '체험/학습/산업':
                        tour_list.append((2, val['courseId'], val['spotAreaId'], i))
                    elif val['thema'] == '쇼핑/놀이':
                        tour_list.append((3, val['courseId'], val['spotAreaId'], i))
                    elif val['thema'] == '자연/힐링':
                        tour_list.append((4, val['courseId'], val['spotAreaId'], i))
                    elif val['thema'] == '종교/역사/전통':
                        tour_list.append((5, val['courseId'], val['spotAreaId'], i))
                    i+=1
    except:
        print("오류입니다.")

## dict.fromkeys() 사용하여 중복데이터 제거 ##
## -> dict.fromkeys()를 사용하여 기존 리스트의 순서를 유지하면서 중복제거
## python 3.7버전부터 dictionary가 삽입 순서를 보존하기 때문
## 데이터 한꺼번에 넣기 위해서는 꼭 append 뒤에 튜플()로 감싸서 보내기

thema_del_duple=list(dict.fromkeys(thema_list))
course_del_duple=list(dict.fromkeys(course_list))
spot_del_duple=list(dict.fromkeys(spot_list))
climate_del_duple=list(dict.fromkeys(climate_list))
tour_del_duple=list(dict.fromkeys(tour_list))



## (3) 가공된 데이터 RDBMS 적재 ##
## 연결 했을 때 오류메시지 발생의 경우 클라우드 데이터베이스의 연결상태 확인하기!(홈페이지 들어가서) ##
conn, cur = postgreconn()

cur.execute("DROP TABLE IF EXISTS Spot;")
cur.execute("DROP TABLE IF EXISTS Thema;")
cur.execute("DROP TABLE IF EXISTS Course;")
cur.execute("DROP TABLE IF EXISTS Climate;")
cur.execute("DROP TABLE IF EXISTS Tour;")

# 꼭 해당 순서대로 table 생성 진행 -> foreign key가 있기 때문 #

# Spot 테이블
cur.execute("""CREATE TABLE Spot(
                id INTEGER PRIMARY KEY,
                spotname VARCHAR(50));""")

# thema 테이블
cur.execute("""CREATE TABLE Thema(
                id SERIAL PRIMARY KEY,
                themaname VARCHAR(50));""")

## Course 테이블 생성 및 데이터 적재
cur.execute("""CREATE TABLE Course(
                id INTEGER PRIMARY KEY,
                coursename VARCHAR(50));""")

## Climate 테이블 생성 및 데이터 적재 ##
cur.execute("""CREATE TABLE Climate(
                id INTEGER PRIMARY KEY,
                temperature INTEGER,
                winddirec INTEGER,
                windspe INTEGER,
                humidity INTEGER,
                date DATE,
                spotId INTEGER,
                FOREIGN KEY (spotId) REFERENCES Spot(id) ON UPDATE CASCADE);""")

## Tour 테이블 생성 및 데이터 적재 ##
cur.execute("""CREATE TABLE Tour(
                id SERIAL PRIMARY KEY,
                themaId INTEGER NOT NULL,
                courseId INTEGER NOT NULL,
                spotId INTEGER NOT NULL,
                climateId INTEGER NOT NULL,
                FOREIGN KEY (themaId) REFERENCES Thema(id) ON UPDATE CASCADE,
                FOREIGN KEY (courseId) REFERENCES Course(id) ON UPDATE CASCADE,
                FOREIGN KEY (spotId) REFERENCES Spot(id) ON UPDATE CASCADE,
                FOREIGN KEY (climateId) REFERENCES Climate(id) ON UPDATE CASCADE);""")

conn.commit() ## table 생성에 대한 COMMIT

## DB INSERT시 데이터 타입 꼭 확인하여 넣기 -> VARCHAR타입이면 '' 붙이기 ##
## thema 데이터 INSERT ##
for t_value in thema_del_duple:
    cur.execute(f"INSERT INTO Thema (id, themaname)VALUES (DEFAULT, '{t_value}');")
conn.commit() ## INSERT 마다 바로 COMMIT 진행

## spot 데이터 INSERT ##
for value in spot_del_duple:
    cur.execute("INSERT INTO Spot VALUES (%s, %s)", value)
conn.commit() ## INSERT 마다 바로 COMMIT 진행

## course 데이터 INSERT ##
for c_value in course_del_duple:
    cur.execute("INSERT INTO Course VALUES(%s, %s)", c_value)
conn.commit() ## INSERT 마다 바로 COMMIT 진행

## climate 데이터 INSERT ##
for cli_value in climate_del_duple:
    cur.execute("INSERT INTO Climate VALUES(%s, %s, %s, %s, %s, %s, %s)", cli_value)
conn.commit() ## INSERT 마다 바로 COMMIT 진행

for tour_value in tour_del_duple:
    cur.execute(f"INSERT INTO Tour(id, themaId, courseId, spotId, climateId) VALUES(DEFAULT,{tour_value[0]},{tour_value[1]},{tour_value[2]}, {tour_value[3]})")
conn.commit() ## INSERT 마다 바로 COMMIT 진행