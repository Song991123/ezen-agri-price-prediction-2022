import MLP as mlp
import pandas as pd
import numpy as np
import datetime as dt

from sklearn.preprocessing import MinMaxScaler

## initialize start ==========================================================#
# 파일 이름 지정
# 날짜, 날씨, 가격 정보가 있는 파일을 대상으로 한다.
#dataset_path = './4_기후가격병합/raw_data.csv'
dataset_path = './4_기후가격병합/lettuce.csv'

#cols_cut = ['date','Tmean','subdo','Tmin','Tmax','rain','amount','price']

# date,Tmean,Tmax,Tmin,temp high-min,rain,Hmax,Hmin,amount,price_min,price_max,price_mean
cols_cut = ['date','Tmin','Tmax','Tmean','Hmax','price_mean']

# 스케일(0~1)처리할 컬럼들
cols_scale =  ['Tmin','Tmax','Tmean','Hmax']

# 시프팅할 컬럼들
cols_shift =  ['Tmin','Tmax','Tmean','Hmax']

# 시프팅 할 수치 초기화
shift_days = 0
shift_month = 1
shift_step = shift_days + shift_month * 30

#---------------------------------------------- ------------------------------#

## functions start ===========================================================#

# 데이터프레임을 날짜로 나눔
def slide_dataset(DataFrame,start, end) :
    result = DataFrame.copy()
    result = result.loc[(result.date > start) & (result.date < end)]
    return result

# 특정 컬럼을 시프트한다
def shift_columns(Dataframe, columns, shift_steps, s=False) :
    result = Dataframe.copy()
    for column in columns :
        new_column_name = '{}_{}'.format(column, str(shift_steps).zfill(2))
        if s :
            new_column_name = '{}_s'.format(column)
        result[new_column_name] = result[column].shift(+shift_steps)
    return result

def line_tbt(df) :
    mlp.draw_lineplot(df,'date',['Tmin','Tmax','Tmean','price']) 
    mlp.draw_lineplot(df,'date',['Hmax','Hmax','price','price'])
    
# 상관계수 목록을 반환
def find_max_corr(DataFrame) :
    # 원본 데이터는 남기고 테스트용 df 생성
    df = DataFrame.copy()
    # 1부터 설정된 최대 스텝 까지 모두 시프팅한다
    shift_steps = range(1,shift_step)
    for step in shift_steps :
        df = shift_columns(df,cols_shift, step)
    
    # 기상조건과 가격의 상관계수
    corr = df.corr(method = 'pearson')
    
    # 가격에의 상관계수만 뽑아낸다.
    corr = corr['price']
    
    # 인덱스에서 'price'를 삭제
    corr = corr[corr.index != 'price']
    
    # +-0.5를 넘는 상관계수의 개수
    count = corr[(corr > 0.5) | (corr < -0.5)].count()
    
    if count > 0 :
        # +-0.5를 넘는 상관계수만 남긴다.
        corr = corr[(corr > 0.5) | (corr < -0.5)]
    
    # 상관계수로 정렬한다
    corr.sort_values(ascending=False, inplace=True)
    return corr

# 상관계수가 높은 스탭을 찾는다
# 만일 상관계수가 +-0.5를 넘는게 없으면, 가장 높은 수치의 상관계수로 찾는다
def find_step(corr):
    if corr.count() > 10 :
        max = 10
    else :
        max = corr.count()
    shift_step = 0
    for index in range(0, max) :
        shift_step += int(corr.index[index][-2:])
    shift_step = int(shift_step/max)
    return shift_step

