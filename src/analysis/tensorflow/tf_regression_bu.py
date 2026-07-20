import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import datetime as dt

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# 텐서 버전 확인
print(tf.__version__)

# 파일에서 데이터를 읽어온다.
dataset_path = 'dataset21.csv'
raw_dataset = pd.read_csv(dataset_path)
# 초기데이터를 dataset에 복사
dataset = raw_dataset.copy()

# 컬럼 줄이기
cols_all = ['date','date','Tmean','subdo','Tmin','Tmax','rain','amount','price','Tmean_23','subdo_23','Tmin_23','Tmax_23','rain_23']
cols_get = ['date','Tmean_23','subdo_23','Tmin_23','Tmax_23','rain_23','amount','price']
cols_cut = ['date','Tmean','subdo','Tmin','Tmax','rain','amount','price']
dataset[cols_cut] = dataset[cols_get]
cols_cut = ['date','Tmean','Tmin','price']
dataset = dataset[cols_cut]
print(dataset.tail())

# 'date' 컬럼을 date타입으로 변경
dataset['date'] = pd.to_datetime(dataset['date']).dt.date

# 인덱스를 'date'로 리셋
def reset_index(DataFrame) :
    DataFrame.reset_index( drop = True, inplace = True )
#    DataFrame.set_index('date', drop=True, inplace=True)
    DataFrame.sort_index(inplace=True)
reset_index(dataset)

# 데이터 분할
#start = dt.date(2021, 9, 15)
#train_dataset = dataset.loc[(dataset.index < start)]
#test_dataset = dataset.drop(train_dataset.index)
train_dataset = dataset[:70][['date','Tmean','Tmin','price']]
test_dataset = dataset[70:][['date','Tmean','Tmin','price']]

train_dataset = dataset.drop('date', axis=1)
test_dataset = dataset.drop('date', axis=1)

# 산점도 분포 확인
#sns.pairplot(train_dataset[['Tmean','subdo','Tmin','Tmax','rain','amount','price']], diag_kind="kde")
sns.pairplot(train_dataset[['Tmean','Tmin','price']], diag_kind="kde")

# 데이터 확인
train_stats = train_dataset.describe()
train_stats.pop("price")
train_stats = train_stats.transpose()
print(train_stats)

# 특성과 레이블 분리
train_labels = train_dataset.pop('price')
test_labels = test_dataset.pop('price')

# 데이터 정규화
def norm(x):
  return (x - train_stats['mean']) / train_stats['std']

normed_train_data = norm(train_dataset)
normed_test_data = norm(test_dataset)

# 모델 만들기
def build_model():
  model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=[len(train_dataset.keys())]),
    layers.Dense(64, activation='relu'),
    layers.Dense(1)
  ])

  optimizer = tf.keras.optimizers.RMSprop(0.001)

  model.compile(loss='mse',
                optimizer=optimizer,
                metrics=['mae', 'mse'])
  return model

model = build_model()

# 모델 확인
print(model.summary())

# 샘플로 모델 확인
example_batch = normed_train_data[:10]
example_result = model.predict(example_batch)
print(example_result)

# 모델 훈련
# 에포크가 끝날 때마다 점(.)을 출력해 훈련 진행 과정을 표시합니다
class PrintDot(keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs):
    if epoch % 100 == 0: print('')
    print('.', end='')

EPOCHS = 1000

# 지정된 에포크 횟수 동안 성능 향상이 없으면 자동으로 훈련을 멈춥니다
# patience 매개변수는 성능 향상을 체크할 에포크 횟수입니다
early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)

history = model.fit(normed_train_data, train_labels, epochs=EPOCHS,
                    validation_split = 0.2, verbose=0, callbacks=[early_stop, PrintDot()])

# 훈련과정 시각화
hist = pd.DataFrame(history.history)
hist['epoch'] = history.epoch
hist.tail()

def plot_history(history):
  hist = pd.DataFrame(history.history)
  hist['epoch'] = history.epoch

  plt.figure(figsize=(8,12))

  plt.subplot(2,1,1)
  plt.xlabel('Epoch')
  plt.ylabel('Mean Abs Error [price]')
  plt.plot(hist['epoch'], hist['mae'],
           label='Train Error')
  plt.plot(hist['epoch'], hist['val_mae'],
           label = 'Val Error')
  plt.ylim([0,5])
  plt.legend()

  plt.subplot(2,1,2)
  plt.xlabel('Epoch')
  plt.ylabel('Mean Square Error [$price^2$]')
  plt.plot(hist['epoch'], hist['mse'],
           label='Train Error')
  plt.plot(hist['epoch'], hist['val_mse'],
           label = 'Val Error')
  plt.ylim([0,20])
  plt.legend()
  plt.show()

plot_history(history)

# 모델 성능 검증
loss, mae, mse = model.evaluate(normed_test_data, test_labels, verbose=2)

print("테스트 세트의 평균 절대 오차: {:5.2f} price".format(mae))

# 예측
test_predictions = model.predict(normed_test_data).flatten()

plt.scatter(test_labels, test_predictions)
plt.xlabel('True Values [price]')
plt.ylabel('Predictions [price]')
plt.axis('equal')
plt.axis('square')
plt.xlim([0,plt.xlim()[1]])
plt.ylim([0,plt.ylim()[1]])
_ = plt.plot([-100, 100], [-100, 100])

# 오차분포
error = test_predictions - test_labels
plt.hist(error, bins = 25)
plt.xlabel("Prediction Error [price]")
_ = plt.ylabel("Count")
