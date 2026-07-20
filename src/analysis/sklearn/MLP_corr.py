import  pandas              as pd
import  matplotlib.pyplot   as plt
# 상관계수
import  seaborn             as sns

## ===========================================================================#
## initialize start ==========================================================#

# 파일 이름 -------------------------------------------------------------------
filename = "result.csv"
#-----------------------------------------------------------------------------#
## 기상조건과 거래량, 평균가격의 상관계수용 컬럼 ------------------------------
cols = ['Tmean','subdo','Tmin','Tmax','rain','amount','price']
#-----------------------------------------------------------------------------#
## 평균가격과 지역가격의 상관계수용 컬럼들 ------------------------------------
cols_price = [ 'price', 'seoul', 'busan', 'daegu', 'gwangju', 'daejun']
#-----------------------------------------------------------------------------#
## 그래프 출력을 위한 cols 한글 이름 ------------------------------------------
cols_view = ['평균기온','습도','최저기온','최고기온','강우량','거래량','평균가격']
cols_price_view = [ '평균가격', '서울', '부산', '대구', '광주', '대전' ]
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

# functions end ==============================================================#
#=============================================================================#

## ===========================================================================#
## main start ================================================================#

# 파일에서 데이터를 불러와 DF에 넣는다
df = make_DF(filename)

# 2x2 lineplot으로 시간별 피쳐값들 그래프로 그리기
draw_lineplot(df,'date',['rain','price','amount','seoul'])
draw_lineplot(df,'date',['Tmean','Tmin','Tmax','subdo'])

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

# main end ===================================================================#
#=============================================================================#