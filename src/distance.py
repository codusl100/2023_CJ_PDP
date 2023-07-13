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
    with open('C:\pythonProject4\CJ\data\\od_matrix.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # 헤더 행 스킵
        for row in reader:
            data.append(row)

    # pickle 파일로 저장
    with open('od_matrix.pkl', 'wb') as file:
        pickle.dump(data, file)

def calculate_distance_time(departure, destination):
    global data
    if data is None:
        # pickle 파일 로드
        with open('od_matrix.pkl', 'rb') as file:
            data = pickle.load(file)

    for row in data:
        if row[0] == departure and row[1] == destination:
            distance = float(row[2])
            time = float(row[3])
            return distance, time

    return None, None