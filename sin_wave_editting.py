import matplotlib.pyplot as plt
import numpy as np

from util.view_controller import ViewController

class PlotPicker:

    def __init__(self, fig, ax):
        self.fig = fig
        self.ax = ax
        self.before_mouse_xdata = None
        self.before_mouse_ydata = None

        for line in self.ax.lines:
            line.set_picker(self.dummy_picker)
        fig.canvas.mpl_connect('motion_notify_event', self.motion)

    def motion(self, event):
        if event.xdata is None:
            self.before_mouse_xdata = None
            self.before_mouse_ydata = None
            return
        if event.button == 1:
            xdata = self.ax.lines[0].get_xdata()
            ydata = self.ax.lines[0].get_ydata()
            
            idx = np.argmin(np.abs(xdata - event.xdata))
            
            # 線形補間
            if self.before_mouse_xdata is not None:
                b_idx = np.argmin(np.abs(xdata - self.before_mouse_xdata))
                n_step = abs(idx - b_idx)
                
                if n_step != 0:
                    diff = event.ydata -self.before_mouse_ydata
                    step_d = diff/n_step
                    
                    if b_idx < idx:
                        for n, idx in enumerate(range(b_idx,idx+1)):
                            ydata[idx] = self.before_mouse_ydata + step_d*n
                    else:
                        for n, idx in enumerate(reversed(range(idx,b_idx+1))):
                            ydata[idx] = self.before_mouse_ydata + step_d*n
            else:
                ydata[idx] = event.ydata
                
            self.ax.lines[0].set_ydata(ydata)
            
        self.before_mouse_xdata = event.xdata
        self.before_mouse_ydata = event.ydata
        self.fig.canvas.draw()

    def dummy_picker(self, artist, mouseevent):
        """
        何もしないダミー
        """
        return False, dict()


fig, ax = plt.subplots()
ax.set_title('custom picker for line data')
x = np.arange(2*np.pi*5)/5
y = np.sin(x)

ax.plot(x, y, marker='.')
vc = ViewController(fig, ax)
pp = PlotPicker(fig, ax)

print(ax.lines[0].get_ydata())
plt.show()
print(ax.lines[0].get_ydata())