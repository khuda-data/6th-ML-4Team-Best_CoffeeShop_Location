import pandas as pd


file_path = 'C:\Users\pjung\OneDrive\문서\정현\동아리\쿠다\TP\서울시 휴게음식점 인허가 정보.csv'


data = pd.read_csv(file_path, encoding='euc-kr')

# 커피숍 데이터 선택
data_filtered_category = data[data['업태구분명'] == '커피숍']

# 업장명으로 프렌차이즈 커피 선택
business_names = ['컴포즈', '메가엠지', '빽다방', '이디야', '스타벅스', '투썸', '할리스', '커피빈']
data_filtered_business = data_filtered_category[data_filtered_category['사업장명'].str.contains('|'.join(business_names))]

# 필요한 데이터 행만 선택
required_columns = ['인허가일자', '영업상태명', '폐업일자', '지번주소', '도로명주소', '좌표정보(X)', '좌표정보(Y)', '소재지면적', '사업장명']
data_selected = data_filtered_business[required_columns]

# 업장명으로 중저가커피와 고가 커피 구분
def classify_business(row):
    if any(name in row['사업장명'] for name in ['컴포즈', '메가엠지', '빽다방']):
        if row['영업상태명'] == '영업\정상':
            return '저가'
        elif row['영업상태명'] == '폐업':
            return '저가'
    elif '이디야' in row['사업장명']:
        if row['영업상태명'] == '영업\정상':
            return '중저가'
        elif row['영업상태명'] == '폐업':
            return '중저가'
    elif any(name in row['사업장명'] for name in ['스타벅스', '투썸', '할리스', '커피빈']):
        if row['영업상태명'] == '영업\정상':
            return '고가'
        elif row['영업상태명'] == '폐업':
            return '고가'
    return '기타'

# 가격대 컬럼 추가
data_selected['가격대'] = data_selected.apply(classify_business, axis=1)


low_price_data = data_selected[data_selected['가격대'] == '저가']
mid_low_price_data = data_selected[data_selected['가격대'] == '중저가']
high_price_data = data_selected[data_selected['가격대'] == '고가']


low_price_data.to_csv('C:\Users\pjung\OneDrive\문서\정현\동아리\쿠다\TP\저가커피.csv', index=False)
mid_low_price_data.to_csv('C:\Users\pjung\OneDrive\문서\정현\동아리\쿠다\TP\중저가커피.csv', index=False)
high_price_data.to_csv('C:\Users\pjung\OneDrive\문서\정현\동아리\쿠다\TP\고가커피.csv', index=False)

