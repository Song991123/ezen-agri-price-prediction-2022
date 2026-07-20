import pandas as pd
#import datetime as dt


## 가격 정보와 날씨 정보를 하나의 파일로 병합한다

## initialize start ==========================================================#
# 파일 이름 -------------------------------------------------------------------
file_weather = './2_기후데이터_파싱/전주날씨.csv'
file_item = './3_가격데이터_전처리/result_lettuce.csv'
file_save = './4_기후가격병합/lettuce.csv'
#-----------------------------------------------------------------------------#

## functions start ===========================================================#
## 파일에서 데이터를 불러와 DF로 합친다 ---------------------------------------
def make_DF(file) :
    result = pd.read_csv(file, encoding="UTF-8")
    result['date'] = pd.to_datetime(result['date']).dt.date
#    reset_index(result)
    return result
#-----------------------------------------------------------------------------#

## index 재 설정 --------------------------------------------------------------
def reset_index(DataFrame) :
    DataFrame.reset_index( drop = True, inplace = True )
    DataFrame.set_index('date', drop=True, inplace=True)
    DataFrame.sort_index(inplace=True)
#-----------------------------------------------------------------------------#

## join files -----------------------------------------------------------------
def join_files(file_weather,file_item) :
    df1 = make_DF(file_weather)
    df2 = make_DF(file_item)
    df = df1.set_index('date').join(df2.set_index('date'))
    return df
#-----------------------------------------------------------------------------#

## main start ================================================================#
df = join_files(file_weather,file_item)
df = df.fillna(0)
result = df[df.price_mean != 0]
result.to_csv(file_save,encoding='UTF-8')
#-----------------------------------------------------------------------------#