import  pandas              as pd
import  datetime            as dt

## ===========================================================================#
## initialize start ==========================================================#

# 파일 이름 -------------------------------------------------------------------
# 읽어올 파일 목록
files = ["data_2022.csv",
         "data_2021.csv" ]
# 저장할 파일 이름
filename = "result.csv"
#-----------------------------------------------------------------------------#

## columns to do scaling ------------------------------------------------------
cols_scaling = ['subdo','Tmax','rain','amount']
cols_scaling = ['Tmean','subdo','Tmin','Tmax','rain','amount']
#-----------------------------------------------------------------------------#

# initialize end =============================================================#
#=============================================================================#

## ===========================================================================#
## functions start ===========================================================#

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
# 기존 'date' 컬럼은 삭제
# 새로 지정된 index로 정렬
def reset_index(DataFrame) :
    DataFrame.reset_index( drop = True, inplace = True )
    DataFrame.set_index('date', drop=True, inplace=True)
    DataFrame.sort_index(inplace=True)
#-----------------------------------------------------------------------------#

## interpolate 결측치 보간 ----------------------------------------------------
# 시계열 index를 바탕으로, 유효한 값으로 둘러싸인,
# 한도 5의 범위로, 앞뒤 값을 바탕으로 보간 계산
def interpolate(DataFrame, columns, limit_num, round=None) :
    DataFrame[columns] = DataFrame[columns].interpolate( method='time', limit=limit_num, limit_direction='both', limit_area='inside').round(round)
#-----------------------------------------------------------------------------#

## scaling --------------------------------------------------------------------
# z- = (x - x평균)/x표준편차
# 소수점 4자리까지만
def standard_scaling(DataFrame, columns) :
    for column in columns :
        series_mean = DataFrame[column].mean()
        series_std  = DataFrame[column].std()
        DataFrame[column] = DataFrame[column].apply(lambda x : (x-series_mean)/series_std).round(4)
#-----------------------------------------------------------------------------#

## fill zero ------------------------------------------------------------------
# 나머지 0으로 채우기
def fillZero(DataFrame,columns) :
    DataFrame[columns] = DataFrame[columns].fillna(0)
#-----------------------------------------------------------------------------#

## preprocessing --------------------------------------------------------------
# 전처리
def preprocessing(DataFrame) :
    # 날짜 형식으로 변환
    str_to_Date(DataFrame,'date')
    # index 리셋 후 정렬
    reset_index(DataFrame)
    # 결측치 보간
    interpolate(DataFrame, 'amount', 3, 4)
    interpolate(DataFrame, 'price', 3, 2)
    # 나머지 0으로 채우기
    fillZero(DataFrame, 'amount')
    fillZero(DataFrame, 'price')
    # 피처 스케일링하기
    standard_scaling(DataFrame, cols_scaling)
#-----------------------------------------------------------------------------#

# functions end ==============================================================#
#=============================================================================#

## ===========================================================================#
## main start ================================================================#

# 파일에서 데이터를 불러와 DF에 넣는다
df = make_DF(files)

# 전처리
preprocessing(df)

# 지역 가격 삭제
#df.drop(['seoul','busan','daegu','gwangju','daejun'], axis=1, inplace=True)

# 파일에 저장
df.to_csv(filename)

# main end ===================================================================#
#=============================================================================#