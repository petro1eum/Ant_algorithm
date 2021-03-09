import numpy as np
from datasets import input_data


# функция для расчета суммы удовольствия муравьёв
def total_desire(distance, feromones):
    total_desire = ((distance ** input_data.beta) * (feromones ** input_data.alfa))
    return total_desire


# функция для расчета нормированного удовольствия каждого муравья
def desire(choice, distance, feromones):
    desire = ((distance[choice, :] ** input_data.beta) * (feromones[choice, :] ** input_data.alfa)) / np.nansum(total_desire(distance, feromones)[choice, :])
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


# берем на вход обрезанный массив и подаем его на вход в функцию расчета удовольствия
def next_city(choice_list, choice):
    distance = null_distance(choice_list)
    #    print(distance, 'distance')
    feromones = null_feromones(choice_list)
    #    print(feromones, 'feromones')
    local_desire = desire(choice, distance, feromones)  # отнимаем длину, чтобы не пересчитывать вручную номер столбца
    #    print(local_desire, 'local_desire')
    return local_desire


# функция рулетки
def roulette():
    roulette = np.random.randint(0, 99) / 100
    return roulette


choice_list = [0, 3, 7, 4]

k = null_distance(choice_list)
j = null_feromones(choice_list)

y = desire(8, k, j)

print(y, 'total desire')

print('place holder')


k = next_city([choice_list], 3)  # choice_list - колонки в изначальной теблице, choice - новая колонка в обрезанном наборе
print('Next City #:', k)
