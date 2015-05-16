#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from itertools import combinations

relative_importance_table = (
    {'desc': 'Умеренное превосходство', 'value': 3}, #0
    {'desc': 'Существенное или сильное превосходство', 'value': 5}, #1
    {'desc': 'Значительное превосходство', 'value': 7}, #2
    {'desc': 'Очень большое превосходство', 'value': 9}, #3
    {'desc': 'Равная важность', 'value': 1}, #4
    {'desc': 'Очень большое превосходство второго', 'value': 1.0/9}, #5
    {'desc': 'Значительное превосходство второго', 'value': 1.0/7}, #6
    {'desc': 'Существенное или сильное превосходство второго', 'value': 1.0/5}, #7
    {'desc': 'Умеренное превосходство второго', 'value': 1.0/3}, #8
)

criterias = ('Зарплата', 'Перспективы карьерного роста', 'Интересные задачи')#, 'Сильная команда')
alternatives = ('Mail.ru', 'Yandex', 'Google')

def calc_matrix_self_vector(m):
    from scipy.stats.mstats import gmean
    return gmean(m, axis=1)
def normalize_vector(v):
    return v / v.sum()
def pretty_flist(flist):
    return ['{:.2f}'.format(f) for f in flist]

def compare_elems(elems):
    elems_cmp = np.zeros(shape=(len(elems), len(elems)))
    for c0, c1 in combinations(enumerate(elems), 2):
        cmp_index = input('"{}" относится к "{}": '.format(c0[1], c1[1]))
        elems_cmp[c0[0], c1[0]] = relative_importance_table[cmp_index]['value']
        elems_cmp[c1[0], c0[0]] = relative_importance_table[len(relative_importance_table) - 1 - cmp_index]['value']
    np.fill_diagonal(elems_cmp, 1)
    print('Матрица сравнений: \n{}'.format(elems_cmp))
    elems_cmp_self_vector = calc_matrix_self_vector(elems_cmp)
    print('Собственный вектор: {}'.format(pretty_flist(elems_cmp_self_vector)))
    elems_cmp_self_vector = normalize_vector(elems_cmp_self_vector)
    print('Нормализованный собственный вектор: {}'.format(pretty_flist(elems_cmp_self_vector)))
    return elems_cmp_self_vector


print('Критерии: ' + ' | '.join(criterias))
print('Альтернативы: ' + ' | '.join(alternatives))

np.set_printoptions(precision=2)
print('Варианты сравнения:')
for i, comparison in enumerate(relative_importance_table):
    print('  -- #{} = {} (значение {:.2f})'.format(i, comparison['desc'], comparison['value']))

print('\nСравните критерии:')
criterias_self_vector = compare_elems(criterias)

print('\nСравните альтернативы по критериям:')
alternatives_matrix = np.empty(shape=(len(criterias),len(alternatives)))
for i, crit in enumerate(criterias):
    print('\nПо критерию "{}":'.format(crit))
    alternatives_matrix[i] = compare_elems(alternatives)

print('\n\nМатрица собственных векторов альтернатив по всем критериям: \n{}'.format(alternatives_matrix))
alternatives_importance = np.squeeze(np.asarray(alternatives_matrix.T * np.matrix(criterias_self_vector).T))
print('Собственный вектор критериев: {}'.format(pretty_flist(criterias_self_vector)))
print('\nВажность альтернатив:')
for importance, name in sorted(zip(list(alternatives_importance), alternatives), key=lambda v: v[0], reverse=True):
    print('  -- {} = {:.2f}'.format(name, importance))
