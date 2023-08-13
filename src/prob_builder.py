import copy
import distance
from datetime import datetime, timedelta
import pandas as pd

class Prob_Instance:
    def __init__(self):
        self.objective = 'Total_Cost'
        self.ord_list = [] # order list
        self.car_list = [] # car list

    def deepcopy(self):
        return copy.deepcopy(self)

class Order: # 입력 데이터: car (요청)
    def __init__(self, ORD_NO, arrive_latitude, arrive_longitude, arrive_ID, CBM, start_tw, end_tw, work_time,
                 terminal_ID, date, Group):
        self.ord_no = ORD_NO    # 주문 ID
        self.final_coord = [arrive_latitude,arrive_longitude]   # 도착지 좌표
        self.arrive_id = arrive_ID  # 도착지 ID
        self.cbm = CBM  # 상품 CBM
        self.time_window = [
                datetime.strptime(f"2023-05-01 {start_tw}", "%Y-%m-%d %H:%M"),
                datetime.strptime(f"2023-05-01 {end_tw}", "%Y-%m-%d %H:%M")
        ]

        self.work_time = work_time      # 하차 작업시간
        self.terminal_ID = terminal_ID  # 터미널ID (출발지)
        # self.start_coord = [start_latitude, start_longitude] # 터미널 좌표
        self.date = date    # 주물 발생 날짜
        self.group = Group  # 그룹

    def initialize(self):   # 결과 테이블
        self.delivered = False  # 배송 완료 여부
        self.vehicle_id = None  # 할당된 차량 ID
        self.sequence = None      # 할당된 배송 시퀀스
        self.site_code = None   # 도착지 ID
        self.arrival_time = None    # 도착시각
        self.waiting_time = None    # 대기시간
        self.service_time = None    # 상하/하차시간
        self.departure_time = None  # 출발시각

    def __repr__(self):
        return str(self.ord_no)

class Car: # 이동 차량
    def __init__(self, VehicleID, max_capa, start_center,fixed_cost, variable_cost):
        self.vehicle_id = VehicleID
        self.start_center = start_center
        self.max_capa = max_capa    # 적재 capa_max
        self.fixed_cost = fixed_cost    # 차량 고정비
        self.variable_cost = variable_cost  # 차량 변동비
        self.fixed_cost_incurred = False    # 고정비가 계산이 되었는지
        self.now_time = datetime.strptime("2023-05-01 00:00", "%Y-%m-%d %H:%M")

    def initialize(self):   # 결과 테이블
        self.served_order = []
        self.can_move = True
        self.conut = 0
        self.volume = 0  # 현재 적재량
        self.total_volume = 0  # 누적 적재량
        self.travel_distance = 0  # 총 주행거리
        self.work_time = 0  # 총 작업 시간
        self.travel_time = 0  # 총 이동 시간
        self.service_time = 0  # 총 하역 시간
        self.waiting_time = 0  # 총 대기 시간
        self.total_fixed_cost = 0  # 누적된 차량 고정비
        self.total_variable_cost = 0  # 누적된 차량 변동비


    def loading(self, target: Order):   # 상차 작업
        if not self.doable(target): raise Exception('Infeasible Loading!')
        target.delivered = True
        dist, time = distance.calculate_distance_time(self.start_center, target.terminal_ID)
        self.dist = dist
        self.time = time
        self.travel_distance += dist
        self.travel_time += time
        self.volume += target.cbm
        self.total_volume += target.cbm
        self.conut += 1
        # self.coord = target.start_coord
        self.served_order.append(target)
        self.start_center = target.terminal_ID
        self.can_move = False
        self.loaded_order = True
        self.total_variable_cost += self.variable_cost * self.dist  # 누적된 차량 변동비
        target.vehicle_id = self.vehicle_id
        if not self.fixed_cost_incurred:
            self.total_fixed_cost += self.fixed_cost
            self.fixed_cost_incurred = True
        self.now_time += timedelta(minutes=time)

    def unloading(self, target: Order):     # 하차 작업
        self.volume = 0     # 차량 적재량 0으로 만들기
        dist, time = distance.calculate_distance_time(self.start_center, target.arrive_id)
        self.travel_distance += dist
        self.travel_time += time
        self.start_center = target.arrive_id
        self.total_variable_cost += self.variable_cost * self.dist
        self.can_move = True
        self.now_time += timedelta(minutes=time)
        if time != 0:
            self.now_time += timedelta(minutes=60)

    def doable(self, target: Order) -> bool: # -> return 값 힌트
        load_dist, load_time = distance.calculate_distance_time(self.start_center, target.terminal_ID)
        unload_dist, unload_time = distance.calculate_distance_time(target.terminal_ID, target.arrive_id)
        max_range = datetime(self.now_time.year, self.now_time.month, self.now_time.day) + timedelta(days=3) # 72시간 이내
        if load_time >= 60 or unload_time >= 60:
            load_hours, load_minutes = divmod(load_time, 60)
            unload_hours, unload_minutes = divmod(unload_time, 60)
            car_time = datetime(self.now_time.year, self.now_time.month, self.now_time.day) \
                       + timedelta(hours=load_hours) + timedelta(hours=unload_hours) + timedelta(minutes=load_time) + timedelta(minutes=unload_time)  # 차량 처리하기까지 걸리는 시간

        else:
            car_time = datetime(self.now_time.year, self.now_time.month, self.now_time.day) \
                       + timedelta(minutes=load_time) + timedelta(minutes=unload_time) # 차량 처리하기까지 걸리는 시간
        if target.delivered:    # 아직 미완료 주문만 처리w_time.month,
            return False
        elif self.max_capa < self.volume + target.cbm:  # 상품을 차에 실을 수 있는지 (적재량)
            return False
        elif car_time > max_range: # 72시간 이내 처리되는지
            return False
        else:
            return True

    def __repr__(self):
        return str(self.vehicle_id)

class Result: # 결과 테이블
    def __init__(self, VehicleID, Count, Volume, TravelDistance, WorkTime, TravelTime, ServiceTime, WaitingTime, TotalCost, FixedCost, VariableCost):
        self.VehicleId = VehicleID
        self.Count = Count
        self.Volume = Volume
        self.TravelDistance = TravelDistance
        self.WorkTime = WorkTime
        self.TravelTime = TravelTime
        self.ServiceTime = ServiceTime
        self.WaitingTime = WaitingTime
        self.TotalCost = TotalCost
        self.FixedCost = FixedCost
        self.VariableCost = VariableCost

    def result_table(self):
        pd.set_option('display.max_columns', None)
        fields = ['VehicleID', 'Count', 'Volume', 'TravelDistance', 'WorkTime', 'TravelTime', 'ServiceTime',
                  'WaitingTime', 'TotalCost', 'FixedCost', 'VariableCost']
        df = pd.DataFrame(columns=fields,
                          data=[[self.VehicleId, self.Count, self.Volume, self.TravelDistance, self.WorkTime,
                                 self.TravelTime, self.ServiceTime, self.WaitingTime, self.TotalCost, self.FixedCost, self.VariableCost]])
        return df