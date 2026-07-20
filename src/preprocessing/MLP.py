import  pandas              as pd
import  matplotlib.pyplot   as plt
import  datetime            as dt
from    math                import sqrt
# 상관계수
import  seaborn             as sns
# sklearn 선형 회귀 분석
from    sklearn.linear_model    import LinearRegression
from    sklearn.model_selection import train_test_split
from    sklearn.metrics         import mean_squared_error
# statsmodel 회귀 분석
import  statsmodels.api     as sm

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
## columns to do scaling ------------------------------------------------------
#cols_scaling = ['Tmean','subdo','Tmin','Tmax','rain','amount','price']
cols_scaling = ['Tmean','subdo','Tmin','Tmax','rain','amount']
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
## 기준 날짜 설정 -------------------------------------------------------------
target_date = dt.datetime.strftime( dt.datetime(year=2022, month=9, day=1), '%Y-%m-%d')
#-----------------------------------------------------------------------------#

# initialize end =============================================================#
#=============================================================================#

## ===========================================================================#
## functions start ===========================================================#

## plot 꾸밈 ------------------------------------------------------------------
def set_sns(figsize=(20,20)) :
    plt.figure( figsize=figsize, dpi = 300 )
    sns.set( font = "Malgun Gothic", font_scale = 1.2,
             style = "whitegrid", context = "notebook",
             rc = {"axes.unicode_minus" : False})
#-----------------------------------------------------------------------------#

## heatmap 그리는 함수 ---------------------------------------------------------
def draw_heatMap(DataFrame,columns=None) :
    set_sns()
    if columns :
        sns.heatmap(DataFrame,
                    cbar=True,
                    annot=True,
                    square=True,
                    fmt='.3f',
                    annot_kws={'size': 15},
                    yticklabels=columns, xticklabels=columns)
    else :
        sns.heatmap(DataFrame,
                    cbar=True,
                    annot=True,
                    square=True,
                    fmt='.3f',
                    annot_kws={'size': 15})
    plt.show()
#-----------------------------------------------------------------------------#

## pairplot 그리는 함수 --------------------------------------------------------
def draw_pairplot(DataFrame,columns) :
    set_sns()
    sns.pairplot(DataFrame[columns], height =2.5)
    plt.show()
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

## 파일에서 데이터를 불러와 DF로 합친다 ------------------------------------------
def make_DF(files) :
    result = pd.DataFrame()
    for file in files :
        data   = pd.read_csv(file, encoding='UTF-8')
        result = pd.concat([result, data])
    # 이름 없는 첫번째 컬럼 삭제
    result = result.drop(result.columns[[0]], axis=1)
    # 파일마다 index가 리셋되기에, 최종 DataFrame에서는 index를 reset
    result = result.reset_index(drop=True)
    return result
#-----------------------------------------------------------------------------#

## 문자열인 컬럼을 날짜 형식으로 변환 --------------------------------------------
def str_to_Date(DataFrame,column) :
    DataFrame[column] = DataFrame[column].astype("str")
    DataFrame[column] = pd.to_datetime(DataFrame[column]).dt.date
#-----------------------------------------------------------------------------#

## index 재 설정 --------------------------------------------------------------
# 기존 index를 삭제하고, 'date'를 인덱스로 변경
# 기존 'date' 컬럼은 삭제하지 않고 남겨둔다
# 새로 지정된 index로 정렬
def reset_index(DataFrame, date=None , drop=False) :
    DataFrame.reset_index( drop = True, inplace = True )
    if date :
        DataFrame.set_index('date', drop=drop, inplace=True)
    DataFrame.sort_index(inplace=True)
#-----------------------------------------------------------------------------#

## interpolate 결측치 보간 -----------------------------------------------------
# 시계열 index를 바탕으로, 유효한 값으로 둘러싸인,
# 한도 5의 범위로, 앞뒤 값을 바탕으로 보간 계산
def interpolate(DataFrame, columns, limit_num) :
    DataFrame[columns] = DataFrame[columns].interpolate( method='time', limit=limit_num, limit_direction='both', limit_area='inside')
