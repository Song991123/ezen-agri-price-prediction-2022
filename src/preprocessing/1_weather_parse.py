import pandas as pd
import MLP as mlp

## 2017년부터 2022년까지 컬럼으로 구분되어진 기상 정보 파일을 date를 인덱스로 정렬 

## initialize start ==========================================================#
# 읽어올 파일 이름
file_read = "./1_원본데이터/전주_2017.csv"
# 저장할 파일 이름
file_save = "./2_기후데이터_파싱/전주_날씨.csv"
# 인덱스로 쓸 컬럼
index = ["date"]
# 파일에서 정렬할 연도 리스트
years = ["2017",'2018','2019','2020','2021','2022']
# 바꿔줄 컬럼 리스트
columns = index + years
#---------------------------------------------- ------------------------------#

## functions start ===========================================================#
# 각 년도에 맞춰 문자열을 바꿔준다
def chagedate(df,year) :
    for index, row in df.iterrows() :
        month = row['date'][4:6]
        day = row['date'][6:8]
        row['date'] = '{}-{}-{}'.format(year, month, day)
#-----------------------------------------------------------------------------#

## main start ================================================================#
# 파일에서 읽어온다
data = pd.read_csv(file_read, encoding='UTF-8')

# 컬럼 이름을 변경
data.columns = columns

# 저장할 df 생성
result = pd.DataFrame()

for year in years :
    # 'date'와 연도 2개의 컬럼을 갖는 df를 생성
    columns = index + [year]
    # 윤년 (2.29) 행을 삭제하고, 문자로 형변환
    temp = data[columns].dropna().astype("str")
    # 문자열에 포멧을 주어 날짜 형식으로 표현
    # 날짜 형변환은 하지 않음 
    # CSV로 저장할때 유지되지 않기 때문
    chagedate(temp, year)
    # date 컬럼에 연도 정보가 있기 때문에, 기존 각 년도 컬럼 이름을 평균기온으로 변경
    temp.rename(columns={year:'temp_mean'},inplace=True)
    # 저장할 df에 병합한다
    result = pd.concat([result, temp])
# date 컬럼을 인덱스로 변경하고, sort한다
mlp.reset_index(result,date=True,drop=True)

# 파일로 저장한다
result.to_csv(file_save,encoding='UTF-8')

