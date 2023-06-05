from scipy.stats import ttest_ind, t
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Ttest():
    def __init__(self, data_a, data_b, alpha=0.01) -> None:
        self.alpha = alpha
        self.dataA = data_a
        self.dataB = data_b
        self.t_stat, self.p_value = ttest_ind(self.dataA, self.dataB)
        print(self.t_stat)
        
class PlotTtest(FigureCanvas):
    def __init__(self, data,  parent=None):
        
        
        fig, self.ax = plt.subplots(figsize=(6, 5), dpi=100)
        self.ax.tick_params(axis='both', which='major', labelsize=12)
        super().__init__(fig)
        self.setParent(parent)
        """ 
        Matplotlib Script
        """
        fig.set_facecolor('#e1f0e4')
        
        self.ax.tick_params(axis='both', which='major', labelsize=12)
        self.ax.scatter(np.arange(len(data.dataA)), data.dataA, label='Группа №1')
        self.ax.scatter(np.arange(len(data.dataB)), data.dataB, label='Группа №2')
        self.ax.legend(fontsize=12)
        
        self.ax.set_title(f"t-статистика: {data.t_stat:.5f}, p-значение: {data.p_value:.5f}", fontsize=12)
        plt.grid()
 
if __name__ =="__main__":
    pass
