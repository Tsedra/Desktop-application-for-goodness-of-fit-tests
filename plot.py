import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib as mpl

class Canvas(FigureCanvas):
    def __init__(self, parent=None):
        
        #mpl.rcParams.update({'fontsize': 10})
        fig, self.ax = plt.subplots(figsize=(6, 5),dpi=100)
        self.ax.tick_params(axis='both', which='major', labelsize=12)
        super().__init__(fig)
        self.setParent(parent)

        """ 
        Matplotlib Script
        """
        
        t = np.arange(0.0, 2.0, 0.01)
        s = 1 + np.sin(2 * np.pi * t)
        
        self.ax.plot(t, s)

        self.ax.set_title("График", fontsize=16, fontname='Arial')
        self.ax.grid()