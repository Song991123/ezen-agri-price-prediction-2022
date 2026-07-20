import requests
from bs4 import BeautifulSoup
import datetime
import time
import random
from tkinter import *
from tkinter.ttk import *
import pandas as pd

#지역 사전 작업
area = {"가락공판장":8808990000855 ,
        "강서공판장":8808990000824 ,
        "경산농협공판장":8808990090986 ,
        "경주농협 공판장":8808990089393  ,
        "광주공판장":8808990000961 ,
        "광주원예농협":8808990081625 ,
        "광주원예농협풍암지점":8808990081588 ,
        "구리공판장":8808990000831 ,
        "구미농협공판장":8808990094342 ,
        "군산원예농협(공판)":8808990065960,
        "금성농협(공판)":8808990639093,
        "김천농협공판장":8808990093536 ,
        "나주배농업협동조합":8808990079882 ,
        "남원원예농협 경매식집하장":8808990831053 ,
        "남지농협공판장":8808990101637 ,
        "대관령원예농협공판사업소":8808990031286 ,
        "대구경북능금농협영천공판장":8808990084732 ,
        "대구경북능금농협포항공판장":8808990084930 ,
        "대구경북원예농협":8808990005256 ,
        "대구공판장":8808990001074 ,
        "대구공판장<태평로분장>":8808990000817,
        "대동농협 공판장":8808990237923  ,
        "대전공판장":8808990000923 ,
        "대전원예농협노은농산물공판장":8808990043517 ,
        "동부농협 경매식집하장":8808990305257 ,
        "동안동농협(공판)":8808990625898 ,
        "목포원예농업협동조합":8808990084107 ,
        "무안농업협동조합":8808990102818 ,
        "밀양농협공판장지점":8808990102269 ,
        "반여공판장":8808990001098 ,
        "부산공판장":8808990001104 ,
        "부산화훼공판장":8808990000800 ,
        "북대구공판장":8808990001081 ,
        "북안동농협(공판)":8808990429236 ,
        "산청농협덕산지점":8808990110639 ,
        "상주농협공판장":8808990095011 ,
        "상주원예농협공판장":8808990096001 ,
        "새청도농협공판장":8808990091785 ,
        "새통영농협 도산지점(공판)":8808990677385  ,
        "서안동농협 농산물(고추)공판장<간>":8808990429823 ,
        "선남농협참외집하장":8808990092669 ,
        "성주조합공동사업법인(공판)":8808990500652 ,
        "성주참외원예농협공판장":8808990093000 ,
        "수원원예농협":8808990016597 ,
        "순천원예농협도매시장지점":8808990072289 ,
        "안동농협공판장":8808990086729 ,
        "안산공판장":8808990000794 ,
        "안양원예농협 공판장":8808990017648 ,
        "안의농협 서하지점(공판)":8808990480602  ,
        "영산농협 산지유통센터(공판)":8808990818160  ,
        "영천농협농산물공판장간이지점":8808990090412 ,
        "예산능금농협공판장":8808990050799 ,
        "용암농협농산물공판장":8808990092522 ,
        "용현농업협동조합 농산물산지유통센터(공판)":8808990839745  ,
        "우포농협 (공판)":8808990790862 ,
        "울산원예농협공판장사업소":8808990105017 ,
        "원주원예농협농산물공판장":8808990030340 ,
        "의성농협농산물공판장 (공판)":8808990471754,
        "이방농협":8808990101392 ,
        "익산원협공판장 (공판)":8808990066851 ,
        "인천원예농협남촌공판장":8808990004174 ,
        "인천원예삼산공판장":8808990004099 ,
        "전주농협공판장":8808990055725 ,
        "전주원협공판장":8808990056333 ,
        "점촌농협경제사업소":8808990096148 ,
        "정읍원예농협공판장":8808990061320 ,
        "제주시농협농산물공판장":8808990113999 ,
        "제천농협공판장":8808990040820 ,
        "진주원예농협공판장":8808990100081 ,
        "창녕농협공판장":8808990101934 ,
        "창원공판장":8808990001128 ,
        "창원원예농협 공판장지점 ":8808990107233 ,
        "천안농협공판장":8808990054476 ,
        "청도농협":8808990091563 ,
        "초전농협집하장":8808990092430 ,
        "춘천원예농협공판장":8808990028323 ,
        "충북원예농협청주공판장":8808990036342 ,
        "충북원협충주공판장":8808990036373 ,
        "충서원협농산물공판장":8808990052090 ,
        "포항농협 농산물공판장 ":8808990089201 ,
        "풍기농협 백신<간>(판매)":8808990495460  ,
        "하양농협 공판장(공판)":8808990831046  ,
        "한국화훼농협 음성화훼유통센터":8808990660684  ,
        "합천동부농협집하장 (공판)":8808990607061}

