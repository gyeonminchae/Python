import pandas as pd
import requests

jsonUrl = 'http://kosis.kr/openapi/statisticsData.do?method=getList&apiKey=OGM2N2RlYTNmMjQ2MGY3NWEyYzg5MGU2NmJjYTI4Zjg=&format=json&jsonVD=Y&userStatsId=ox8eb1f9/101/DT_1B040A3/2/1/20200505230018&prdSe=M&newEstPrdCnt=1'

try:
    response = requests.get(jsonUrl)
    if response.status_code == 200:
        population = pd.read_json(jsonUrl)
    else:
        response.close()
except Exception as e:
    print(e)

population.head()