from copy import copy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton


class ViewController:
    """
    キー・マウス入力によって、matplotlibの図を拡大縮小・範囲の移動をするクラス

    マウスホイール：                上下移動
    shift + マウスホイール：        左右移動
    ctrl + マウスホイール：         y軸の拡大縮小
    ctrl+shift + マウスホイール：   x軸の拡大縮小
    右クリック：                    拡大縮小のリセット
    ctrl + 右クリック：                    //       y軸のみ
    ctrl+shift + 右クリック：              //       x軸のみ
    """

    def __init__(self, fig, ax):
        """
        変数の初期化とイベントと関数の紐づけ

        Args:
            fig (_type_): matplotlibのfig
            ax (_type_): matplotlibのax
        """
        self.index = 0
        self.fig = fig
        self.ax = ax

        # 描画範囲取得
        self.xmin_ini, self.xmax_ini = self.xmin, self.xmax = self.ax.get_xlim()
        self.ymin_ini, self.ymax_ini = self.ymin, self.ymax = self.ax.get_ylim()

        # key state
        self.shift_key = False
        self.ctrl_key = False

        # イベントと関数の紐づけ
        fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        fig.canvas.mpl_connect('button_press_event',
                               self.on_button_press)
        fig.canvas.mpl_connect('button_release_event',
                               self.on_button_release)
        fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        fig.canvas.mpl_connect('key_release_event', self.on_key_release)
        self.update()

    def on_scroll(self, event):
        """
        マウスホイールの入力を処理する。
        奥に向かって回すと1
        手前に向かって回すと-1

        Args:
            event (_type_): _description_
        """
        print(event.button, event.step)
        increment = 1 if event.button == 'up' else -1

        print(f"shift_key: {self.shift_key}    ctrl_key:{self.ctrl_key}")
        self.update(increment)

    def on_button_press(self, event):
        """
        マウスの左クリックが話されたとき、その時点での描画範囲を取得する

        Args:
            event (_type_): _description_
        """
        if event.button is MouseButton.RIGHT:
            if not (not self.shift_key and self.ctrl_key):
                self.xmin, self.xmax = copy(self.xmin_ini), copy(self.xmax_ini)
            if not (self.shift_key and self.ctrl_key):
                self.ymin, self.ymax = copy(self.ymin_ini), copy(self.ymax_ini)

            print(f"xlim: {[self.xmin, self.xmax]}",
                  f"ylim: {[self.ymin, self.ymax]}")
        self.update()

    def on_button_release(self, event):
        """
        マウスの左クリックが話されたとき、その時点での描画範囲を取得する

        Args:
            event (_type_): _description_
        """
        if event.button is MouseButton.LEFT:
            self.xmin, self.xmax = self.ax.get_xlim()
            self.ymin, self.ymax = self.ax.get_ylim()
            print(f"xlim: {[self.xmin, self.xmax]}",
                  f"ylim: {[self.ymin, self.ymax]}")

    def on_key_press(self, event):
        """
        キーが押されると、キー状態変数をTrueにする

        Args:
            event (_type_): _description_
        """
        print('press', event.key)
        if 'shift' in event.key:
            self.shift_key = True
        if "control" in event.key:
            self.ctrl_key = True

    def on_key_release(self, event):
        """
        キーが離されると、キー状態変数をFalseにする

        Args:
            event (_type_): _description_
        """
        print('release', event.key)
        if 'shift' in event.key:
            self.shift_key = False
        if 'control' in event.key:
            self.ctrl_key = False

    def zoom(self, magnification: float, target: str = 'xy'):
        """
        描画範囲の拡大縮小

        Args:
            magnification (float): 拡大倍率
        """
        reciprocal_mag = 1/magnification
        xlim_range = self.xmax - self.xmin
        ylim_range = self.ymax - self.ymin

        new_xlim_range = xlim_range * abs(reciprocal_mag)
        new_ylim_range = ylim_range * abs(reciprocal_mag)
        dx = (xlim_range - new_xlim_range)/2
        dy = (ylim_range - new_ylim_range)/2

        if magnification < 0:
            dx = -dx
            dy = -dy
        if 'x' in target:
            self.xmin += dx
            self.xmax -= dx
        if 'y' in target:
            self.ymin += dy
            self.ymax -= dy

    def x_shift(self, direction: int, tick: float = 0.1):
        """
        現在の描画範囲のtick分だけ上下方向に移動する

        Args:
            direction (int): 移動する方向を1,-1で指定する。1で上に移動。-1で下に移動
            tick (float): 例えば、描画範囲が-10~10でtick=0.1の場合、+-2ずつ移動する
        """
        xlim_range = self.xmax - self.xmin
        dx = xlim_range*tick*direction

        self.xmin -= dx
        self.xmax -= dx

    def y_shift(self, direction: int, tick: float = 0.1):
        """
        現在の描画範囲のtick分だけ上下方向に移動する

        Args:
            direction (int): 移動する方向を1,-1で指定する。1で上に移動。-1で下に移動
            tick (float): 例えば、描画範囲が-10~10でtick=0.1の場合、+-2ずつ移動する
        """
        ylim_range = self.ymax - self.ymin
        dy = ylim_range*tick*direction

        self.ymin += dy
        self.ymax += dy

    def update(self, scroll=0):
        self.ax.set_title(
            f'Use scroll wheel to navigate\nindex {self.index}')

        # 描画範囲変更
        if self.ctrl_key and self.shift_key:
            self.zoom(1.1**scroll, target='x')
        elif self.ctrl_key:
            self.zoom(1.1**scroll, target='y')
        elif self.shift_key:
            self.x_shift(scroll)
        else:
            self.y_shift(scroll)
        self.ax.set_xlim(self.xmin, self.xmax)
        self.ax.set_ylim(self.ymin, self.ymax)

        self.ax.set_aspect('auto')
        self.fig.canvas.draw()
