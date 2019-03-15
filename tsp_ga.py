#! /usr/local/bin/python3

import sys
import random
import math
import copy
import tkinter

# パラメータ
SCREEN_WIDTH = 150
SCREEN_HEIGHT = 150

POINTS_SIZE = 100

POPULATION_SIZE = 30
GENERATION = 5000
MUTATE = 0.3
SELECT_RATE = 0.5


def calc_distance(points, route):
    """経路の距離を計算する

    Parameters
    ----------
    points : list
        都市の位置情報
    route : list
        経路情報（巡回する都市の順番）

    Returns
    -------
    int
        経路の距離
    """
    distance = 0
    for i in range(POINTS_SIZE):
        (x0, y0) = points[route[i]]
        if i == POINTS_SIZE - 1:
            # 最後は始点へ戻る
            (x1, y1) = points[route[0]]
        else:
            (x1, y1) = points[route[i + 1]]
        # 2点間の距離を求める
        distance = distance + math.sqrt(
            (x0 - x1) * (x0 - x1) +
            (y0 - y1) * (y0 - y1)
        )
    return distance


def sort_fitness(points, population):
    """集団を距離で照準にソートする

    Parameters
    ----------
    points : list
        都市の位置情報
    population : list
        集団（経路の集まり）

    Returns
    -------
    list
        ソート済みの集団
    """
    # 適応度と個体をタプルにしてリストに格納する
    fp = []
    for individual in population:
        fitness = calc_distance(points, individual)
        fp.append((fitness, individual))
    fp.sort()

    # ソートした個体を新たな集団に格納する
    sorted_population = []
    for fitness, individual in fp:
        sorted_population.append(individual)

    return sorted_population


def selection(points, population):
    """選択

    適応度の高い（距離が短い）個体を残す

    Parameters
    ----------
    points : list
        都市の位置情報
    population : list
        集団（経路の集まり）

    Returns
    -------
    list
        選択済みの集団
    """
    sorted_population = sort_fitness(points, population)

    n = int(POPULATION_SIZE * SELECT_RATE)
    return sorted_population[:n]


def crossover(ind1, ind2):
    """交叉

    交差点の範囲（r1〜r2）は乱数で決める

    Parameters
    ----------
    ind1, ind2 : list(int)
        親個体

    Returns
    -------
    list(int)
        子個体
    """
    r1 = random.randint(0, POINTS_SIZE - 1)
    r2 = random.randint(r1 + 1, POINTS_SIZE)

    flag = [0] * POINTS_SIZE
    ind = [-1] * POINTS_SIZE

    # r1〜r2をind2から複製
    for i in range(r1, r2):
        city = ind2[i]
        ind[i] = city
        flag[city] = 1

    # r1〜r2以外をind1から複製
    # （まだ使われていない都市のみ）
    for i in list(range(0, r1)) + list(range(r2, POINTS_SIZE)):
        city = ind1[i]
        if flag[city] == 0:
            ind[i] = city
            flag[city] = 1

    # 残った都市
    for i in range(0, POINTS_SIZE):
        if ind[i] == -1:
            for j in range(0, POINTS_SIZE):
                city = ind1[j]
                if flag[city] == 0:
                    ind[i] = city
                    flag[city] = 1
                    break
    return ind


def mutation(ind1):
    """突然変異

    個体の書く遺伝子に対して突然変異確率にしたがって突然変異させる
    ランダムに選んだ都市１と都市２の間を逆順にする
    """
    ind2 = copy.deepcopy(ind1)
    if random.random() < MUTATE:
        city1 = random.randint(0, POINTS_SIZE - 1)
        city2 = random.randint(0, POINTS_SIZE - 1)
        if city1 > city2:
            city1, city2 = city2, city1
        ind2[city1:city2+1] = reversed(ind1[city1:city2+1])
    return ind2


if __name__ == '__main__':
    # ウィンドウ初期化
    root = tkinter.Tk()
    root.title(u'TSPをGAで解いてみる')

    width_size = 5
    height_size = math.ceil(POPULATION_SIZE / width_size)

    window_width = SCREEN_WIDTH * width_size
    window_height = SCREEN_HEIGHT * height_size
    root.geometry(str(window_width) + "x" + str(window_height))

    # Tkinterのキャンバスを集団の数だけ作成する
    canvas_list = []
    for i in range(POPULATION_SIZE):
        canvas = tkinter.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        cx = i % width_size * SCREEN_WIDTH
        cy = int(i / width_size) * SCREEN_HEIGHT
        canvas.place(x=cx, y=cy)
        canvas_list.append(canvas)

    # 都市の座標を乱数で生成する
    points = []
    for i in range(POINTS_SIZE):
        points.append((random.random(), random.random()))

    # 初期集団を乱数で生成する
    population = []
    for i in range(POPULATION_SIZE):
        individual = list(range(POINTS_SIZE))
        random.shuffle(individual)
        population.append(individual)

    # 本処理
    for generation in range(GENERATION):
        root.title(u"TSPをGAで解いてみる（" + str(generation + 1) + u"世代）")

        # 選択
        population = selection(points, population)

        # 交叉と突然変異
        n = POPULATION_SIZE - len(population)
        for i in range(n):
            # 集団から２個体をランダムで選び、交叉した個体を生成する
            r1 = random.randint(0, len(population) - 1)
            r2 = random.randint(0, len(population) - 1)
            individual = crossover(population[r1], population[r2])

            # 突然変異
            individual = mutation(individual)

            population.append(individual)

        # ソート
        sort_fitness(points, population)

        if generation % 100:
            continue

        # 都市の経路を描画する
        for ind in range(POPULATION_SIZE):
            canvas = canvas_list[ind]
            route = population[ind]
            dist = calc_distance(points, route)
            canvas.delete('all')
            for i in range(POINTS_SIZE):
                (x0, y0) = points[route[i]]
                if i == POINTS_SIZE - 1:
                    # 最後は始点に戻る
                    (x1, y1) = points[route[0]]
                else:
                    (x1, y1) = points[route[i + 1]]
                # 経路の線を描画する
                canvas.create_line(
                    x0 * SCREEN_WIDTH,
                    y0 * SCREEN_HEIGHT,
                    x1 * SCREEN_WIDTH,
                    y1 * SCREEN_HEIGHT,
                    fill="black", width=1
                )
                # 都市を描画する
                canvas.create_oval(
                    x0 * SCREEN_WIDTH - 2,
                    y0 * SCREEN_HEIGHT - 2,
                    x0 * SCREEN_WIDTH + 2,
                    y0 * SCREEN_HEIGHT + 2,
                    fill="blue"
                )
            # 枠を描画する
            canvas.create_rectangle(
                0, 0, SCREEN_WIDTH - 1, SCREEN_HEIGHT - 1,
                outline="gray", width=1
            )
            # 距離を描画する
            canvas.create_text(
                5, 5,
                text="{:.2f}".format(dist),
                anchor="nw", fill="red"
            )
            canvas.update()

    root.mainloop()
