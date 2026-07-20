import tensorflow as tf
import numpy as np
from pandas.io.parsers import read_csv

tf.compat.v1.disable_eager_execution()

## initialize =================================================================
# 플레이스 홀더를 설정합니다.
X = tf.compat.v1.placeholder(tf.float32, shape=[None, 4])
Y = tf.compat.v1.placeholder(tf.float32, shape=[None, 1])

W = tf.Variable(tf.random.normal([4, 1]), name="weight")
b = tf.Variable(tf.random.normal([1]), name="bias")

# 가설을 설정합니다.
hypothesis = tf.matmul(X, W) + b

# 저장된 모델을 불러오는 객체를 선언합니다.
saver = tf.compat.v1.train.Saver()
model = tf.compat.v1.global_variables_initializer()
columns_get = ['Tmean_32','Tmin_32','Tmax_32','rain_32','price']
# =============================================================================

## input ======================================================================
# 파일로 테스트 데이터를 불러옴
test_data = read_csv('./dataset22.csv', encoding='UTF-8')
# 파일에서 사용할 컬럼을 고른다
test_data = test_data[columns_get]
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
    
        list = []
        arr = np.array(test_data, dtype=np.float32)
        for x in arr :
            x = x.reshape((1,5))
            x_data = x[:,:4]
            dict = sess.run(hypothesis, feed_dict={X: x_data})
            pre = dict[0][0]
            rea = x[:,[4]][0][0]
            msg = 'predict : {:.2f} / real price : {:.2f} \n'.format(pre, rea)
            list.append(msg)
# =============================================================================

## output =====================================================================
if flag :
    for item in list :
        print(item)