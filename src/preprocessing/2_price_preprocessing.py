import pandas   as pd
import MLP      as mlp

#%% ==========================================================================#
## initialize start ==========================================================#

# 파일 이름 -------------------------------------------------------------------
file_read = "./1_원본데이터/jeonju_lettuce.csv"
# 저장할 파일 이름
file_save = "./3_가격데이터_전처리/result_lettuce.csv"
#-----------------------------------------------------------------------------#

## 공판장 데이터 컬럼
cols_lettuce = [ 'date', 'area', 'item', 'grade', 'amount', 'price']

columns ={
    '경매시간':'date',
    '산지':'area',
    '품종':'item',
    '규격/등급/과수':'grade',
    '수량':'amount',
    '경락가':'price',
    '경매사':'name'
}

# 동의어 사전
'''
dict = {
    "김제" : ["전라북도 김제시","전북 김제시 용","전북 김제시","전북 김제시상동"],
    "완주" : ["전라북도 완주군","전북 완주군 이","전북 완주군 상","전북 완주군 구","전북 완주군"],
    "전주" : ["전라북도 전주시","전북 전주시 완","전북 전주시 덕","전북 전주시"],
    "익산" : ["전라북도 익산시","전북 익산시"]
}
'''
dict = {
    "김제" : ["전라북도 김제시","전북 김제시 용","전북 김제시","전북 김제시상동"],
    "전주" : ["전라북도 전주시","전북 전주시 완","전북 전주시 덕","전북 전주시"],
    "익산" : ["전라북도 익산시","전북 익산시"]
}

# 그룹화에 필요한 딕셔너리
dict_for_group = {
    'amount':'sum',
    'price':['min','max'],
    'price_sum':'sum'
}

# 품목으로 필터링
#dict_item = ['적상추(적치마)','청상추(청치마)','청양','홍고추(일반)']
dict_item = ['적상추(적치마)','청상추(청치마)']

#-----------------------------------------------------------------------------#

# initialize end =============================================================#
#=============================================================================#

#%% ==========================================================================#
## functions start ===========================================================#

# multiIndex 컬럼을 평탄화
def flatten_cols(df) :
#    df.columns = ['_'.join(x) for x in df.columns.to_flat_index()]
#    df.columns = ['date', 'area', 'item', 'grade', 'amount', 'price_min', 'price_max', 'price_mean']
    df.columns = ['date', 'amount', 'price_min', 'price_max', 'price_mean']
    return df

# functions end ==============================================================#
#=============================================================================#

#%% ==========================================================================#
## main start ================================================================#

# 파일에서 데이터를 불러와 DF에 넣는다
raw_date = pd.read_csv(file_read, encoding='UTF-8')

# dataframe 복사
data = raw_date.copy()

# 컬럼 이름 변경
data.rename(columns=columns,inplace=True)

# 필요한 컬럼만 잘라내기
data = data[cols_lettuce]

# 오류 데이터 삭제
idx = data[(data['date'] == "조회된 데이터가 없습니다.")].index
data.drop(idx,inplace=True)

# 'date'에서 시간 정보 삭제 date형으로 변경한다.
data['date'] = pd.to_datetime(data['date']).dt.date

# 'date'로 올림차순 정렬
data.sort_values(by=['date'],ascending=True,inplace=True)

# 인덱스 리셋
mlp.reset_index(data)

# 'amount','price'를 정수형으로 변환
data[['amount','price']] = data[['amount','price']].astype("int")

# 동의어 사전으로 데이터 보정
for key, list in dict.items() :
    for word in list :
        data = data.replace(word, key)

# dict에 있는 지역으로 필터링
data = data[data['area'].isin(dict.keys())]

# 품목으로 필터링
data = data[data['item'].isin(dict_item)]

# 등급으로 필터링
data = data[data['grade'].isin(['4kg특','4kg1등'])]

# 가격 평균을 구하기 위해 각 항목의 가격총량의 컬럼을 만든다
data['price_sum'] = data['amount']*data['price']

# 날짜, 지역, 품종, 등급을 그룹으로 수량의 합과, 가격의 평균을 구한다.
#result = data.groupby(['date','area','item','grade'], as_index=False).agg(dict_for_group).pipe(flatten_cols).round(2)

# 날짜, 등급을 그룹으로 수량의 합과, 가격의 평균을 구한다.
# .agg(dict_for_group) 으로 그룹화 내용을 설정하고,
# .pipe(flatten_cols) 으로 이중 컬럼을 평탄화 하면서,
# flatten_cols 으로 새 컬럼 이름을 정한다 (price_sum -> price_mean)
# .round(2) 으로 소수점 두자리까지 표시
result = data.groupby(['date'], as_index=False).agg(dict_for_group).pipe(flatten_cols).round(2)

# 가격총량의 합계를 수량합계로 나눠 평균 가격을 산출한다
result['price_mean'] = (result['price_mean']/result['amount']).round(2)

print(result.head(10))
print(result.count())

mlp.reset_index(result, date=True, drop=True)

# 파일로 저장한다
try :
    result.to_csv(file_save,encoding='UTF-8')
    print("파일을 저장했습니다.")
except Exception as e:
    print(e)
    print('저장하지 못했습니다.')

# main end ===================================================================#
#=============================================================================#