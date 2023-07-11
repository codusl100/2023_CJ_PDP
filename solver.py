def rule_solver(prob_instance):
    # 우선 처리할 Order들을 담을 리스트
    print('solver start')

    filtered_orders = list(filter(lambda order: order.group == 0, prob_instance.ord_list))  # 예시로 일단 group0인 경우만

    for order in filtered_orders:
        for car in prob_instance.car_list:
            if car.doable(order) and order.terminal_ID == car.start_center: # 차가 상품을 실을 수 있고, 상품의 위치랑 차의 위치가 동일한 경우
                car.loading(order)
                print("차량:", car, "-> 주문:", order)
                break

    solution = {}

    return solution
