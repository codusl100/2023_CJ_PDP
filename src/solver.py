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

    filtered_orders = [     # ex) 그룹이 0이고, 5월1일, 타임 윈도우 안에 들어오는 것들
        order for order in prob_instance.ord_list
        if order.group == 0 and order.date == '2023-05-01' and order.time_window[0] in group_time_windows[0]
    ]

    a = 0

    for order in filtered_orders:
        for car in prob_instance.car_list:
            if car.doable(order) and order.terminal_ID == car.start_center: # 차가 상품을 실을 수 있고, 상품의 위치랑 차의 위치가 동일한 경우
                car.loading(order)
                print("차량:", car, "-> 주문:", order)
                a += 1
                break

    print('총 처리 주문 수:', a)

    objective = 0
    for car in car_list:    # 운영비용 계산
        objective += car.total_fixed_cost + car.total_variable_cost

    solution = {}
    solution['Objective'] = objective

    return solution