# 데이터 프레임을 확장한다.
# 시프팅한 인자들은, 예측에 사용되는데, 스텝만큼 행을 늘려주지 않으면 소실된다
def append_df(DataFrame,step):
    # df의 마지막 행에서 인덱스값을 가져온다.
    last_index = DataFrame.index[-1]
    
    # 원본 데이터에서 결과용 df 생성
    result = DataFrame.copy()
    
    # 컬럼 개수 추출
    row, col = result.shape
    
    # 임시 DF 생성
    # 차원은, 스텝과 컬럼 개수로 정하고, 데이터는 0으로 채워넣는다.
    # 컬럼 이름은 동일하게 생성
    temp = pd.DataFrame(np.zeros((step,col)),columns=result.columns)
    
    # 시프트되어 넘어가는 행을 위한 인덱스를 만든다
    date_list =[]
    for idx in range(1,step+1):
        # 마지막 행에서 받아온 인덱스 값에서 date형식으로 '일'을 더해나간다
        index = last_index + dt.timedelta(days=idx)
        date_list.append(index)
    
    # 임시 DF에 date 컬럼을 list를 이용해 추가한다
    temp['date'] = date_list
    # date 컬럼을 인덱스로 변경한다
    temp.set_index('date', drop=True, inplace=True)
    # 결과 출력용 DF에 임시 DF를 병합한다.
    result = pd.concat([result,temp])
    return result

#-----------------------------------------------------------------------------#

## main start ================================================================#
# 파일에서 데이터를 읽어온다.
raw_dataset = pd.read_csv(dataset_path, encoding='UTF-8')

# 초기데이터를 dataset에 복사
dataset = raw_dataset.copy()

# 컬럼 줄이기
dataset = dataset[cols_cut]

# 'date' 컬럼을 date형으로 변경
mlp.str_to_Date(dataset, 'date')

# 'date' 컬럼을 인덱스로 변경
mlp.reset_index(dataset, date=True, drop=True)

# 컬럼 이름 변경
dataset.rename(columns={'price_mean':'price'},inplace=True)
#print(dataset.head())

# 스케일러 생성
x_scaler = MinMaxScaler()

# 타겟 컬럼의 값을 0~1사이의 숫자로 스케일링한다
for col in cols_scale :
    dataset[[col]] = x_scaler.fit_transform(dataset[[col]]).round(4)

# 상관계수가 높은 시프팅을 찾는다
corr= find_max_corr(dataset)

# 상관계수가 높은 스텝을 찾는다
if corr.count() > 0 :
    shift_step = find_step(corr)

# 찾아낸 스텝 만큼 DF의 행을 확장한다
df_append = append_df(dataset,shift_step)

# 찾아낸 스텝 값으로 시프팅한다
result = shift_columns(df_append,cols_shift, shift_step, s=True)

# 시프팅으로 인해 데이터 값이 없는 앞 부분을 삭제한다
result = result[shift_step:]

# 시프팅 이후의 상관계수 시각화
corr = result.corr(method = 'pearson')
mlp.draw_heatMap(corr)

# 파일에 저장한다.
file_name = './5_스케일링_시프팅/data_ss{}.csv'.format(shift_step)
# result.to_csv(file_name, encoding='UTF-8')

#-----------------------------------------------------------------------------#

# 가격이 존재하지 않는 (0인) 열을 삭제
#dataset = dataset[dataset.price != 0]

# 고냉지 배추 수확 시기의 데이터만 남긴다
#dataset21 = slide_dataset(dataset21,dt.date(2021, 7,15),dt.date(2021,10,31))
#dataset22 = slide_dataset(dataset22,dt.date(2022, 7,15),dt.date(2022,10,31))

# 기상조건과 물량, 가격의 상관계수
#corr21 = dataset21.corr(method = 'pearson')
#corr22 = dataset22.corr(method = 'pearson')

#print(corr21[(corr21.index == 'price')])

#mlp.draw_heatMap(corr21)
#mlp.draw_heatMap(corr22)

#line_tbt(dataset21)
#line_tbt(dataset22)

# 파일에 저장
#dataset21.to_csv('dataset21.csv',encoding='cp949')
#dataset22.to_csv('dataset22.csv',encoding='cp949')