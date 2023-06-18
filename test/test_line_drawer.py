from copy import copy

import matplotlib.pyplot as plt
import numpy as np

from ..util.line_drawer import LineDrawer

def test_line_drawer():
    fig, ax = plt.subplots()
    x = np.arange(2*np.pi*5)/5
    y = np.sin(x)

    ax.plot(x, y, marker='.')
    data = y
    ld = LineDrawer(fig, ax,data)

    before = copy(data)
    plt.show()
    after = copy(data)
    
    # プロットが書き換えられているか
    assert not all(before == after)