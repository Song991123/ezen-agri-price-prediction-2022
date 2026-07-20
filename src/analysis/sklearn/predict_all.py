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

#def DoPredct(csvname) :
# 경고 off
pd.set_option('mode.chained_assignment',  None)
#CSV 읽기 
#df = pd.read_csv(csvname,encoding="UTF-8")
df  = pd.read_csv('./data/data21.csv', encoding="UTF-8")
df2 = pd.read_csv('./data/data22.csv', encoding="UTF-8")
#df = pd.concat([df1,df2])
#print(df.tail())
#print("=" * 40)

#학습용 데이터만 추출하기
X_colums = [ "date","Tmean_s","subdo_s","Tmin_s","Tmax_s","rain_s" ]
y_colums = [ "price" ]

df = df[X_colums + y_colums]
df2 = df2[X_colums + y_colums]
#print(df.tail())
#print("=" * 40)

#학습 / 훈련 데이터 생성
#독립 변수 X
X_train = df[X_colums]
X_test  = df2[X_colums]

#날짜를 그레고리력으로 변환(1,2,3,4..와 같이 숫자)
X_train["date"] = pd.to_datetime(X_train["date"]).dt.date
X_train["date"] = X_train["date"].map(dt.datetime.toordinal)

X_test["date"] = pd.to_datetime(X_test["date"]).dt.date
X_test["date"] = X_test["date"].map(dt.datetime.toordinal)

#종속 변수 Y
y_train = df["price"]
y_test  = df2["price"]

#x_train, x_test, y_train, y_test = train_test_split(X, y, train_size=0.6, test_size=0.4, shuffle = False,)

X_train_lr = X_train[X_colums]
X_test_lr  = X_test[X_colums]

ridge_alpha = 1 #default 1
lasso_alpha = 0.5 #default 0.1

linear = LinearRegression()
ridge  = Ridge(alpha = ridge_alpha)
lasso  = Lasso(alpha = lasso_alpha)

linear.fit(X_train_lr,y_train)
ridge.fit(X_train_lr,y_train)
lasso.fit(X_train_lr,y_train)

linear_y_hat = linear.predict(X_test_lr)
ridge_y_hat  = ridge.predict(X_test_lr)
lasso_y_hat  = lasso.predict(X_test_lr)

total = X_test["date"].count()

#날짜를 원래대로 변경 
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
plt.title("고냉지 배추 가격예측")
plt.show()
plt.close()

print("Done....")
#DoPredct("./data/고냉지배추.csv")