import os
import sys
import urllib.request
import datetime
import time
import json
import pymysql

def get_request_url(url):
    req = urllib.request.Request(url)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print ("[%s] Url Request Success" % datetime.datetime.now())  #// % 서식에 요소가 1개일때는 괄호를 안해줘도 된다.
            return response.read().decode('utf-8') #// 정보를 utf-8로 리턴
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

#==

#[CODE 1]
def getNatVisitor(yyyymm, nat_cd, ed_cd):
    access_key= "" #//개인 인증키
    end_point = "http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList" #//개발 가이드 -> 요청주소
    parameters = "?_type=json&serviceKey=" + access_key
    parameters += "&YM=" + yyyymm
    parameters += "&NAT_CD=" + nat_cd
    parameters += "&ED_CD=" + ed_cd

    url = end_point + parameters

    retData = get_request_url(url)

    if (retData == None):
        return None
    else:
        return json.loads(retData)

#==

def mysql_save(krName, yyyymm, iTotalVisit):
    conn = pymysql.connect(host='bethepresent.caihya0i6v5g.ap-northeast-2.rds.amazonaws.com', user='user', password='ckm15963',db='sampledb', charset='utf8') #//mysql 계정정보 입력
    #conn=MySQLdb.connect("localhost","pgm","1234","pydb",charset='utf8') //pymysql 대체
    cursor = conn.cursor()
    sql="insert into totVisit(krname,ym,totalvisit) values('%s','%s','%s')" %(krName,yyyymm,iTotalVisit)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

#==

def main():
    jsonResult = []

    #중국: 112 / 일본: 130 / 미국: 275
    national_code = "275"
    ed_cd = "E"

    nStartYear = 2011
    nEndYear = 2017
    krName=""
    visit_list=[] #// 오라클에서 리스트로 세이브 하기 위한 준비

    for year in range(nStartYear, nEndYear):
        for month in range(1, 13):
            yyyymm = "{0}{1:0>2}".format(str(year), str(month))
            jsonData = getNatVisitor(yyyymm, national_code, ed_cd)

            print (json.dumps(jsonData,indent=4, sort_keys=True,ensure_ascii=False))
            if (jsonData['response']['header']['resultMsg'] == 'OK'):
                krName = jsonData['response']['body']['items']['item']["natKorNm"]
                krName = krName.replace(' ', '')
                iTotalVisit = jsonData['response']['body']['items']['item']["num"]
                print('%s_%s : %s' %(krName, yyyymm, iTotalVisit))
                jsonResult.append({'nat_name': krName, 'nat_cd': national_code, 'yyyymm': yyyymm, 'visit_cnt': iTotalVisit})
                mysql_save(krName,yyyymm,iTotalVisit)

    cnVisit = []
    VisitYM = []
    index = []
    i = 0
    for item in jsonResult:
        index.append(i)
        cnVisit.append(item['visit_cnt'])
        VisitYM.append(item['yyyymm'])
        i = i + 1

    with open('%s(%s)_해외방문객정보_%d_%d.json'% (krName, national_code, nStartYear, nEndYear-1), 'w', encoding='utf8') as outfile:
        retJson = json.dumps(jsonResult,indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(retJson)