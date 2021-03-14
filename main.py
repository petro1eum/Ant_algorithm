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


# расчёт суммы расстояний всех городов
def travel_calc(choice_list):
    travel = 0
    for n in range(1, len(choice_list)):
        try:
            travel = travel + 200 / input_data.route[int(choice_list[n]), int(choice_list[n + 1])]
        #            print('n=', n, int(choice_list[n]), int(choice_list[n + 1]),
        #                  input_data.distance[int(choice_list[n]), int(choice_list[n + 1])])
        except IndexError:
            pass
    return travel


# функция рулетки
def roulette():
    roulette = np.random.randint(0, 99) / 100
    return roulette


# функция приложения рулетки к списку вероятностей следующего города
def roulette_run(local_desire):
    moving_value = 0
    chance = roulette()
    print('значение рулетки:', chance)
    for value in range(0, len(local_desire)):
        if np.isnan(local_desire[value]) == False:
            moving_value = local_desire[value] + moving_value
            if moving_value >= chance:
                print('накопленная сумма =', moving_value)
                break

    return int(value)


# функция, которая обновляет список уже выбранных городов
def update_choice(choice_list, choice):  # необходимо определить перемернные как глобальные
    choice_list = np.array(np.append(choice_list, choice), dtype=int)
    return choice_list.tolist()


# первый выбор задается вручную
distance_matrix = []

for m in range(3):
        choice_list = []
        choice = 0
        first_choice = 0
        distance = input_data.route
        feromones = input_data.feromones
        for value in range(0, len(input_data.distance)):
            print('матрица выбора', next_city(choice_list, choice))
            new_choice = roulette_run(next_city(choice_list, choice))
            print('new choice', new_choice)
            choice_list = update_choice(choice_list, choice)
            print('новый choice_list', choice_list)
            choice = new_choice
        choice_list = np.array(np.append(choice_list, first_choice), dtype=int)
        print('новый choice_list', choice_list.tolist())
        k = travel_calc(choice_list)
        distance_matrix = np.array(np.append(distance_matrix, k), dtype=int)

print('call function travel_calc', distance_matrix)




#k = next_city([], 0)
#print('Pleasure to remaining cities:', k)
#d = roulette_run(k)
#print('next city is', d)


