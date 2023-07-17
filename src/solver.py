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
        3: [datetime.strptime("13:00", "%H:%M").time(), datetime.strptime("18:00", "%H:%M").time()]
    }

    date_list = [
        '2023-05-01',
        '2023-05-02',
        '2023-05-03',
        '2023-05-04',
        '2023-05-05',
        '2023-05-06'
    ]  # 처리할 날짜 리스트

    a = 0
    b = 0

    for date in date_list:
        for group in range(4):
            group_orders = [
                order for order in prob_instance.ord_list
                if order.group == group and order.date == date and order.time_window[0] in group_time_windows[group]
            ]

            for order in group_orders:   # 상차 작업
                filtered_cars = list(
                    filter(lambda car: car.start_center == order.terminal_ID and car.doable(order), prob_instance.car_list))

                if filtered_cars:
                    closest_car = min(
                        filtered_cars,
                        key=lambda car: distance.calculate_distance_time(car.start_center, order.terminal_ID)[0]
                    )
                else:
                    closest_car = min(
                        filter(lambda car: car.doable(order), prob_instance.car_list),
                        key=lambda car: distance.calculate_distance_time(car.start_center, order.terminal_ID)[0]
                    )

                closest_car.loading(order)
                a += 1

            for car in prob_instance.car_list:  # 하차 작업
                if car.can_move == False:
                    for order in car.served_order:
                        if order in group_orders:
                            car.unloading(order)
                            b += 1
        print(date, '총 상차 주문 수:', a)
        print(date, '총 하차 주문 수:', b)
        a = 0
        b = 0

    objective = 0
    for car in car_list:    # 운영비용 계산
        objective += car.total_fixed_cost + car.travel_distance * car.variable_cost

    solution = {}
    solution['Objective'] = objective

    return solution
