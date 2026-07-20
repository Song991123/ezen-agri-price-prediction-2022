import pandas as pd
#import datetime as dt

#날짜 형식 변경
file_read = './2_기후데이터_파싱/전주날씨.csv'
file_save = './2_기후데이터_파싱/전주날씨_p.csv'

result = pd.read_csv(file_read, encoding="UTF-8")
result['date'] = pd.to_datetime(result['date'], format='%Y%m%d').dt.date
result.to_csv(file_save, encoding='UTF-8')