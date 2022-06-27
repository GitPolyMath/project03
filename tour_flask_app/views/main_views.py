from flask import Blueprint, render_template, request
from dotenv import load_dotenv
import pickle
import os
import psycopg2
import numpy as np


main_bp = Blueprint('main', __name__)

def postgreconn():

    load_dotenv()

    ## 가공된 데이터 RDBMS 적재 ##
    host = 'heffalump.db.elephantsql.com'
    user = 'flmgdojp'
    password = '3JM5mpw3YhAyWVm07rxzfOUX7jKtV59H'
    database = 'flmgdojp'

    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cur = connection.cursor()

    return connection, cur

## 제일 처음 인덱스 페이지 ##
@main_bp.route('/', methods=['GET'])
def index():
    return render_template('/main/index.html'), 200

## 예상 날씨 출력 페이지 ##
@main_bp.route('/main', methods=['POST'])
def main():
    
    temp_list=[]
    hum_list=[]
    date = None

    conn, cur = postgreconn()
    if request.method == 'POST':
        date = request.form['select']
    cur.execute(f"""select date, round(avg(temperature),2), round(avg(humidity),2)
                   from climate 
                   group by date
                   having date < '{date}' and date >= '{date}'::date -'3 day' ::interval
                   order by date desc;""")
    temps = cur.fetchall()

    for t_value in temps:
            temp_list.append(float(t_value[1]))
            hum_list.append(float(t_value[2]))
        ## 학습한 model 가져오기 ##
    with open('tour_flask_app/model.pkl','rb') as model_file:
        model = pickle.load(model_file)

        climate = round(model.predict([temp_list])[0], 1)
    conn.close()
    return render_template('/main/main.html', date=date, climate=climate, humidity=round(np.mean(hum_list),2)), 200


## 테마 소개페이지로 이동 ##
@main_bp.route('/main/art', methods=['GET'])
def themaart():
    return render_template('/main/themaart.html')

@main_bp.route('main/nature', methods=['GET'])
def themanature():
    return render_template('/main/themanature.html')

@main_bp.route('/main/history', methods=['GET'])
def themahistory():
    return render_template('/main/themahistory.html')


## 테마 id, 코스 id를 입력 받고

@main_bp.route('main/tour', methods=['POST'])
def tour():
    conn, cur = postgreconn() ## postgre 접속

    thema_list = []
    course_list = []
    spot_list=[]

    Themaname = None
    Coursename = None
    ## thema DB 추출 ##
    cur.execute("SELECT * FROM thema")
    themas = cur.fetchall()
    for thema in themas:
        thema_list.append(thema)

    ## course DB 추출 ##
    cur.execute("SELECT * FROM course")
    courses = cur.fetchall()
    for course in courses:
        course_list.append(course)

    if request.method == 'POST':
        themaId = request.form['thema']
        courseId = request.form['course']

        for t_value in thema_list:
            if t_value[0] == int(themaId):
                Themaname = t_value[1]
        
        for c_value in course_list:
            if c_value[0] == int(courseId):
                Coursename = c_value[1]
    
    ## 최종 spot장소 추출
    cur.execute(f"""select b.themaname , c.coursename, d.spotname
                   from tour as a
	                    join thema as b on a.themaid = b.id
	                    join course as c on a.courseid = c.id 
	                    join spot as d on a.spotid = d.id 
                   group by b.themaname , c.coursename, d.spotname
                   having b.themaname = '{Themaname}' and c.coursename = '{Coursename}';
    """)
    spots = cur.fetchall()
    for spotname in spots:
        spot_list.append(spotname[2])

    conn.close()
    return render_template('/main/recommand.html', themaname=Themaname, coursename=Coursename,spot_list=spot_list), 200

## 테마 
# @main_bp.route('/main/thema', methods=['GET'])
# def thema():
#     return render_template('/main/thema.html'), 200