#라이브러리 import
import requests
from bs4 import BeautifulSoup
import pandas as pd

#요청url 잘게 자르기
url = "http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson?"
serviceKey = "serviceKey=nIHNFvYbUsYHBizeBJ10UQBDliypceGUnFTLzIK3UmgKg0dTyzIBXDGJMPD3uiHlQOVHcQzdidYU7choE0BwMg=="
pageNo="&pageNo=1"
numOfRows="&numOfRows=10"
StartCreateDt = "&startCreateDt=20210101"
endCreateDt = "&endCreateDt=20211231"

#항목 parsing 함수작성하기
def parse():
    try:
        SEQ = item.find("seq").get_text()
        DEATH_CNT = item.find("DEATH_CNT").get_text()
        GUBUN = item.find("GUBUN").get_text()
        gubunEn = item.find("gubunEn").get_text()
        INC_DEC = item.find("INC_DEC").get_text()
        QUR_RATE = item.find("QUR_RATE").get_text()
        STD_DAY = item.find("STD_DAY").get_text()
        DEF_CNT = item.find("DEF_CNT").get_text()
        OVER_FLOW_CNT = item.find("OVER_FLOW_CNT").get_text()
        LOCAL_OCC_CNT = item.find("LOCAL_OCC_CNT").get_text()
        CREATE_DT = item.find("createDt").get_text()
        UPDATE_DT = item.find("UPDATE_DT").get_text()
        return {
            "게시글번호":SEQ,
            "사망자 수":DEATH_CNT,
            "시도명(한글)":GUBUN,
            "시도명(영어)":gubunEn,
            "전일대비 증감 수":INC_DEC,
            "10만명당 발생률":QUR_RATE,
            "기준일시":STD_DAY,
            "확진자 수":DEF_CNT,
            "해외유입 수":OVER_FLOW_CNT,
            "지역발생 수":LOCAL_OCC_CNT,
            "등록일시분초":CREATE_DT,
            "수정일시분초":UPDATE_DT
        }
    except AttributeError as e:
        return {
            "게시글번호":None,
            "사망자 수":None,
            "시도명(한글)":None,
            "시도명(영어)":None,
            "전일대비 증감 수":None,
            "10만명당 발생률":None,
            "기준일시":None,
            "확진자 수":None,
            "해외유입 수":None,
            "지역발생 수":None,
            "등록일시분초":None,
            "수정일시분초":None
        }

#parsing 하기
result = requests.get(url+serviceKey+pageNo+numOfRows+StartCreateDt+endCreateDt)
soup = BeautifulSoup(result.text,'lxml-xml')
items = soup.find_all("item")
print(items)

row = []
for item in items:
    row.append(parse())

#pandas 데이터프레임에 넣기
df = pd.DataFrame(row)

#csv 파일로 저장하기
df.to_csv("../data/코로나20210101-20211231.csv",mode='w')
