import pandas as pd
import requests

jsonUrl = 'http://kosis.kr/openapi/statisticsData.do?method=getList&apiKey=OGM2N2RlYTNmMjQ2MGY3NWEyYzg5MGU2NmJjYTI4Zjg=&format=json&jsonVD=Y&userStatsId=ox8eb1f9/101/DT_1B040A3/2/1/20200505230018&prdSe=M&newEstPrdCnt=1'

# 정상 여부 확인
response = requests.get(jsonUrl)
response

# JSON 데이터 획득
json = response.json()
# json

# 데이터프레임으로 저장
population = pd.json_normalize(json)
population.head()