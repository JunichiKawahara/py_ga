#! /usr/local/bin/python3

import sys
import random
import math
import copy
import tkinter

"""
巡回セールスマン問題を乱数だけで解いてみる
日経ソフトウェア2019年3月号 「Pythonで遺伝的アルゴリズムのプログラムを作る」
Copyright (C) 2019 J.Kawahara
2019.3.14 J.Kawahara 新規作成
"""

# パラメータ
SCREEN_WIDTH = 360
SCREEN_HEIGHT = 360

POINTS_SIZE = 50
LOOP = 100000


def calc_distance(points, route):
    """経路の距離を計算する

    Parameters
    ----------
    points : list
        巡回すべき都市の座標のリスト
    route : list
        都市を巡回する順番

    Returns
    -------
    int
        経路の距離の合計値
    """
    distance = 0
    for i in range(POINTS_SIZE):
        (x0, y0) = points[route[i]]
        if i == POINTS_SIZE - 1:
            # 最後は始点へ戻る
            (x1, y1) = points[route[0]]
        else:
            (x1, y1) = points[route[i+1]]

        distance = distance + math.sqrt(
            (x0 - x1) * (x0 - x1) +
            (y0 - y1) * (y0 - y1))

    return distance


if __name__ == '__main__':
    root = tkinter.Tk()
    root.title(u"TSPを乱数だけで解いてみる")
    root.geometry(
        str(SCREEN_WIDTH) + "x" +
        str(SCREEN_HEIGHT))

    # キャンバスを作成する
    canvas = tkinter.Canvas(
        root,
        width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    canvas.place(x=0, y=0)

    # 都市の座標を作成する
    points = []
    for i in range(POINTS_SIZE):
        points.append((random.random(), random.random()))

    # 都市を一巡する経路を作成する
    route = list(range(POINTS_SIZE))

    min_route = copy.copy(route)
    min_dist = calc_distance(points, route)

    for c in range(LOOP):
        root.title(
            u"TSPを乱数だけで解いてみる（" +
            str(c + 1) + u"回）")

        # 経路をランダムに入れ替える
        random.shuffle(route)

        dist = calc_distance(points, route)

        if min_dist > dist:
            min_route = copy.copy(route)
            min_dist = dist

            # 都市の経路を描画する
            canvas.delete('all')
            for i in range(POINTS_SIZE):
                (x0, y0) = points[route[i]]
                if i == POINTS_SIZE - 1:
                    # 最後は視点に戻る
                    (x1, y1) = points[route[0]]
                else:
                    (x1, y1) = points[route[i+1]]

                # 経路の線を描画
                canvas.create_line(
                    x0 * SCREEN_WIDTH,
                    y0 * SCREEN_HEIGHT,
                    x1 * SCREEN_WIDTH,
                    y1 * SCREEN_HEIGHT,
                    fill="black", width=1)

                # 都市を描画する
                canvas.create_oval(
                    x0 * SCREEN_WIDTH - 3,
                    y0 * SCREEN_HEIGHT - 3,
                    x0 * SCREEN_WIDTH + 3,
                    y0 * SCREEN_HEIGHT + 3,
                    fill="blue"
                )

            # 距離を描画する
            canvas.create_text(
                5, 5,
                text="{:.2f}".format(min_dist),
                anchor="nw", fill="red")

            canvas.update()

    root.mainloop()
