from copy import copy

import matplotlib.pyplot as plt
import numpy as np

from ..util.line_drawer import LineDrawer

def test_line_drawer():
    fig, ax = plt.subplots()
    ax.set_title('custom picker for line data')
    x = np.arange(2*np.pi*5)/5
    y = np.sin(x)

    ax.plot(x, y, marker='.')
    LineDrawer(fig, ax)

    before = copy(ax.lines[0].get_ydata())
    plt.show()
    after = copy(ax.lines[0].get_ydata())
    
    # プロットが書き換えられているか
    assert not all(before == after)