#-----------------------------------------------------------------------------#

## scaling --------------------------------------------------------------------
# z- = (x - x평균)/x표준편차
def standard_scaling(DataFrame, columns) :
    for column in columns :
        series_mean = DataFrame[column].mean()
        series_std  = DataFrame[column].std()
        DataFrame[column] = DataFrame[column].apply(lambda x : (x-series_mean)/series_std)
#-----------------------------------------------------------------------------#

## fill zero ------------------------------------------------------------------
# 나머지 0으로 채우기
def fillZero(DataFrame,columns) :
    DataFrame[columns] = DataFrame[columns].fillna(0)
#-----------------------------------------------------------------------------#

## split Dataframe for train use date -----------------------------------------
# 기준 날짜로 DataFrame를 쪼갬
def split_Data(DataFrame, target_date, columns) :
    train_data = DataFrame.loc[DataFrame["date"] < target_date][columns]
    test_data  = DataFrame.loc[DataFrame["date"] >= target_date][columns]
    return train_data, test_data
#-----------------------------------------------------------------------------#

## split dataframe for X, y ---------------------------------------------------
# 독립변수와 종속변수를 나눈다
def set_Xy(train_data, X_cols, y_col) :
    X_train = train_data[X_cols]
    y_train = train_data[y_col]
    return X_train, y_train
#-----------------------------------------------------------------------------#

## LinearRegression -----------------------------------------------------------
# 선형회귀 수행하고 학습계수를 출력한다.
def train_LR(X_train, y_train) :
    # 선형회귀
    lr = LinearRegression()
    # 선형 회귀 학습
    lr.fit(X_train, y_train)
    # 학습 계수 출력
    print(lr.coef_)
    return lr
#-----------------------------------------------------------------------------#

## statsmodel OLS -------------------------------------------------------------
# statsmodel 라이브러리로 회귀 분석을 수행한다.
def train_OLS(X_train, y_train) :
    X_train = sm.add_constant(X_train)
    model = sm.OLS(y_train, X_train).fit()
    print(model.summary())
    return model
#-----------------------------------------------------------------------------#

## make DataFrame from coefs --------------------------------------------------
# 회귀 계수를 DF로 변환
def make_coefs_df(model) :
    # 회귀 계수를 리스트로 반환합니다.
    coefs = model.params.tolist()
    # 변수명을 리스트로 반환합니다.
    x_labels = model.params.index.tolist()
    # DF 생성
    coefs_df = pd.DataFrame({'coef':coefs}, index=x_labels)
    print('coefs_df \n', coefs_df)
    return coefs_df
#-----------------------------------------------------------------------------#

## draw coefs bar -------------------------------------------------------------
# 회귀 계수를 출력합니다.
def draw_bar_coefs(coefs_df,x_labels) :
    plt.bar(x_labels, coefs_df['coef'])
    #plt.plot(x_labels, coefs_df['coef'])
    plt.title('feature_coef_graph')
    plt.xlabel('x_features')
    plt.ylabel('coef')
    plt.show()
    plt.close()
#-----------------------------------------------------------------------------#

## preprocessing --------------------------------------------------------------
# 전처리
def preprocessing(DataFrame) :
    # 날짜 형식으로 변환
    str_to_Date(DataFrame,'date')
    # index 리셋 후 정렬
    reset_index(DataFrame)
    # 결측치 보간
    interpolate(DataFrame, 'amount', 3)
    interpolate(DataFrame, cols_price, 3)
    # 나머지 0으로 채우기
    fillZero(DataFrame,'amount')
    fillZero(DataFrame,cols_price)
    # 피처 스케일링하기
    standard_scaling(DataFrame, cols_scaling)
#-----------------------------------------------------------------------------#