import numpy as np
import matplotlib.pyplot as plt


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
        print(event.button, event.step)
        increment = 1 if event.button == 'up' else -1
        max_index = self.X.shape[-1] - 1
        self.index = np.clip(self.index + increment, 0, max_index)

        print(f"shift_key: {self.shift_key}    ctrl_key:{self.ctrl_key}")
        self.update(increment)

    def on_press(self, event):
        print('press', event.key)
        if event.key == 'shift':
            self.shift_key = True
        if event.key == "control":
            self.ctrl_key = True

    def on_release(self, event):
        print('release', event.key)
        if event.key == 'shift':
            self.shift_key = False
        if event.key == "control":
            self.ctrl_key = False

    def update(self, increment=0):
        self.im.set_data(self.X[:, :, self.index])
        self.ax.set_title(
            f'Use scroll wheel to navigate\nindex {self.index}')

        # 描画範囲変更
        self.xmin += increment
        self.xmax -= increment
        self.ymin -= increment
        self.ymax += increment
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
fig.canvas.mpl_connect('key_press_event', tracker.on_press)
fig.canvas.mpl_connect('key_release_event', tracker.on_release)
plt.show()
