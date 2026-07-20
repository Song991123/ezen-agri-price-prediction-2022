import requests 
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc
from sklearn.linear_model import LinearRegression
import datetime as dt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
import statsmodels.formula.api as smf
from datetime import datetime
from tkinter import *
from tkinter.ttk import *
from decimal import Decimal

pd.set_option('mode.chained_assignment',  None)

# [변수 초기 설정] ------------------------------------

global percent
percent = Decimal('0.3')

# [메소드] =========================================

# 비율 초기화(0.3)
def percent_set():
    global percent
    percent = Decimal('0.3')
    print(Decimal('1.0')-percent)

# 트레이닝 비율 증가
def percent_plus():
    global percent
    if percent >= 0.05:
        percent -= Decimal('0.05')
    print(Decimal('1.0')-percent)

# 트레이닝 비율 감소   
def percent_minus():
    global percent
    if percent < 1:
        percent += Decimal('0.05')
    
    print(Decimal('1.0')-percent)
    
    
def predict():
    
    # 독립 변수 설정 ----------------------------
    '''
    date	Tmin	Tmax	Tmean	Hmax	price	Tmin_s	Tmax_s	Tmean_s	Hmax_s

    '''
    X_colums = [ "date" ]
    
    CheckList = [CheckVar1.get(), CheckVar2.get(), CheckVar3.get(),CheckVar4.get(),
                 CheckVar5.get(),CheckVar6.get(),CheckVar7.get(),CheckVar8.get()]
    
    for value in CheckList:
        if value!= "":
            X_colums.append(value)
    print(X_colums)
    
    y_colums = [ "price" ]
    
    # csv 파일 읽기 ----------------------------
    df  = pd.read_csv('./lettuce_ss13.csv', encoding="UTF-8")
    df  = pd.read_csv('./data_ss13.csv', encoding="UTF-8")
    df = df[X_colums + y_colums]

    #학습 / 훈련 데이터 생성  ----------------------------
    #독립 변수 X
    X = df[X_colums]

    #날짜를 그레고리력으로 변환(1,2,3,4..와 같이 숫자) 
    X["date"] = pd.to_datetime(X["date"]).dt.date
    X["date"] = X["date"].map(dt.datetime.toordinal)

    #종속 변수 Y
    y = df["price"]

    global percent
    baserow = df['date'].count() - int(df['date'].count()*percent)
    
    X_train = X.iloc[0:baserow]
    X_test = X.iloc[baserow:]
    y_train = y.iloc[0:baserow]
    y_test = y.iloc[baserow:]


    X_train_lr = X_train[X_colums]
    X_test_lr  = X_test[X_colums]

    # 선형 회귀 모델 선언 ----------------------------

    ridge_alpha = 1 #default 1
    lasso_alpha = 0.5 #default 0.1
    
    linear = LinearRegression()
    ridge  = Ridge(alpha = ridge_alpha)
    lasso  = Lasso(alpha = lasso_alpha)
    
    
    # 선형 회귀 모델 학습 ----------------------------
    
    linear.fit(X_train_lr,y_train)
    ridge.fit(X_train_lr,y_train)
    lasso.fit(X_train_lr,y_train)

    # 선형 회귀 모델 예측 ----------------------------

    linear_y_hat = linear.predict(X_test_lr)
    ridge_y_hat  = ridge.predict(X_test_lr)
    lasso_y_hat  = lasso.predict(X_test_lr)

    total = X_test["date"].count()

    #날짜를 원래대로 변경 ----------------------------
    X_test["date"] = X_test["date"].map(dt.datetime.fromordinal)

    for i in range(0,total) :    
        print(str(X_test.iloc[i]["date"])[0:10],end="  :  ")
        print(y_test.iloc[i],end="  :  ")
        print(linear_y_hat[i])
        print(ridge_y_hat[i])
        print(lasso_y_hat[i])
        print("=" * 30)

    #그래프 그리기
    plt.figure(figsize=(10,4), dpi=300)
    plt.rc('font', family='Malgun Gothic')
    plt.plot(X_test["date"].tolist(),y_test.tolist(), label="실제가격")
    plt.plot(X_test["date"].tolist(),linear_y_hat, label="linear")
    plt.plot(X_test["date"].tolist(),ridge_y_hat, label="ridge")
    plt.plot(X_test["date"].tolist(),lasso_y_hat, label="lasso")
    plt.xlabel("날짜")
    plt.ylabel("가격")
    plt.legend()
    plt.title("전주 상추 가격예측")
    plt.show()
    plt.close()

    #그래프 그리기
    plt.figure(figsize=(10,4), dpi=300)
    plt.rc('font', family='Malgun Gothic')
    plt.plot(X_test["date"][-30:].tolist(),y_test[-30:].tolist(), label="실제가격")
    plt.plot(X_test["date"][-30:].tolist(),linear_y_hat[-30:], label="linear")
    plt.plot(X_test["date"][-30:].tolist(),ridge_y_hat[-30:], label="ridge")
    plt.plot(X_test["date"][-30:].tolist(),lasso_y_hat[-30:], label="lasso")
    plt.xlabel("날짜")
    plt.ylabel("가격")
    plt.legend()
    plt.title("전주 상추 가격예측")
    plt.show()
    plt.close()


    print(">> Done....")
    print("=" * 30)
    print("percent : (", Decimal('1.0')-percent, ":" , percent, ")")
    print("train size : ", len(X_train))
    print("test size : ", len(X_test))
    print("colum : ", X_colums)
    print("=" * 30)

