import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

## ===========================================================================#
## functions start ===========================================================#
## plot 꾸밈 ------------------------------------------------------------------
def set_sns() :
    plt.figure( dpi = 300 )
    sns.set( font = "Malgun Gothic", font_scale = 1.2,
             style = "whitegrid", context = "notebook",
             rc = {"axes.unicode_minus" : False, "figure.figsize" : (16,9)})
#-----------------------------------------------------------------------------#
## heatmap 그리는 함수 --------------------------------------------------------
def draw_heatMap(DataFrame,columns) :
    set_sns()
    sns.heatmap(DataFrame,
                cbar=True,
                annot=True,
                square=True,
                fmt='.2f',
                annot_kws={'size': 15},
                yticklabels=columns, xticklabels=columns)
    plt.show()
#-----------------------------------------------------------------------------#
## pairplot 그리는 함수 -------------------------------------------------------
def draw_pairplot(DataFrame,columns) :
    set_sns()
    sns.pairplot(DataFrame[columns], height =2.5)
    plt.show()
#-----------------------------------------------------------------------------#
## 파일에서 데이터를 불러와 DF로 합친다 ---------------------------------------
def make_DF(files) :
    result = pd.DataFrame()
    for file in files :
        data   = pd.read_csv(file)
        result = pd.concat([result, data])
    # 파일마다 index가 리셋되기에, 최종 DataFrame에서는 index를 reset
    result = result.reset_index(drop=True)
    return result
#-----------------------------------------------------------------------------#
## 문자열인 컬럼을 날짜 형식으로 변환 -----------------------------------------
def str_to_Date(DataFrame,column) :
    DataFrame[column] = DataFrame[column].astype("str")
    DataFrame[column] = pd.to_datetime(DataFrame[column])
#-----------------------------------------------------------------------------#
## index 재 설정 --------------------------------------------------------------
# 기존 index를 삭제하고, 'date'를 인덱스로 변경
# 기존 'date' 컬럼은 삭제하지 않고 남겨둔다
# 새로 지정된 index로 정렬
def reset_index(DataFrame) :
    DataFrame.reset_index( drop = True, inplace = True )
    DataFrame.set_index('date', drop=False, inplace=True)
#    DataFrame.set_index('date', drop=True, inplace=True)
    DataFrame.sort_index(inplace=True)
#-----------------------------------------------------------------------------#
## 2x2 lineplot ---------------------------------------------------------------
def draw_lineplot(DataFrame, xtick, yticks) :
    set_sns()
    fig, ax = plt.subplots(nrows=2, ncols=2)
    fig.set_size_inches(16,9)
    sns.lineplot(x=DataFrame[xtick], y=DataFrame[yticks[0]], ax=ax[0][0])
    sns.lineplot(x=DataFrame[xtick], y=DataFrame[yticks[1]], ax=ax[0][1])
    sns.lineplot(x=DataFrame[xtick], y=DataFrame[yticks[2]], ax=ax[1][0])
    sns.lineplot(x=DataFrame[xtick], y=DataFrame[yticks[3]], ax=ax[1][1])
    plt.show()
#-----------------------------------------------------------------------------#
## interpolate 결측치 보간 ----------------------------------------------------
# 시계열 index를 바탕으로, 유효한 값으로 둘러싸인,
# 한도 5의 범위로, 앞뒤 값을 바탕으로 보간 계산
def interpolate(DataFrame, columns, limit_num) :
    DataFrame[columns] = DataFrame[columns].interpolate( method='time', limit=limit_num, limit_direction='both', limit_area='inside')
#-----------------------------------------------------------------------------#

# functions end ==============================================================#
#=============================================================================#

## ===========================================================================#
## initialize start ==========================================================#

# 파일 목록 -------------------------------------------------------------------
files = ["data_2022.csv",
         "data_2021.csv" ]
#-----------------------------------------------------------------------------#
## 기상조건과 거래량, 평균가격의 상관계수용 컬럼 ------------------------------
cols     = ['Tmean','subdo','Tmin','Tmax','rain','amount','price']
cols_all = ['Tmean_PM','Tmean','subdo_PM','subdo','Tmin_PM','Tmin',
        'Tmax_PM','Tmax','rain_PM', 'rain','amount', 'price']
#-----------------------------------------------------------------------------#
## 평균가격과 지역가격의 상관계수용 컬럼들 ------------------------------------
cols_price = [ 'price', 'seoul', 'busan', 'daegu', 'gwangju', 'daejun']
#-----------------------------------------------------------------------------#
## 그래프 출력을 위한 cols 한글 이름 ------------------------------------------
cols_view = ['평균기온','습도','최저기온','최고기온','강우량','거래량','평균가격']
cols_all_view = ['평균기온(평년비교)','평균기온','습도(평년비교)','습도',
             '최저기온(평년비교)','최저기온','최고기온(평년비교)','최고기온',
             '강우량(평년비교)', '강우량','거래량', '평균가격']
