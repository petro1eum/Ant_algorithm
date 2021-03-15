import numpy as np
from datasets import input_data


# функция для расчета суммы удовольствия муравьёв
def total_desire(distance1, feromones):
    total_desire = ((distance1 ** input_data.beta) * (feromones ** input_data.alfa))
    return total_desire


# расчет значений удовольстия от текущего выбора до всех городов в строке
def desire(choice, distance1, feromones):
    np.seterr(divide='ignore', invalid='ignore')  # игнор ошибок деления на NaN
    desire = total_desire(distance1, feromones)[choice, :] / np.nansum(total_desire(distance1, feromones)[choice, :])
    return desire


def null_distance(choice_list):
    var_distance = np.array(input_data.track)  # тут трахался три дня, т.к. input_data.distance после вычислений -> nan
    for n in choice_list:
        var_distance[:, n] = np.nan  # убираем значения пересчитанных городов
        var_distance[n, :] = np.nan
    return var_distance


def null_feromones(choice_list):
    var_feromones = np.array(input_data.feromes)
    for n in choice_list:
        var_feromones[:, n] = np.nan
        var_feromones[n, :] = np.nan
    return var_feromones


# расчет значений удовольстия от текущего выбора до оставшихся городов
def next_city(choice_list, choice):
    loc_distance = null_distance(choice_list)
    loc_feromones = null_feromones(choice_list)
    local_desire = desire(choice, loc_distance, loc_feromones)
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
#    print('значение рулетки:', chance)
    for value in range(0, len(local_desire)):
        if np.isnan(local_desire[value]) == False:
            moving_value = local_desire[value] + moving_value
            if moving_value >= chance:
#                print('накопленная сумма =', moving_value)
                break

    return int(value)


# функция, которая обновляет список уже выбранных городов
def update_choice(choice_list, choice):  # необходимо определить перемернные как глобальные
    choice_list = np.array(np.append(choice_list, choice), dtype=int)
    return choice_list.tolist()


# первый выбор задается вручную
distance_list = []
choice_list = []
choice_set = {}
choice = 0
first_choice = choice

for m in range(50):
    for value in range(0, len(input_data.track)):
#        print('value', value, choice_list, choice)
#        print('матрица выбора', next_city(choice_list, choice))
        new_choice = roulette_run(next_city(choice_list, choice))
#        print('new choice', new_choice)
        choice_list = update_choice(choice_list, choice)
#        print('новый choice_list', choice_list)
        choice = new_choice

    choice_list = np.array(np.append(choice_list, first_choice), dtype=int)
#    print('новый choice_list', choice_list.tolist())
    k = travel_calc(choice_list)
    distance_matrix = {
        k: choice_list
    }
    distance_list.append(distance_matrix)
    choice_list = []
    choice = 0
    first_choice = choice

print(distance_list)






#k = next_city([], 0)
#print('Pleasure to remaining cities:', k)
#d = roulette_run(k)
#print('next city is', d)


