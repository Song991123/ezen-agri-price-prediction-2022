import  pandas              as pd
import  matplotlib.pyplot   as plt
import  datetime            as dt
# 상관계수
import  seaborn             as sns
# sklearn 선형 회귀 분석
from    sklearn.linear_model    import LinearRegression

## ===========================================================================#
## initialize start ==========================================================#

# 파일 목록 -------------------------------------------------------------------
file = "result.csv"
#-----------------------------------------------------------------------------#
## 기상조건과 거래량, 평균가격의 상관계수용 컬럼 ------------------------------
cols     = ['Tmean','subdo','Tmin','Tmax','rain','amount','price']
#-----------------------------------------------------------------------------#
## 기준 날짜 설정 -------------------------------------------------------------
target_date = dt.datetime.strftime( dt.datetime(year=2022, month=9, day=1), '%Y-%m-%d')
#-----------------------------------------------------------------------------#

# initialize end =============================================================#
#=============================================================================#

## ===========================================================================#
## functions start ===========================================================#

## 파일에서 데이터를 불러와 DF로 합친다 ---------------------------------------
def make_DF(file) :
    result = pd.read_csv(file)
    reset_index(result)
    return result
#-----------------------------------------------------------------------------#

## index 재 설정 --------------------------------------------------------------
def reset_index(DataFrame) :
    DataFrame.reset_index( drop = True, inplace = True )
    DataFrame.set_index('date', drop=False, inplace=True)
    DataFrame.sort_index(inplace=True)
#-----------------------------------------------------------------------------#

## plot 꾸밈 ------------------------------------------------------------------
def set_sns() :
    plt.figure( dpi = 300 )
    sns.set( font = "Malgun Gothic", font_scale = 1.2,
             style = "whitegrid", context = "notebook",
             rc = {"axes.unicode_minus" : False, "figure.figsize" : (16,9)})
#-----------------------------------------------------------------------------#

## split Dataframe for train use date -----------------------------------------
# 기준 날짜로 DataFrame를 쪼갬
def split_Data(DataFrame, target_date, columns) :
    train_data = DataFrame.loc[DataFrame["date"] < target_date][columns]
    test_data  = DataFrame.loc[DataFrame["date"] > target_date][columns]
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

# functions end ==============================================================#
#=============================================================================#

## ===========================================================================#
## main start ================================================================#

# 파일에서 데이터를 불러와 DF에 넣는다
df = make_DF(file)

# 기준 날짜로 DataFrame를 쪼갬
train_data, test_data = split_Data(df, target_date, cols)

# 컬럼 재설정 / 독립변수에서 종속변수(가격)을 뺀다
cols_X = ['subdo','Tmax','rain']
#cols_X = ['Tmean','subdo','Tmin','Tmax','rain','amount','price']


# train data를 독립변수와 종속변수로 나눈다
X_train, y_train = set_Xy(train_data, cols_X, 'price')

# test data를 독립변수와 종속변수로 나눈다
X_test, y_test = set_Xy(test_data, cols_X, 'price')

# LinearRegression 선형회귀 분석 수행
lr = train_LR(X_train, y_train)
print('LinearRegression train score : ', lr.score(X_train, y_train))
print('LinearRegression test score : ',  lr.score(X_test,  y_test ))

# 다중 공산성 확인
from statsmodels.stats.outliers_influence import variance_inflation_factor
# 피처마다의 VIF 계수를 출력한다
# VIF Variance Inflation Factor 분산팽창요인
# 10-15를 넘으면 문제가 있음
X = X_train
vif = pd.DataFrame()
vif['VIF Factor'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
vif['features'] = X.columns
print(vif.round(1))

# main end ===================================================================#
#=============================================================================#