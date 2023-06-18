from concurrent.futures import ThreadPoolExecutor
import time
from copy import copy

import matplotlib.pyplot as plt
import numpy as np

from util.line_drawer import LineDrawer
from util.view_controller import ViewController

def plot_show(x,y,data,editting):
    fig, ax = plt.subplots()
    ax.plot(x, y, marker='.')
    vc = ViewController(fig,ax)
    ld = LineDrawer(fig, ax, data)

    before = copy(data)
    plt.show()
    editting[0] = False


def read_data(data,editting):
    while editting[0]:
        time.sleep(1)
        print(data)


if __name__ == '__main__':
    x = np.arange(2*np.pi*5)/5
    y = np.sin(x)
    data = copy(y)
    editting = [True]
    with ThreadPoolExecutor() as executor:
        executor.submit(plot_show,x,y,data,editting)
        executor.submit(read_data, data, editting)
    print('終了')