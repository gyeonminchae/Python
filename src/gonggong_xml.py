import requests, bs4
import pandas as pd
from lxml import html
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, unquote

# 1. URL 파라미터 분리하기.
# Service URL
xmlUrl = 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev'

My_API_Key = unquote('nIHNFvYbUsYHBizeBJ10UQBDliypceGUnFTLzIK3UmgKg0dTyzIBXDGJMPD3uiHlQOVHcQzdidYU7choE0BwMg==')

queryParams = '?' + urlencode(    # get 방식으로 쿼리를 분리하기 위해 '?'를 넣은 것이다. 메타코드 아님.
    {
        quote_plus('ServiceKey') : My_API_Key,    # 필수 항목 1 : 서비스키 (본인의 서비스키)
        quote_plus('LAWD_CD') : '11110',          # 필수 항목 2 : 지역코드 (법정코드목록조회에서 확인)
        quote_plus('DEAL_YMD') : '201512'         # 픽수 항목 3 : 계약월
     }
)

response = requests.get(xmlUrl + queryParams).text.encode('utf-8')
xmlobj = bs4.BeautifulSoup(response, 'lxml-xml')
# xmlobj    # 디버깅용.

rows = xmlobj.findAll('item')
# rows    # 디버깅용.
columns = rows[0].find_all()

# columns    # 디버깅용.
# columns[0].name    # 디버깅용.
# columns[0].text    # 디버깅용.

# 모든 행과 열의 값을 모아 매트릭스로 만들어보자.
rowList = []
nameList = []
columnList = []

rowsLen = len(rows)
for i in range(0, rowsLen):
    columns = rows[i].find_all()

    columnsLen = len(columns)
    for j in range(0, columnsLen):
        # 첫 번째 행 데이터 값 수집 시에만 컬럼 값을 저장한다. (어차피 rows[0], rows[1], ... 모두 컬럼헤더는 동일한 값을 가지기 때문에 매번 반복할 필요가 없다.)
        if i == 0:
            nameList.append(columns[j].name)
        # 컬럼값은 모든 행의 값을 저장해야한다.
        eachColumn = columns[j].text
        columnList.append(eachColumn)
    rowList.append(columnList)
    columnList = []    # 다음 row의 값을 넣기 위해 비워준다. (매우 중요!!)

result = pd.DataFrame(rowList, columns=nameList)
print(result)

result.to_csv('../data/Apt.csv', encoding='cp949')