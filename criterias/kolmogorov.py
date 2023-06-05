import pandas as pd
import numpy as np
import scipy.stats as sps
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Kolm():
    def __init__(self, data=[], n = 0, alpha = 0.01 ) -> None:
        self.alpha = alpha
        self.f_obs = data
        self.x_i = list(range(len(self.f_obs)))
   
        self.size = sum(self.f_obs)

        self.data = pd.DataFrame({
                "Xi": self.x_i,
                "Ni": self.f_obs }, index=None)
        self.data = self.data.T

        self.rel_obs = list(map(lambda n : n/self.size, self.f_obs))
        self.acumulate_obs = [sum(self.rel_obs[:i + 1]) for i in range(len(self.rel_obs))]

        self.f_exp = [self.size/len(self.f_obs) for i in range(len(self.f_obs))]
        self.rel_exp = [1/len(self.f_obs)]*len(self.f_obs)
        self.acumulate_exp = [sum(self.rel_exp[:i + 1]) for i in range(len(self.rel_exp))]

        self.x_i.append(len(self.x_i))
        self.acumulate_exp.insert(0,0)
        self.acumulate_obs.insert(0,0)

        self.df_ks = pd.DataFrame({
                "Income" : self.x_i,
                "F_control": self.acumulate_exp,
                "F_treatment":  self.acumulate_obs}, index=None)

        self.k = np.argmax( np.abs(self.df_ks['F_control'] - self.df_ks['F_treatment']))
        self.ks_stat = np.abs(self.df_ks['F_treatment'][self.k] - self.df_ks['F_control'][self.k])
        print("Выборка : ", self.data)
        print("Аккумулятивные частоты эмп. :", self.acumulate_obs)
        print("Аккумулятивные частоты теор. :", self.acumulate_exp)
        print("D_n = ", self.ks_stat)

        self.y = (self.df_ks['F_treatment'][self.k] + self.df_ks['F_control'][self.k])/2
        
        self.critical_value = (sps.kstwobign.ppf(1 - self.alpha))/(self.size**(1/2))
        print("Критическое значение : ", self.critical_value)
        if (self.ks_stat < self.critical_value):
            print("Нет оснований отвергнуть проверяемую гипотезу")
        else:
            print("Отвергаем гипотезу")
        

class PlotKolm(FigureCanvas):
    def __init__(self, data,  parent=None):
        
        
        fig, self.ax = plt.subplots(figsize=(6, 5), dpi=100)
        self.ax.tick_params(axis='both', which='major', labelsize=12)
        super().__init__(fig)
        self.setParent(parent)

        """ 
        Matplotlib Script
        """
        
        self.ax.plot('Income', 'F_control', data=data.df_ks, label='Теоретическая')
        self.ax.plot('Income', 'F_treatment', data=data.df_ks, label='Эмпирическая')
        self.ax.errorbar(x=data.df_ks['Income'][data.k], y=data.y, yerr=data.ks_stat/2, color='k',
                        capsize=2, mew=3, label=f"Статистическая разница: {data.ks_stat:.4f}")
        self.ax.legend(loc='upper left', fontsize=12)
        self.ax.set_title("Критерий Колмогорова", fontsize=12)
        
        self.ax.grid()

if __name__=="__main__":
   # a = Kolm([2048,1992])
    pass