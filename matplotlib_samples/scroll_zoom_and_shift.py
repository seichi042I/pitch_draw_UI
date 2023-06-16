import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton


class IndexTracker:
    def __init__(self, ax, X):
        self.index = 0
        self.X = X
        self.ax = ax
        self.im = ax.imshow(self.X[:, :, self.index])

        # 描画範囲取得
        self.xmin, self.xmax = self.ax.get_xlim()
        self.ymin, self.ymax = self.ax.get_ylim()

        # key state
        self.shift_key = False
        self.ctrl_key = False
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

    def on_button_release(self, event):
        """
        マウスの左クリックが話されたとき、その時点での描画範囲を取得する

        Args:
            event (_type_): _description_
        """
        if event.button is MouseButton.LEFT:
            self.xmin, self.xmax = self.ax.get_xlim()
            self.ymin, self.ymax = self.ax.get_ylim()
            print(f'get ax xy lims:{self.xmin,self.xmax,self.ymin,self.ymax}')

    def on_key_press(self, event):
        """
        キーが押されると、キー状態変数をTrueにする

        Args:
            event (_type_): _description_
        """
        print('press', event.key)
        if event.key == 'shift':
            self.shift_key = True
        if event.key == "control":
            self.ctrl_key = True

    def on_key_release(self, event):
        """
        キーが離されると、キー状態変数をFalseにする

        Args:
            event (_type_): _description_
        """
        print('release', event.key)
        if event.key == 'shift':
            self.shift_key = False
        if event.key == "control":
            self.ctrl_key = False

    def zoom(self, magnification: float):
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

        self.xmin += dx
        self.xmax -= dx
        self.ymin += dy
        self.ymax -= dy

    def y_shift(self, direction: int, tick: float = 0.1):
        """
        現在の描画範囲のtick分だけ上下方向に移動する

        Args:
            direction (int): 移動する方向を1,-1で指定する。1で上に移動。-1で下に移動
            tick (float): 例えば、描画範囲が-10~10でtick=0.1の場合、+-2ずつ移動する
        """
        ylim_range = self.ymax - self.ymin
        dy = abs(ylim_range)*tick*direction

        self.ymin -= dy
        self.ymax -= dy

    def update(self, scroll=0):
        self.im.set_data(self.X[:, :, self.index])
        self.ax.set_title(
            f'Use scroll wheel to navigate\nindex {self.index}')

        # 描画範囲変更
        if self.ctrl_key:
            self.zoom(1.1**scroll)
        # elif self.shift_key:
        #     x_shift()
        else:
            self.y_shift(scroll)
        self.ax.set_xlim(self.xmin, self.xmax)
        self.ax.set_ylim(self.ymin, self.ymax)
        print(f"xlim: {[self.xmin, self.xmax]}",
              f"ylim: {[self.ymin, self.ymax]}")

        self.im.axes.figure.canvas.draw()


x, y, z = np.ogrid[-10:10:100j, -10:10:100j, 1:10:20j]
X = np.sin(x * y * z) / (x * y * z)

fig, ax = plt.subplots()
# create an IndexTracker and make sure it lives during the whole
# lifetime of the figure by assigning it to a variable
tracker = IndexTracker(ax, X)

fig.canvas.mpl_connect('scroll_event', tracker.on_scroll)
fig.canvas.mpl_connect('button_release_event', tracker.on_button_release)
fig.canvas.mpl_connect('key_press_event', tracker.on_key_press)
fig.canvas.mpl_connect('key_release_event', tracker.on_key_release)
plt.show()
