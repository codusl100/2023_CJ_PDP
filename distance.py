import csv
import pickle

def calculate_distance_time(departure, destination):
    # CSV 파일 읽어오기
    data = []
    with open('od_matrix.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # 헤더 행 스킵
        for row in reader:
            data.append(row)

    # pickle 파일로 저장
    with open('od_matrix.pkl', 'wb') as file:
        pickle.dump(data, file)

    # pickle 파일 로드
    with open('od_matrix.pkl', 'rb') as file:
        data = pickle.load(file)

    for row in data:
        if row[0] == departure and row[1] == destination:
            distance = float(row[2])
            time = float(row[3])
            return distance, time

    return None, None