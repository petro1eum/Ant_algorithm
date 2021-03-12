import numpy as np
from datasets import input_data


# функция для расчета суммы удовольствия муравьёв
def total_desire(distance, feromones):
    total_desire = ((distance ** input_data.beta) * (feromones ** input_data.alfa))
    return total_desire


# функция для расчета нормированного удовольствия каждого муравья
def desire(choice, distance, feromones):
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


choice_list = [0, 3, 7, 4]

k = next_city([choice_list], 8)
print('Pleasure to remaining cities:', k)
