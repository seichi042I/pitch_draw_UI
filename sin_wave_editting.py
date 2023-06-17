import matplotlib.pyplot as plt
import numpy as np
from numpy.random import rand

from util.view_controller import ViewController
# クリックした自転でのマウスカーソルの位置から半径maxdいないのプロット点の座標を取得する
# propsにはeventの属性を定義する辞書を指定する
# この場合はind, pickx, pickyという属性にデータ番号、データx座標、データy座標を指定している


class PlotPicker:

    def __init__(self, fig, ax):
        self.fig = fig
        self.ax = ax
        self.idxs = None

        for line in self.ax.lines:
            line.set_picker(self.line_picker)
        fig.canvas.mpl_connect('pick_event', self.onpick2)
        fig.canvas.mpl_connect('motion_notify_event', self.motion)

    def motion(self, event):
        if event.button == 1 and self.idxs:
            ydata = self.ax.lines[0].get_ydata()
            ydata[self.idxs[0]] = event.ydata
            self.ax.lines[0].set_ydata(ydata)
        # gco.set_data(x, y)
        plt.draw()

    def onpick2(self, event):
        print('onpick2 line:', event.pickx, event.picky)
        self.idxs = event.ind

    def line_picker(self, artist, mouseevent):
        """
        Find the points within a certain distance from the mouseclick in
        data coords and attach some extra attributes, pickx and picky
        which are the data points that were picked.
        """
        if mouseevent.xdata is None:
            return False, dict()
        xdata = artist.get_xdata()
        ydata = artist.get_ydata()
        maxd = 0.05
        d = np.sqrt(
            (xdata - mouseevent.xdata)**2 + (ydata - mouseevent.ydata)**2)

        ind, = np.nonzero(d <= maxd)
        if len(ind):
            pickx = xdata[ind]
            picky = ydata[ind]
            props = dict(ind=ind, pickx=pickx, picky=picky)
            return True, props
        else:
            return False, dict()


fig, ax = plt.subplots()
ax.set_title('custom picker for line data')
x = np.arange(2*np.pi*10)/10
y = np.sin(x)

ax.plot(x, y, marker='o')
vc = ViewController(fig, ax)
pp = PlotPicker(fig, ax)

plt.show()
