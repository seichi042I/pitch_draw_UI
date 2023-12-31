import matplotlib.pyplot as plt
import numpy as np

class LineDrawer:
    """
    マウスのxデータ座用に一番近いプロットをマウスのy座標に変更する
    """
    def __init__(self, fig, ax, ydata:np.ndarray):
        self.fig = fig
        self.ax = ax
        self.ydata = ydata
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
            
            ydata[idx] = event.ydata
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

                
            self.ax.lines[0].set_ydata(ydata)
            
        self.before_mouse_xdata = event.xdata
        self.before_mouse_ydata = event.ydata
        self.fig.canvas.draw()
        self.ydata[:] = self.ax.lines[0].get_ydata()

    def dummy_picker(self, artist, mouseevent):
        """
        何もしないダミー
        """
        return False, dict()