cols_price_view = [ '평균가격', '서울', '부산', '대구', '광주', '대전' ]
#-----------------------------------------------------------------------------#
# initialize end =============================================================#
#=============================================================================#

## ===========================================================================#
## main start ================================================================#

# 파일에서 데이터를 불러와 DF에 넣는다
df = make_DF(files)
# 날짜 형식으로 변환
str_to_Date(df,'date')
# index 리셋 후 정렬
reset_index(df)

# 결측치 보간
interpolate(df, 'amount', 3)
interpolate(df, cols_price, 3)

"""
df.drop(['date'], axis=1 , inplace=True)
print(df.head())

import numpy as np  # 넘파이 호출 
import statsmodels.api as sm # statsmodels 호출 
from statsmodels.tsa.seasonal import seasonal_decompose # 데이터 필터 라이러리 호출 

set_sns()

result = seasonal_decompose(df[cols], model = 'Mulitiolicative', extrapolate_trend=30) # 대략 1달치 기준으로 데이터 분해 실시  
result.plot()

from statsmodels.tsa.stattools import adfuller #ADF Test를 위한 함수 호출 

st_result = adfuller(df['Tmean'])
print(st_result)

df['1st diff'] = df['Tmean']- df['Tmean'].shift(1)

# diff 값으로 계절성 값 계산 
df['seasonal diff'] = df['1st diff'] - df['1st diff'].shift(30)
st_result = adfuller(df['seasonal diff'].dropna()) # 차분에 의해 발생한 Na 값을 제거 하고 진행 
print(st_result[1])
df['seasonal diff'].plot()

# ACF 그려 보기 / PACF
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf # acf 와 pacf 시각화를 위한 라이브러리 호출 
plot_acf(df['Tmean'])
plot_pacf(df['Tmean'])

# ACF 그려 보기 / PACF (계절성)
plot_acf(df['seasonal diff'].dropna())
plot_pacf(df['seasonal diff'].dropna())

# Arima 예측 
from statsmodels.tsa.arima_model import ARIMA
model = ARIMA(df['Tmean'], order=(0,2,1))
model_fit = model.fit(trend='nc',full_output=True, disp=1)
print(model_fit.summary())

# 시각화 하기 
model_fit.plot_predict()

'''
# 나머지 0으로 채우기
df['amount'] = df['amount'].fillna(0)
df[cols_price] = df[cols_price].fillna(0)

# 평균 가격과, 지역별 가격의 상관계수
corr = df[cols_price].corr(method = 'pearson')
# heatmap, pairplot 
draw_heatMap(corr,cols_price_view)
draw_pairplot(df,cols_price)

# 기상조건과 물량, 가격의 상관계수
corr = df[cols].corr(method = 'pearson')
# heatmap, pairplot 
draw_heatMap(corr,cols_view)
draw_pairplot(df,cols)

# 2x2 lineplot으로 시간별 피쳐값들 그래프로 그리기
draw_lineplot(df,'date',['Tmean','price','amount','seoul'])
"""

from statsmodels.tsa.statespace.sarimax import SARIMAX
import numpy as np

import itertools
p = d = q = range(0, 3)
pdq = list(itertools.product(p,d,q))
seasonal_pdq = [(x[0],x[1],x[2],364) for x in list(itertools.product(p,d,q))]
best_aic = np.inf
best_pdq = None
best_seasonal_pdq = None
tmp_model = None
best_model = None

for param in pdq :
    for param_seasonal in seasonal_pdq :
        try :
            tmp_model = SARIMAX(endog=df['Tmean'], exog=None, order = param,
                                  seasonal_order = param_seasonal,
                                  enforce_stationarity=True,
                                  enforce_invertibility=True)
            res = tmp_model.fit()
            print("SARIMAX{}x{} year model - AIC:{}".format(param, param_seasonal, res.aic))
            if res.aic < best_aic :
                best_aic = res.aic
                best_pdq = param
                best_seasonal_pdq = param_seasonal
                best_model = tmp_model
        except :
            continue
print("Best SARIMAX{}x{} year model - AIC:{}".format(best_pdq, best_seasonal_pdq, best_aic))

'''
mdl = SARIMAX(endog=df['Tmean'], order=(2,1,2),
              seasonal_order=(0,0,0,365),
              enforce_stationarity=True,
              enforce_invertibility=True)
res = mdl.fit()
res.summary()
'''

#https://goodboychan.github.io/python/datacamp/time_series_analysis/2020/06/16/02-Seasonal-ARIMA-Models.html#Seasonal-ACF-and-PACF
            
# main end ===================================================================#
#=============================================================================#