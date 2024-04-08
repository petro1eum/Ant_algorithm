import numpy as np
from datasets import input_data

np.seterr(divide='ignore', invalid='ignore')

def total_desire(distance, pheromones):
    return (distance ** input_data.beta) * (pheromones ** input_data.alfa)

def desire(choice, distance, pheromones):
    total = total_desire(distance, pheromones)
    return total[choice, :] / np.sum(total[choice, :])

def null_matrix(choice_list, matrix):
    var_matrix = np.array(matrix)
    var_matrix[choice_list, :] = np.nan
    var_matrix[:, choice_list] = np.nan
    return var_matrix

def next_city(choice_list, choice):
    loc_distance = null_matrix(choice_list, input_data.track)
    loc_pheromones = null_matrix(choice_list, input_data.feromes)
    return desire(choice, loc_distance, loc_pheromones)

def travel_calc(choice_list):
    travel = 0
    for city1, city2 in zip(choice_list[:-1], choice_list[1:]):
        travel += 200 / input_data.route[city1, city2]
    return travel

def roulette_run(local_desire):
    valid_indices = ~np.isnan(local_desire)
    if np.any(valid_indices):
        probabilities = local_desire[valid_indices]
        probabilities /= np.sum(probabilities)
        return np.random.choice(np.arange(len(local_desire))[valid_indices], p=probabilities)
    else:
        return np.random.choice(np.arange(len(local_desire)))

def update_choice(choice_list, choice):
    if choice not in choice_list:
        return np.append(choice_list, choice).astype(int).tolist()
    else:
        return choice_list

distance_list = []
choice_list = []
choice = 0

for m in range(15000):
    first_choice = choice
    while len(choice_list) < len(input_data.track):
        new_choice = roulette_run(next_city(choice_list, choice))
        choice_list = update_choice(choice_list, new_choice)
        choice = new_choice
    choice_list = update_choice(choice_list, first_choice)
    k = travel_calc(choice_list)
    if np.isfinite(k):
        distance_list.append((k, choice_list))
    choice_list = []
    choice = 0

# Сортировка distance_list по возрастанию значений расстояний
sorted_distance_list = sorted(distance_list, key=lambda x: x[0])

# Вывод двух результатов с минимальным расстоянием
print("Два результата с минимальным расстоянием:")
for i in range(min(2, len(sorted_distance_list))):
    distance, route = sorted_distance_list[i]
    print(f"Расстояние: {distance}, Маршрут: {route}")