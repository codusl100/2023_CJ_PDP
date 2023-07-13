import csv
import pickle

# 전역 변수로 데이터 저장
data = None

def load_data():
    global data
    if data is not None:
        return

    # CSV 파일 읽어오기
    data = []
    with open('C:\pythonProject4\data\\od_matrix.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # 헤더 행 스킵
        for row in reader:
            data.append(row)

    # pickle 파일로 저장
    with open('C:\pythonProject4\data\\od_matrix.pkl', 'wb') as file:
        pickle.dump(data, file)

def calculate_distance_time(departure, destination):
    load_data()  # 데이터 로드
    global data

    for row in data:
        if row[0] == departure and row[1] == destination:
            distance = float(row[2])
            time = float(row[3])
            return distance, time

    return None, None
