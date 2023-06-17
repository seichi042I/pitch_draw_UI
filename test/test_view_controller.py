import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from ..util.view_controller import ViewController


def test_view_controller():
    fig, ax = plt.subplots()

    x = np.arange(2*np.pi*25)/25
    y = np.sin(x)
    ax.plot(y, marker='o')

    vs = ViewController(fig, ax)

    plt.show()
