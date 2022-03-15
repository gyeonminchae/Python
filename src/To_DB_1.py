import requests
from bs4 import BeautifulSoup as bs
import json
import pandas as pd
import pymysql

serviceKey='본인 서비스키'
rType='json'
num='32'
url='http://apis.data.go.kr/6260000/FestivalService/getFestivalKr?serviceKey='+serviceKey+'&pageNo=1&numOfRows='+num+'&resultType='+rType

res=requests.get(url).text
data=json.loads(res)
fests=data["getFestivalKr"]["item"]
fest_list=[]
i=0
for fest in fests:
    festival_title=fest["MAIN_TITLE"]
    festival_addr=fest["ADDR1"]
    if festival_addr == '':
        festival_addr='주소정보없음'
    usage_day=fest["USAGE_DAY"]
    if usage_day == '':
        usage_day='시간정보없음'
    festival_area=fest["GUGUN_NM"]
    homepage=fest["HOMEPAGE_URL"]
    if homepage == '':
        homepage='홈페이지없음'
    thumb=fest["MAIN_IMG_THUMB"]
    traffic=fest["TRFC_INFO"]
    if traffic == '':
        traffic='교통정보없음'
    lat=fest["LAT"]
    lng=fest["LNG"]
    #print(festival_title,festival_addr,usage_day,festival_area,homepage,thumb,traffic)
    fest_list.append(tuple([festival_title,festival_addr,usage_day,festival_area,homepage,thumb,traffic,lat,lng]))
    i+=1
    print(i)
print(fest_list)

df=pd.DataFrame(fest_list,columns=['festival_title','festival_addr','usage_day','festival_area','homepage','thumb','traffic','lat','lng'])

def mysql_save(fest_list):
    conn=pymysql.connect(host='bethepresent.caihya0i6v5g.ap-northeast-2.rds.amazonaws.com',
                        user='user',
                        password='ckm15963',
                        db='sampledb',
                        charset='utf8')
    cursor=conn.cursor()
    sql="insert into festival(festival_title,festival_addr,usage_day,festival_area,homepage,thumb,traffic,lat,lng) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.executemany(sql,fest_list)
    conn.commit()
    conn.close()
mysql_save(fest_list)

