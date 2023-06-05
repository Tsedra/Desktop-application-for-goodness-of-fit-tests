
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class Permutation():
    def __init__(self, f_obs, f_exp, alpha=0.01) -> None:
        self.alpha = alpha
        n_permutations = 10000
        xy = np.concatenate([f_obs, f_exp])
        self.obs_diff = np.mean(f_obs) - np.mean(f_exp)
        self.perm_diffs = np.zeros(n_permutations)
        for i in range(n_permutations):
            permuted_xy = np.random.permutation(xy)
            permuted_x = permuted_xy[:len(f_obs)]
            permuted_y = permuted_xy[len(f_obs):]
            self.perm_diff = np.mean(permuted_x) - np.mean(permuted_y)
            self.perm_diffs[i] = self.perm_diff
        self.p_value = (np.abs(self.perm_diffs) >= np.abs(self.obs_diff)).mean()
        print(self.p_value)

class PlotPerm(FigureCanvas):
    def __init__(self, data,  parent=None):
        
        
        fig, self.ax = plt.subplots(figsize=(6, 5), dpi=100)
        self.ax.tick_params(axis='both', which='major', labelsize=12)
        super().__init__(fig)
        self.setParent(parent)

        """ 
        Matplotlib Script
        """
        self.ax.hist(data.perm_diffs, bins=50, density=True, color='gray', alpha=0.5)
        self.ax.axvline(x=data.obs_diff, color='red', linestyle='--', linewidth=2, label='Наблюдаемая разница')
        self.ax.axvline(x=-data.obs_diff, color='red', linestyle='--', linewidth=2)
        self.ax.set_title('Распределение разницы между средними значениями в пермутированных выборках', fontsize=12)
        self.ax.set_xlabel('Разница между средними значениями', fontsize=12)
        self.ax.set_ylabel('Плотность вероятности', fontsize=12)
        self.ax.legend()
        self.ax.grid()
        
 
if __name__=="__main__":
    pass