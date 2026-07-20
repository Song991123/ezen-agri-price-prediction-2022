import tensorflow as tf
import pandas as pd
import numpy as np

## initialize =================================================================
# v1 에러 메세지 출력하지 않음
tf.compat.v1.disable_eager_execution()
# 모델 초기화
model = tf.compat.v1.global_variables_initializer()
# 플레이스 홀더를 설정합니다.
# X 독립변수 4개
# y 종속변수 1개
X = tf.compat.v1.placeholder(tf.float32, shape=[None, 4])
y = tf.compat.v1.placeholder(tf.float32, shape=[None, 1])
# WX+b
W = tf.Variable(tf.random.normal([4, 1]), name="weight")
b = tf.Variable(tf.random.normal([1]), name="bias")
hypothesis = tf.matmul(X, W) + b
# 비용 함수를 설정합니다.
cost = tf.reduce_mean(input_tensor=tf.square(hypothesis - y))
# 최적화 함수를 설정합니다.
optimizer = tf.compat.v1.train.GradientDescentOptimizer(learning_rate=0.000005)
train = optimizer.minimize(cost)
# 세션을 생성합니다.
sess = tf.compat.v1.Session()
# 글로벌 변수를 초기화합니다.
sess.run(tf.compat.v1.global_variables_initializer())
# =============================================================================

## input ======================================================================
# 파일에서 데이터 불러오기
#train_data = pd.read_csv('./dataset21.csv', encoding='UTF-8')
#train_data = pd.read_csv('./상추.csv', encoding='UTF-8')
train_data = pd.read_csv('./고냉지배추.csv', encoding='UTF-8')
# 사용할 컬럼 정리
#[ "date","Tmean_s",'subdo_s',"Tmin_s","Tmax_s","rain_s" ]
#[ "price" ]
#columns_get = ['Tmean_23','Tmin_23','Tmax_23','rain_23','price']
#columns_get = [ "Tmean","Tmin","Tmax","Hmax" ,'price_mean' ]
columns_get = [ 'subdo_s',"Tmin_s","Tmax_s","rain_s",'price' ]
#columns_name = ['Tmean','Tmin','Tmax','rain','price']
train_data = train_data[columns_get]
#train_data.columns = columns_name
# numpy array로 변환
xy = np.array(train_data, dtype=np.float32)
# 4개의 변인을 독립 변수로
x_data = xy[:, :4]
# 가격을 종속 변수로
y_data = xy[:, [4]]
# =============================================================================

## process ====================================================================
# 학습을 수행합니다.
for step in range(100001):
    cost_, hypo_, _ = sess.run([cost, hypothesis, train], feed_dict={X: x_data, y: y_data})
    if step % 500 == 0:
        print("#", step, " 손실 비용: ", cost_)
        print("- 배추 가격: ", hypo_[0])
# =============================================================================

## output =====================================================================
# 학습된 모델을 저장합니다.
try :
    saver = tf.compat.v1.train.Saver()
    save_path = saver.save(sess, './save_check')
    print('학습된 모델을 저장했습니다.')
except Exception as e:
    print(e)
    print('저장하지 못했습니다.')
# =============================================================================

## initialize =================================================================
# 저장된 모델을 불러오는 객체를 선언합니다.
saver = tf.compat.v1.train.Saver()
model = tf.compat.v1.global_variables_initializer()
# =============================================================================

## input ======================================================================
# 파일로 테스트 데이터를 불러옴
raw_data = pd.read_csv('./dataset22.csv', encoding='UTF-8')
# 사용할 컬럼 정리
columns_get = ['Tmean_32','Tmin_32','Tmax_32','rain_32','price']
# 파일에서 사용할 컬럼을 고른다
test_data = raw_data[columns_get]
# =============================================================================

## process ====================================================================
with tf.compat.v1.Session() as sess:
    flag = False
    try :
        sess.run(model)
        save_path = './save_check'
        saver.restore(sess, save_path)
        print('학습된 모델을 복원했습니다.')
        flag = True
    except Exception as e:
        print(e)
        print('모델을 불러오지 못했습니다.')
    if flag :
        sess.run(model)
        save_path = './save_check'
        saver.restore(sess, save_path)
    
        list_pre = []
        list_rea = []
        result = pd.DataFrame()
        arr = np.array(test_data, dtype=np.float32)
        for x in arr :
            x = x.reshape((1,5))
            x_data = x[:,:4]
            dict = sess.run(hypothesis, feed_dict={X: x_data})
            list_pre.append(dict[0][0])
            list_rea.append(x[:,[4]][0][0])
        result['date'] = raw_data['date']
        result['predict'] = list_pre
        result['price'] = list_rea
# =============================================================================

## output =====================================================================
for item in result :
    print(item)
# 저장할 파일 이름
filename = "result_tf_v1.csv"
# 파일에 저장
result.to_csv(filename,encoding='UTF-8')