#[window] -----------------------------------------

window = Tk()
window.title("농산물 가격 예측 시스템")
window.geometry('700x150')
##########################################
# [label]
##########################################
label1 = Label(window, text="피처 : ")
label1.grid(column=0, row=0)
label2 = Label(window, text="트레이닝 비율 : ")
label2.grid(column=0, row=1)

##########################################
# [checkbutton]
##########################################
CheckVar1=StringVar()
CheckVar2=StringVar()
CheckVar3=StringVar()
CheckVar4=StringVar()
CheckVar5=StringVar()
CheckVar6=StringVar()
CheckVar7=StringVar()
CheckVar8=StringVar()

C1 = Checkbutton(window, text = "Tmin_s", variable = CheckVar1, onvalue='Tmin_s', offvalue="")
C2 = Checkbutton(window, text = "Tmax_s", variable = CheckVar2, onvalue='Tmax_s', offvalue="")
C3 = Checkbutton(window, text = "Tmean_s", variable = CheckVar3, onvalue='Tmean_s', offvalue="")
C4 = Checkbutton(window, text = "Hmax_s", variable = CheckVar4, onvalue='Hmax_s', offvalue="")
C5 = Checkbutton(window, text = "Tmin", variable = CheckVar5, onvalue='Tmin', offvalue="")
C6 = Checkbutton(window, text = "Tmax", variable = CheckVar6, onvalue='Tmax', offvalue="")
C7 = Checkbutton(window, text = "Tmean", variable = CheckVar7, onvalue='Tmean', offvalue="")
C8 = Checkbutton(window, text = "Hmax", variable = CheckVar8, onvalue='Hmax', offvalue="")

C1.grid(column=1, row=0)
C2.grid(column=2, row=0)
C3.grid(column=3, row=0)
C4.grid(column=4, row=0)
C5.grid(column=5, row=0)
C6.grid(column=6, row=0)
C7.grid(column=7, row=0)
C8.grid(column=8, row=0)

##########################################
# [button]
##########################################
btn = Button(window, text="예측")
btn.grid(column=8, row=2)
btn.config(command=predict)
btn2 = Button(window, text="+")
btn2.grid(column=1, row=1)
btn2.config(command=percent_plus)
btn3 = Button(window, text="-")
btn3.grid(column=2, row=1)
btn3.config(command=percent_minus)
btn3 = Button(window, text="초기화")
btn3.grid(column=3, row=1)
btn3.config(command=percent_set)




window.mainloop()
#[window] -----------------------------------------
