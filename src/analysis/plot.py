import pandas as pd
import matplotlib.pyplot as plt

## initialize =================================================================
filename = './result_tf_v1.csv'

# =============================================================================

## input ======================================================================
# 파일로 테스트 데이터를 불러옴
data = pd.read_csv(filename, encoding='UTF-8')
x_data = data['date']
y_pre  = data['predict']
y_pri  = data['price']
# =============================================================================


plt.figure(figsize=(10,4), dpi=300)
plt.rc('font', family='Malgun Gothic')
plt.plot(x_data, y_pri, label="실제가격")
plt.plot(x_data, y_pre, label="linear")
plt.xlabel("날짜")
plt.ylabel("가격")
plt.legend()
plt.title("가격예측")
plt.show()
plt.close()