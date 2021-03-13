import numpy as np
from datasets import input_data


# функция для расчета суммы удовольствия муравьёв
def total_desire(distance, feromones):
    total_desire = ((distance ** input_data.beta) * (feromones ** input_data.alfa))
    return total_desire


# расчет значений удовольстия от текущего выбора до всех городов в строке
def desire(choice, distance, feromones):
    np.seterr(divide='ignore', invalid='ignore')  # игнор ошибок деления на NaN
    desire = total_desire(distance, feromones)[choice, :] / np.nansum(total_desire(distance, feromones)[choice, :])
    return desire


def null_distance(choice_list):
    distance = input_data.distance
    for n in choice_list:
        distance[:, n] = np.nan  # убираем значения пересчитанных городов
        distance[n, :] = np.nan
    return distance


def null_feromones(choice_list):
    feromones = input_data.feromones
    for n in choice_list:
        feromones[:, n] = np.nan
        feromones[n, :] = np.nan
    return feromones


# расчет значений удовольстия от текущего выбора до оставшихся городов
def next_city(choice_list, choice):
    distance = null_distance(choice_list)
    feromones = null_feromones(choice_list)
    local_desire = desire(choice, distance, feromones)
    return local_desire


# функция рулетки
def roulette():
    roulette = np.random.randint(0, 99) / 100
    return roulette


#choice_list = [0, 3, 7, 4]

#k = next_city([], 0)
#print('Pleasure to remaining cities:', k)

choice_list = [[], 0, 3, 7, 4, 8, 6, 9, 5, 2, 1, 0]
order = []
k = []

for m in range(0, len(choice_list)):
    try:
        order = np.array(np.append(order, choice_list[m]), dtype=int)
        print(m, 'ордер', order.tolist(), choice_list[m+1])
        print(m, next_city(order.tolist(), choice_list[m+1]))
    except:
        print('pass_ордер', order.tolist())
        pass
print(order.tolist())

travel = 0

for n in range(1, len(choice_list)):
    try:
        travel = travel + 200/input_data.route[int(choice_list[n]), int(choice_list[n+1])]
        print('n=',  n, int(choice_list[n]), int(choice_list[n+1]), input_data.route[int(choice_list[n]), int(choice_list[n+1])])
    except:
        print('pass')
        pass
print(travel)