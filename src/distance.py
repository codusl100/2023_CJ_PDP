import csv
import pickle
import os

# 전역 변수로 데이터 저장
data = None

def load_data():
    global data
    if data is not None:
        return

    # CSV 파일 읽어오기
    data = {}
    with open(os.getenv("DATA_PATH") + '/od_matrix.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # 헤더 행 스킵
        for row in reader:
            departure = row[0]
            destination = row[1]
            distance = float(row[2])
            time = float(row[3])

            if departure not in data:
                data[departure] = {}
            data[departure][destination] = (distance, time)

    # pickle 파일로 저장
    with open(os.getenv("DATA_PATH") + '/od_matrix.pkl', 'wb') as file:
        pickle.dump(data, file)

def calculate_distance_time(departure, destination):
    load_data()  # 데이터 로드
    global data

    if departure in data and destination in data[departure]:
        distance, time = data[departure][destination]
        return distance, time

    return None, None