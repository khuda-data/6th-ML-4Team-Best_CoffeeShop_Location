import pandas as pd
from math import radians, sin, cos, sqrt, atan2

# 데이터 로드
mid = pd.read_csv('C:/Users/pjung/OneDrive/문서/정현/동아리/쿠다/TP/중저가형(최종)_cleaned.csv', encoding='cp949')  # 중심이 될 카페
surround = pd.read_csv('C:/Users/pjung/OneDrive/문서/정현/동아리/쿠다/TP/공기업.csv', encoding='utf-8')

# 위도와 경도를 숫자형으로 변환
mid['위도'] = pd.to_numeric(mid['위도'], errors='coerce')
mid['경도'] = pd.to_numeric(mid['경도'], errors='coerce')
surround['Latitude'] = pd.to_numeric(surround['Latitude'], errors='coerce')
surround['Longitude'] = pd.to_numeric(surround['Longitude'], errors='coerce')

# 거리 계산 함수
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # 지구 반경 (단위: km)

    # 위도와 경도를 라디안으로 변환
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # 두 지점 간의 차이
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # 하버사인 공식
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # 거리 계산
    distance = R * c
    return distance

# 주변 공기업 수 계산을 위한 열 추가
mid['주변공기업수'] = 0  # 여기에 주변 시설물 이름!

# 각 중저가형 카페에 대해 반복
for i in range(len(mid)):
    distances = []
    # 주변의 공기업 위치와의 거리 계산
    for j in range(len(surround)):
        distance = calculate_distance(
            mid.iloc[i]['위도'], mid.iloc[i]['경도'],  # 수정된 부분
            surround.iloc[j]['Latitude'], surround.iloc[j]['Longitude']  # 좌표 x,y로 전환
        )
        distances.append(distance)

    # 거리 계산이 완료된 후, 0.3km 이내에 있는 공기업의 수를 계산
    if distances:
        num = 0
        for distance in distances:
            if distance <= 0.3:
                num += 1
        mid.at[i, '주변공기업수'] = num  # 수정된 부분

# 결과를 CSV 파일로 저장
mid.to_csv('C:/Users/pjung/OneDrive/문서/정현/동아리/쿠다/TP/중저가공기업.csv', index=False)
