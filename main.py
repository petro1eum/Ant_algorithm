import numpy as np
from datasets import input_data


# distance = np.array(input_data.distance)
# feromones = np.array(input_data.feromones)

# функция для расчета суммы удовольствия муравьёв
def total_desire(choice, distance, feromones):
    total_desire = ((distance[choice, :] ** input_data.beta) * (feromones[choice, :] ** input_data.alfa)).sum()
    return total_desire


# функция для расчета нормированного удовольствия каждого муравья
def desire(choice, distance, feromones):
    desire = ((distance[choice, :] ** input_data.beta) * (feromones[choice, :] ** input_data.alfa)) / total_desire(
    choice, distance, feromones)
    return desire


# функция для обрезания города, которые уже пересчитали (нужно будет добавить обновляемый список отрезанных городов)
def cut_distance(choice_list):
    distance = np.delete(np.array(input_data.distance), choice_list, axis=1)
    distance = np.delete(distance, choice_list, axis=0)
    return distance


def cut_feromones(choice_list):
    feromones = np.delete(np.array(input_data.feromones), choice_list, axis=1)
    feromones = np.delete(feromones, choice_list, axis=0)
    return feromones


# функция рулетки
def roulette():
    roulette = np.random.randint(0, 99) / 100
    return roulette


# берем на вход обрезанный массив и подаем его на вход в функцию расчета удовольствия
def next_city(choice_list, choice):
    distance = cut_distance(choice_list)
    #    print(distance, 'distance')
    feromones = cut_feromones(choice_list)
    #    print(feromones, 'feromones')
    local_desire = desire(choice, distance, feromones)  # отнимаем длину, чтобы не пересчитывать вручную номер столбца
    #    print(local_desire, 'local_desire')
    return local_desire


# y = total_desire(0)
# print(y)
# z = desire(0)
# print(z[2])

# z = cut_distance([0, 1])
# print(z)

# z = cut_distance([0])
# print(z)

# choice_list = [0, 1]

k = next_city([0, 3, 7], 2)  # choice_list - колонки в изначальной теблице, choice - новая колонка в обрезанном наборе
print(len(k), 'k')
