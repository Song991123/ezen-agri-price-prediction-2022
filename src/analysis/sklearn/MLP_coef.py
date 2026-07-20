import  pandas              as pd
import  matplotlib.pyplot   as plt
import  datetime            as dt
# 상관계수
import  seaborn             as sns
# sklearn 선형 회귀 분석
from    sklearn.linear_model    import LinearRegression
# statsmodel 회귀 분석
import  statsmodels.api     as sm

## ===========================================================================#
## initialize start ==========================================================#

# 파일 이름 -------------------------------------------------------------------
file = "result.csv"
#-----------------------------------------------------------------------------#

## 기상조건과 거래량, 평균가격의 상관계수용 컬럼 ------------------------------
cols     = ['Tmean','subdo','Tmin','Tmax','rain','amount','price']
cols_all = ['Tmean_PM','Tmean','subdo_PM','subdo','Tmin_PM','Tmin',
        'Tmax_PM','Tmax','rain_PM', 'rain','amount', 'price']
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
# 기존 index를 삭제하고, 'date'를 인덱스로 변경
# 기존 'date' 컬럼은 삭제
# 새로 지정된 index로 정렬
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
def split_Data(DataFrame, target_date) :
    train_data = DataFrame.loc[DataFrame["date"] < target_date][cols]
    test_data  = DataFrame.loc[DataFrame["date"] > target_date][cols]
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

# functions end ==============================================================#
#=============================================================================#

## ===========================================================================#
## main start ================================================================#

# 파일에서 데이터를 불러와 DF에 넣는다
df = make_DF(file)
print(df.head())
print(target_date)

# 기준 날짜로 DataFrame를 쪼갬
train_data, test_data = split_Data(df, target_date)
#print('train_data \n{}\ntest_data \n{}\n'.format(train_data, test_data))

# 컬럼 재설정 / 독립변수에서 종속변수(가격)을 뺀다
cols_X = ['subdo','Tmax','rain']
cols_y = 'price'

# train data를 독립변수와 종속변수로 나눈다
X_train, y_train = set_Xy(train_data, cols_X, cols_y)
#print('X_train \n{}\ny_train \n{}\n'.format(X_train, y_train))

# test data를 독립변수와 종속변수로 나눈다
X_test, y_test = set_Xy(test_data, cols_X, cols_y)
#print('X_test \n{}\ny_test \n{}\n'.format(X_test, y_test))

# LinearRegression 선형회귀 분석 수행
lr = train_LR(X_train, y_train)
print('LinearRegression train score : ', lr.score(X_train, y_train))
print('LinearRegression test  score : ', lr.score(X_test, y_test))

# statsmodel 라이브러리로 회귀 분석을 수행합니다.
model = train_OLS(X_train, y_train)

# 회귀 계수를 DF로 변환
coefs_df = make_coefs_df(model)
x_labels = model.params.index.tolist()

# 회귀 계수를 출력합니다.
draw_bar_coefs(coefs_df,x_labels)

# main end ===================================================================#
#=============================================================================#