#! /usr/local/bin/python3

import random
import copy

"""
onmax_ga.py
OneMax問題をGAで解くスクリプト
日経ソフトウェア2019年3月号 「Pythonで遺伝的アルゴリズムのプログラムを作る」
Copyright (C) 2019 J.Kawahara
2019.3.14 J.Kawahara 新規作成
"""

# パラメータ
LIST_SIZE = 10      # 0/1のリスト長（遺伝子長）

POPULATION_SIZE = 10    # 集団の個体数
GENERATION = 25         # 世代数
MUTATE = 0.1            # 突然変異の確率
SELECT_RATE = 0.5       # 選択割合


def calc_fitness(individual):
    """適応度を計算する

    Parameters
    ----------
    individual : list
        個体（0/1のリスト）

    Returns
    -------
    int
        適応度（リスト要素の合計値）
    """
    return sum(individual)


def sort_fitness(population):
    """集団を適応度順にソートする

    Parameters
    ----------
    population : list
        個体のリスト

    Returns
    -------
    list
        ソート済みの個体のリスト
    """
    fp = []
    for individual in population:
        fitness = calc_fitness(individual)
        fp.append((fitness, individual))
    fp.sort(reverse=True)

    sorted_population = []

    for fitness, individual in fp:
        sorted_population.append(individual)

    return sorted_population


def selection(population):
    """選択 適応度の高い個体を残す

    Parameters
    ----------
    population : list
        個体のリスト

    Returns
    -------
    list
        残すべき適応度の高い個体のリスト
        （要素数は「集団の個体数」*「選択割合」
    """
    sorted_population = sort_fitness(population)
    n = int(POPULATION_SIZE * SELECT_RATE)
    return sorted_population[:n]


def crossover(ind1, ind2):
    """交差

    ind1をコピーして新しい個体ind を作成する
    ランダムに決めたr1〜r2の範囲をind2の遺伝子に置き換える

    Parameters
    ----------
    ind1, ind2 : list
        親となる個体

    Returns
    -------
    list
        子となる個体
    """
    r1 = random.randint(0, LIST_SIZE - 1)
    r2 = random.randint(r1 + 1, LIST_SIZE)
    ind = copy.deepcopy(ind1)
    ind[r1:r2] = ind[r1:r2]
    return ind


def mutation(ind1):
    """突然変異

    突然変異確率に従って突然変異させる

    Parameters
    ----------
    ind1 : list
        元となる個体

    Returns
    -------
    list
        突然変異後の個体（突然変異しない場合は元となる個体のコピー  ）
    """
    ind2 = copy.deepcopy(ind1)
    for i in range(LIST_SIZE):
        if random.random() < MUTATE:
            ind2[i] = random.randint(0, 1)
    return ind2


if __name__ == '__main__':
    # 初期化
    population = []
    for i in range(POPULATION_SIZE):
        individual = []
        # ランダムで個体を作成する
        for j in range(LIST_SIZE):
            individual.append(random.randint(0, 1))

        population.append(individual)

    for generation in range(GENERATION):
        print(str(generation + 1) + u"世代")

        # 選択
        population = selection(population)

        n = POPULATION_SIZE - len(population)
        for i in range(n):
            # 集団から２個体をランダムに選び、交差した個体を生成する
            r1 = random.randint(0, len(population) - 1)
            r2 = random.randint(0, len(population) - 1)

            # 交差
            individual = crossover(population[r1], population[r2])

            # 突然変異
            individual = mutation(individual)

            population.append(individual)

        for individual in population:
            print(individual)
