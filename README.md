# 서울근교 여행지 추천 프로젝트

>웹 애플리케이션 주소: https://seoul-tourism-project.herokuapp.com/

![image](https://user-images.githubusercontent.com/102206023/195558071-58c62f84-c064-4311-8ae8-a3755863479e.png)


### **1. 프로젝트 소개**
**예측한 날씨를 바탕으로, 서울 근교 여행지를 추천**

### **2. 파이프라인 소개**
- 데이터 출처:
  - 기상청 기상자료(종관기상관측_ASOS_일별): https://data.kma.go.kr/data/grnd/selectAsosRltmList.do?pgmNo=36
  - 기상청 관광코스별 관광지 상세 날씨 조회서비스: https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15056912

![AI_13_이기돈_Section03_DataPipeline_3D](https://user-images.githubusercontent.com/102206023/195554030-b0a5861b-15d7-4af7-90e2-c2a16c209f83.png)

### **3. 코드구현 과정**
1. 데이터 ETL과정 
  - JSON 데이터 RDBMS에 적재할 수 있게 Transform진행
![image](https://user-images.githubusercontent.com/102206023/195562874-29f03058-7ae5-49d3-9358-479d626a7b15.png)

  - Postgre RDBMS에 데이터 Load 진행
![image](https://user-images.githubusercontent.com/102206023/195563162-23be6100-58ca-4e92-bd24-65d4be3d0a2c.png)
![image](https://user-images.githubusercontent.com/102206023/195563476-25f13d52-e926-4b06-a05e-6bcea651ac1a.png)

2. FLASK 애플리케이션 구현과정
![image](https://user-images.githubusercontent.com/102206023/195564092-00c151e8-22e7-4388-9f95-727450354d51.png)

### **4. 구현화면**
![image](https://user-images.githubusercontent.com/102206023/195564603-64a74c57-1fa5-4b32-849f-d975f80a641b.png)
![image](https://user-images.githubusercontent.com/102206023/195564613-610195e8-1b4c-4c93-ac89-ab05a59dd538.png)