# 품목 사전 작업
item = {"풋고추"    :"003005005",
        "홍고추"    :"003005008",
        "배추"      :"003003001",
        "상추"      :"003003005"}

######### 날짜 계산 ######### 
now = datetime.datetime.now()     #현재 날짜
pre = datetime.datetime(2017,8,1) #공판장 데이터 시작날
Alldate = (now-pre).days+1          #현재 날짜와 공판장 데이터 시작날까지의 데이터

# selDate  = "selDate="+ year +"%2F"+ month +"%2F"+ date +"&"
selDate  = "selDate="+ str(now.year) +"%2F"+ str(now.month).zfill(2) +"%2F"+ str(now.day).zfill(2) +"&"
print(selDate)

global na_bzplc
global p_item
na_bzplc = "na_bzplc=8808990000855&"
p_item   = "p_item=003005005"
# [메소드] ------------------------------------

def areaValue(event):
    value = area[combo.get()]
    print(combo.get())
    global na_bzplc 
    na_bzplc = "na_bzplc=" + str(value) +"&"
    
def itemValue(event):
    value = item[combo2.get()]
    print(combo2.get())
    global p_item 
    p_item = "p_item=" + value 
    
def crawling():
    global na_bzplc 
    global p_item 
    global selDate
    global now
    global Alldate
    
    now = datetime.datetime.now() 
    agent_head = {
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }
    
    for i in range(1,Alldate+1):
        selDate  = "selDate="+ str(now.year) +"%2F"+ str(now.month).zfill(2) +"%2F"+ str(now.day).zfill(2) +"&"
        
        mURL = "https://newgp.nonghyup.com/ui/ienb/IENB5010L.jsp?mode=1&excel_flag=0&na_bzplcNm=%B1%A4%C1%D6%BF%F8%BF%B9%B3%F3%C7%F9&itemNm=%B9%E8%C3%DF&varItemNm=%BC%B1%C5%C3%C7%CF%BC%BC%BF%E4&"+selDate + na_bzplc + p_item
    #     print(mURL)
        #크롬에서 페이지를 누르는 걸 요청한 것처럼 해주는 코드
        print(mURL)
        response = requests.get(mURL,headers=agent_head)
        #html 내용을 분석하겠다
        soup = BeautifulSoup(response.text, "html.parser")
        content = soup.select(".table_t1")

        table = pd.read_html(response.text, encoding="euc-kr")
        name = list(table[0])
        if(i == 1) :
            data = table[1]
            data.columns = name
            data.drop(['Unnamed: 7'], axis = 1, inplace = True)
            data = data.drop(data[data['경매사'] == "조회된 데이터가 없습니다."].index)
        else:
            try:
                data2 = table[1]
            except IndexError:
                print("======================")
                print("indexError")
                print("======================")
                continue
            data2.columns = name
            data2.drop(['Unnamed: 7'], axis = 1, inplace = True)
            data = data.drop(data[data['경매사'] == "조회된 데이터가 없습니다."].index)
            data = pd.concat([data, data2])
            
        time.sleep( random.uniform(2,6))
        now -= datetime.timedelta(days=1)
    print(data.head(20))
    
    area_name   = combo.get()
    p_item_name = combo2.get()
    filename = str(area_name) + "_" + str(p_item_name) + ".csv"
    data.to_csv(filename,encoding="euc-kr")
    
#[window] -----------------------------------------

window = Tk()
window.title("공판장 크롤링 프로그램")
window.geometry('400x400')
##########################################
# [area]
##########################################
combo = Combobox(window, state="readonly")
combo['values']=tuple(area.keys())
combo.current(0)
combo.grid(column=0, row=0)

combo.bind("<<ComboboxSelected>>", areaValue)
##########################################
# [item]
##########################################
combo2 = Combobox(window, state="readonly")
combo2['values']=tuple(item.keys())
combo2.current(0)
combo2.grid(column=0, row=1)

combo2.bind("<<ComboboxSelected>>", itemValue)
##########################################
btn = Button(window, text="크롤링")
btn.grid(column=1, row=1)

btn.config(command=crawling)
window.mainloop()

#[window] -----------------------------------------