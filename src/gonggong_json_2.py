# requests 라이브러리 설치
from pandas import read_json
import requests

re = requests.get('http://openapi.seoul.go.kr:8088/인증키/json/RealtimeCityAir/1/99')
rjson = re.json()

data = rjson['RealtimeCityAir']['row']

for i in range(0, len(data)):
    print("지역:" + data[i]['MSRSTE_NM'] + " " + str(data[i]['IDEX_MVL']) + " " + str(data[i]['IDEX_NM']))
    data2.append(data[i]['IDEX_MVL'])