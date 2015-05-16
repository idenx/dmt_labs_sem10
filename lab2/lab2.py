import math

def calc_self_vector(matrix):
    self_vector = []
    for i in range(0, len(matrix)):
        prod = 1
        for j in range(0, len(matrix[i])):
            prod = prod * matrix[i][j]
        self_vector.append(prod ** (1.0 / len(matrix)))
    return self_vector

def normalize_vector(vector):
    vec_len = sum(vector)
    return list(map(lambda x: x / vec_len, vector))

importrance_table = [
        {'description': 'Равная важность', 'value': 1}, #0
        {'description': 'Умеренное превосходство', 'value': 3}, #1
        {'description': 'Существенное или сильное превосходство', 'value': 5}, #2
        {'description': 'Значительное превосходство', 'value': 7}, #3
        {'description': 'Очень большое превосходство', 'value': 9}, #4
        {'description': 'Умеренное превосходство второго', 'value': 1.0/3}, #5
        {'description': 'Существенное или сильное превосходство второго', 'value': 1.0/5}, #6
        {'description': 'Значительное превосходство второго', 'value': 1.0/7}, #7
        {'description': 'Очень большое превосходство второго', 'value': 1.0/9}, #8
    ]

criterias = ['Цена', 'Спортивность', 'Вместимость']
alternatives = ['BMW 3er', 'Mercedes C-Klasse', 'Mercedes GLA']

print('Критерии')
for criteria in criterias:
    print(criteria)
print()
print('Альтернативы')
for alternative in alternatives:
    print(alternative)
print()
print('Таблица важности:')
i = 0
for factor in importrance_table:
    print('%s) %s: %s' % (i, factor['description'], factor['value']))
    i = i + 1
print()
print('Укажите Ваше мнение о соотношениях:')
criteria_compare_matrix = [[None for _ in range(0, len(criterias))] for _ in range(0, len(criterias))]
for i in range(0, len(criterias)):
    criteria_compare_matrix[i][i] = importrance_table[0]['value']
    for j in range(i+1, len(criterias)):
        choice = int(input('%s по отношению к %s: ' % (criterias[i], criterias[j])))
        criteria_compare_matrix[i][j] = importrance_table[choice]['value']
        criteria_compare_matrix[j][i] = 1.0 / importrance_table[choice]['value']
print(criteria_compare_matrix)
self_vector = calc_self_vector(criteria_compare_matrix)
print('Собственный вектор: %s' % self_vector)
self_vector = normalize_vector(self_vector)
print('Собственный вектор после нормализации: %s' % self_vector)

criterias_self_vectors = []
for i in range(0, len(criterias)):
    print()
    print('По критерию %s' % criterias[i])
    per_criteria_matrix = [[None for _ in range(0, len(criterias))] for _ in range(0, len(criterias))]
    for j in range(0, len(alternatives)):
        per_criteria_matrix[j][j] = importrance_table[0]['value']
        for k in range(j + 1, len(alternatives)):
            choice = int(input('%s по отношению к %s: ' % (alternatives[j], alternatives[k])))
            per_criteria_matrix[j][k] = importrance_table[choice]['value']
            per_criteria_matrix[k][j] = 1.0 / importrance_table[choice]['value']
    per_criteria_self_vector = calc_self_vector(per_criteria_matrix)
    print('Матрица %s' % per_criteria_matrix)
    print('Собственный вектор %s' % per_criteria_self_vector)
    per_criteria_self_vector = normalize_vector(per_criteria_self_vector)
    print('Собственный вектор после нормализации: %s' % per_criteria_self_vector)
    criterias_self_vectors.append(per_criteria_self_vector)
print()

final_scores = []
for j in range(0, len(alternatives)):
    s = 0
    for i in range(0, len(criterias)):
        s = s + (criterias_self_vectors[i][j] * self_vector[i])
    final_scores.append(s)
print('Коэффициенты важности: %s' % final_scores)
print()
best_alternative_index = final_scores.index(max(final_scores))
print('Ваш выбор: %s' % alternatives[best_alternative_index])
