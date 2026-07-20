import pandas   as pd
import datetime as dt
import MLP      as mlp

#%% ==========================================================================#
## initialize start ==========================================================#

# 파일 이름 -------------------------------------------------------------------
# 지역, 품목을 리스트로 작성하여, 파일을 목록을 생성한다
areas = ["jeonju"]
items = ["lettuce","red_pepper","green_pepper","cabbage"]
path  = "./NH"
files = []
# 파일목록 생성
for area in areas :
    for item in items :
        file = "{}/{}_{}.csv".format(path,area,item)
        files.append(file)

# 저장할 파일 이름
#file = "result_{}_{}.csv".format(area,item)
#-----------------------------------------------------------------------------#

## 기상조건과 거래량, 평균가격의 상관계수용 컬럼 ---------------------------------
cols_ASOS = ['Tmean','subdo','Tmin','Tmax','rain']
## 공판장 데이터 컬럼
cols_NH = ['date', 'area', 'item', 'grade', 'amount', 'price']
#-----------------------------------------------------------------------------#

## columns to do scaling ------------------------------------------------------
# 스케일 할 컬럼
cols_scaling = ['Tmean','subdo','Tmin','Tmax','rain','amount']
#-----------------------------------------------------------------------------#

## 기준 날짜 설정 -------------------------------------------------------------
#target_date = dt.datetime.strftime( dt.datetime(year=2021, month=1, day=1), '%Y-%m-%d')
# 시간 정보는 필요없음
start_day   = dt.date(2017,8,1)
target_date = dt.date(2022,1,1)
#-----------------------------------------------------------------------------#

# initialize end =============================================================#
#=============================================================================#

#%% ==========================================================================#
## functions start ===========================================================#

# 기준일로 데이터를 분할하여, 샘플데이터를 만든다.
def split_Data(DataFrame, target_date) :
    result = DataFrame.loc[DataFrame["date"] >= target_date]
    return result


# functions end ==============================================================#
#=============================================================================#

#%% ==========================================================================#
## main start ================================================================#

# 초기화
sample_mode = True

# 파일에서 데이터를 불러와 DF에 넣는다
df = mlp.make_DF(files)
#print(df.columns)

# 컬럼명 변경 / 딕셔너리를 사용하는 방법
dict_columns = {
    '경매시간'        :'date',
    '산지'            :'area',
    '품종'            :'item',
    '규격/등급/과수'  :'grade',
    '수량'            :'amount',
    '경락가'          :'price',
    '경매사'          :'name'
}
df.rename(columns=dict_columns,inplace=True)

# 컬럼명 변경 리스트를 이용하여 직접 변경
#df.columns = ['date', 'area', 'item', 'grade', 'amount', 'price', 'name']

# 경매사 이름 제거
df.drop(['name'],axis=1,inplace=True)

# 오류 데이터 삭제
idx = df[(df['date'] == "조회된 데이터가 없습니다.")].index
df.drop(idx,inplace=True)

# 'date'에서 시간 정보 삭제 date형으로 변경한다.
df['date'] = pd.to_datetime(df['date']).dt.date

# 'date'로 올림차순 정렬
df.sort_values(by=['date'],ascending=True,inplace=True)

# 인덱스 리셋
mlp.reset_index(df)

# 'amount','price'를 정수형으로 변환
df[['amount','price']] = df[['amount','price']].astype("int")

# 2022년 1월 1일로 데이터 분할
if sample_mode :
    df = split_Data(df,target_date)

# 동의어 리스트
dict = {
    "김제" : ["전라북도 김제시","전북 김제시 용","전북 김제시","전북 김제시상동"],
    "완주" : ["전라북도 완주군","전북 완주군 이","전북 완주군 상","전북 완주군 구","전북 완주군"],
    "전주" : ["전라북도 전주시","전북 전주시 완","전북 전주시 덕","전북 전주시"],
    "익산" : ["전라북도 익산시","전북 익산시"]
}

# 동의어 리스트를 이용해, area 값을 보정한다
for key, list in dict.items() :
    for word in list :
        df = df.replace(word, key)

# 가격 평균을 구하기 위해 각 항목의 가격총량의 컬럼을 만든다
df['price_sum'] = df['amount']*df['price']
#print(df.head())

# 그룹화에 필요한 딕셔너리
dict_for_group = {
    'amount':'sum',
    'price':['min','max'],
    'price_sum':'sum'
}

# multiIndex 컬럼을 평탄화
def flatten_cols(df) :
#    df.columns = ['_'.join(x) for x in df.columns.to_flat_index()]
    df.columns = ['date', 'area', 'item', 'grade', 'amount', 'price_min', 'price_max', 'price_mean']
    return df

# 날짜, 지역, 품종, 등급을 그룹으로 수량의 합과, 가격의 평균을 구한다.
result = df.groupby(['date','area','item','grade'], as_index=False).agg(dict_for_group).pipe(flatten_cols).round(2)

# 가격총량의 합계를 수량합계로 나눠 평균 가격을 산출한다
result['price_mean'] = (result['price_mean']/result['amount']).round(2)

# dict에 있는 지역으로 필터링
result = result[result['area'].isin(dict.keys())]

# 품목으로 필터링
dict_item = ['적상추(적치마)','청상추(청치마)','청양','홍고추(일반)']
result = result[result['item'].isin(dict_item)]

print(result.head(10))
print(result.count())

# 저장할 파일 이름
filename = "result.csv"
# 파일에 저장
result.to_csv(filename,encoding='cp949')

# main end ===================================================================#
#=============================================================================#