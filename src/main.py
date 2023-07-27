import pandas as pd
import prob_builder as prob
import solver
import os

# CSV 파일을 데이터프레임으로 로드
df_order = pd.read_csv(os.getenv("DATA_PATH") + '/new_orders.csv', encoding='cp949')
df_car = pd.read_csv(os.getenv("DATA_PATH") +'/new_vehicle.csv', encoding='cp949')

def LoadProb():
    ThisProb = prob.Prob_Instance()
    ThisProb.ord_list = [prob.Order(*row) for _, row in df_order.iterrows()]
    ThisProb.car_list = [prob.Car(row[0], row[4], row[5],row[6], row[7]) for _, row in df_car.iterrows()]
    return ThisProb

if __name__ == '__main__':
    Sample = LoadProb()
    print(solver.rule_solver(Sample))
    # Solution = solver.rule_solver(Sample)
    # print('총 운영 비용: ' + str(Solution['Objective']))