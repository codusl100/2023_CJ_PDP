from prob_builder import *

def rule_solver(prob_instance):
    # 우선 처리할 Order들을 담을 리스트
    print('solver start')

    ord_list = prob_instance.ord_list
    for ord in ord_list:
        ord.initialize()

    car_list = prob_instance.car_list
    for car in car_list:
        car.initialize()

    group_time_windows = {
        0: [datetime.strptime("00:00", "%H:%M").time(), datetime.strptime("18:00", "%H:%M").time()],
        1: [datetime.strptime("07:00", "%H:%M").time(), datetime.strptime("10:00", "%H:%M").time()],
        2: [datetime.strptime("07:00", "%H:%M").time(), datetime.strptime("10:00", "%H:%M").time(),
            datetime.strptime("13:00", "%H:%M").time()],
        3: [datetime.strptime("18:00", "%H:%M").time()]
    }

    date_list = [
        '2023-05-01',
        '2023-05-02',
        '2023-05-03',
        '2023-05-04',
        '2023-05-05',
        '2023-05-06'
    ]  # 처리할 날짜 리스트

    group_list = [
        '00:00',
        '06:00',
        '12:00',
        '18:00'
    ]
    a = 0
    b = 0
    load = 0
    unload = 0
    pending_orders = [] # 현재 group에서 처리하지 못하는 물건들을 저장하는 리스트 => 다음 group에서 처리하기 위해

    for date in date_list:
        for group in range(4):
            group_orders = pending_orders
            pending_orders = []
            undelivered_orders = [order for order in ord_list if not order.delivered] # 배송처리가 안된 물건들
            for order in undelivered_orders:
                if order.group == group and order.date == date:     # 날짜와 group별로 처리
                    if order.time_window[0].time() in group_time_windows[group]:    # 그룹별로 처리할 수 있는 time_window에 포함되는 주문인지 판별
                        group_orders.append(order)                  # 맞다면 group_orders에 추가
                    else:
                        pending_orders.append(order)        # 아니라면 pending_orders에 추가

            for order in group_orders:   # 상차 작업
                try:
                    filtered_cars = list(filter(lambda car: car.start_center == order.terminal_ID and car.doable(order),
                               car_list))   # 차의 현재 위치와 물건의 출발 위치가 동일한 차량 추출 + 배달 가능 여부 판단
                    if filtered_cars:
                        closest_car = min(  # 추출된 차량이 여러 대라면 차량의 현재 위치와 상품의 도착 위치가 제일 가까운 차량으로 배정
                            filtered_cars,
                            key=lambda car: distance.calculate_distance_time(car.start_center, order.arrive_id)[0]
                        )
                    else:   # 추출된 차량이 없다면
                        closest_car = min(  # 차량의 현재 위치와 상품의 현재 위치가 제일 가까운 차량으로 배정
                            filter(lambda car: car.doable(order), car_list),
                            key=lambda car: distance.calculate_distance_time(car.start_center, order.terminal_ID)[0]
                        )
                    if closest_car.now_time < datetime.strptime(date + group_list[group], "%Y-%m-%d%H:%M"): # 차량 시간 조정
                        closest_car.now_time = datetime.strptime(date + group_list[group], "%Y-%m-%d%H:%M")

                    closest_car.loading(order)  # 차가 물건을 실음
                    a += 1
                except:
                    pending_orders.append(order)    # 만일 상품을 운반할 차량이 없다면 다음 group에서 처리하기 위해 pending_orders에 저장

            # 하차 작업 순서 정렬
            for car in [car for car in prob_instance.car_list if not car.can_move]:
                car.served_order.sort(
                    key=lambda order: distance.calculate_distance_time(car.start_center, order.arrive_id)[0])

            for car in prob_instance.car_list:  # 하차 작업
                if car.can_move == False:
                    for order in car.served_order:
                        if order in group_orders:
                            car.unloading(order)
                            b += 1
            u = 0
        print(date, '총 상차 주문 수:', a)
        print(date, '총 하차 주문 수:', b)
        load += a
        unload += b
        a = 0
        b = 0
    print('상차 작업 완료 수', load)
    print('하차 작업 완료 수', unload) # Count

    objective = 0
    vehicleId = car_list[-1]

    for car in car_list:    # 운영비용 계산
        objective += car.total_fixed_cost + car.travel_distance * car.variable_cost

    total_distance = sum(map(lambda car: car.travel_distance, car_list))
    total_fixedCost = sum(map(lambda car: car.total_fixed_cost, car_list))
    total_variableCost = sum(map(lambda car: car.variable_cost, car_list))
    total_volume = sum(map(lambda car: car.max_capa, car_list))

    solution = {}
    solution['Objective'] = objective # TotalCost
    # [vehicleId, unload, total_volume, total_distance, 0, 0, 0, 0, objective, total_fixedCost, total_variableCost]
    result_table = Result(vehicleId, unload, total_volume, total_distance, 0, 0, 0, 0, objective, total_fixedCost, total_variableCost)
    return result_table.result_table()