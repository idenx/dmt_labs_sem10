import math
import numpy as np
from nelder_mead import nelder_mead
from genalgo import GenAlgo
import sys

def get_car_score(hp, age, cost):
    min_hp = 80.0
    min_age = 0.0
    max_age = 10.0

    min_cost = 1e5
    max_cost = 1e6

    if hp <= min_hp or age < min_age or age >= max_age or cost <= min_cost or cost >= max_cost:
        return 0

    cost -= cost * age / (max_age + 1)

    avg_repair_cost = cost * 0.10
    max_repair_cost = avg_repair_cost + hp * math.sqrt(cost) # cri 1
    REPAIR_NORM_COEF = 500e3 / 100.0
    repair_need = REPAIR_NORM_COEF * hp / (cost) # cri 2
    hp_preception = math.log(hp - min_hp)
    driving_pleasure_for_driver = hp_preception + 2.0 * math.log(cost)  # cri 3
    driving_pleasure_for_passenger = math.log(cost) / 3.0 - 0.4 * hp_preception # cri 4
    months_to_full_payment = cost / 30000.0 # cri 5
    if months_to_full_payment > 12:
        months_to_full_payment *= 1.1

    a = 1.9 * 100000 / (max_repair_cost * repair_need)
    b = (0.7 * driving_pleasure_for_driver + 0.3 * driving_pleasure_for_passenger) / 10.0
    c = 5.0 / months_to_full_payment

    retv = (a + b + c)
    #print('score(hp=%.1f, age=%.4f, cost=%.1f [%.1f + %.1f + %.1f]) = %.2f' % (hp, age, cost, a, b, c, retv))
    return retv

if __name__ == '__main__':
    def f(x):
        ret = 1.0 / (get_car_score(x[0], x[1], x[2]) + 0.00001)
        return ret
    x, y, it = nelder_mead(f, np.array((200.0, 1.0, 8e5)))
    print('Nelder-Mead solution: horse powers: %.1f, age: %.1f, cost: %.1f, func_val: %.3f' % (x[0], x[1], x[2], y))

    gen_res = GenAlgo(2, 20, 3, 10).execute([81, 500, 1e5], [0.0, 9.9, 1.2*1e5], f, threshold=float(sys.argv[1]), tol=0.001, max_evals=1e6)
    print('Gen algo solution: horse powers: %.1f, age: %.1f, cost: %.1f, func_val: %.3f' % (gen_res.x[0], gen_res.x[1], gen_res.x[2], gen_res.f))
