import pandas as pd
import math
from scipy.stats import chi2
import numpy as np
import scipy.stats as sps
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

red = '#FF3300'
blue = '#0099CC'
green = '#00CC66'

sns.set(style='ticks', font_scale=1.7)

class Interval():
    def __init__(self, l, r) -> None:
        self.left = l
        self.right = r
        self.avg = (l + r)/2
    
    def __str__(self) -> str:
        return "[ "+str(self.left)+", " + str(self.right)+")"
        
class TableForX2():
    def __init__(self, data=[], inter=[], n = 0, alpha = 0.01 ) -> None:
        self.size = n
        self.intervals = inter
        self.f_obs = data
        self.alpha = alpha
        

        if(data == []):
            for i in range(n):
                print(" Interval number " + str(i+1))
                self.intervals.append(Interval(float(input(" left : ")), float(input(" right : "))))
                self.f_obs.append(int(input(" The count of observations : ")))

        self.Emean = sum(map(lambda i, o : i.avg*o, self.intervals, self.f_obs))/sum(self.f_obs)# drop round
        self.dispersion =sum(map(lambda i, o : ((i.avg)**2)*o, self.intervals, self.f_obs))/sum(self.f_obs)-(self.Emean**2)#drop
        self.sqrtDispersion = math.sqrt(self.dispersion)
        self.h = math.fabs(self.intervals[0].right - self.intervals[0].left)


        self.lim = {"low" : self.intervals[0].left, "high" : self.intervals[-1].right}
        self.bins_ranges = list(map(lambda i : i.avg, self.intervals))
        #self.intervals[0].left = -math.inf
        #self.intervals[-1].right = math.inf

        #l = list(map(lambda i : math.fabs(integrate.quad(integralF, 0, math.fabs( (i.left - self.Emean)/self.sqrtDispersion ))[0]), self.intervals))
        #r = list(map(lambda i : math.fabs(integrate.quad(integralF, 0, math.fabs((i.right - self.Emean)/self.sqrtDispersion ))[0]), self.intervals))

                
        self.lent = sum(self.f_obs)
        self.f_exp = list(map(lambda inter: self.lent*self.h*sps.norm.pdf((inter.avg-self.Emean)/self.sqrtDispersion)/self.sqrtDispersion, self.intervals))


        self.f_obs_new = self.greater5(self.greater5(self.f_obs)[::-1])[::-1]
        self.f_exp_new = self.greater5(self.greater5(self.f_exp)[::-1])[::-1]
                       
        self.dof = len(self.f_obs_new) - 3 if (len(self.f_obs_new) - 3 ) > 1 else 1
  
        
        self.chi_2 =sum(list(map(lambda obs, value_f : ((obs-value_f)**2)/value_f, self.f_obs_new, self.f_exp_new)))

        self.X2_table = chi2.ppf((1-self.alpha), self.dof)

        if(self.chi_2 < self.X2_table):
            print(" Нет оснований отвергнуть проверяемую гипотезу ")
        else:
            print(" Отвергаем проверяемую гипотезу")

    def __str__(self) -> str:
        self.data = pd.DataFrame({
                "[Xi, Xi+1)": [str (i) for i in self.intervals],
                "Ni": self.f_obs }, index=None)
        self.data = self.data.T
        s = self.data.to_string(header=False)
        return s

    def greater5(self, f_obs):
        f_obs_new = [0 for i in range(len(f_obs))]
        j, s = 0, 0 
        for i in range(len(f_obs)  ):
            s += f_obs[i]
            if (i == len(f_obs) - 1) : break
            elif(s < 5): continue

            f_obs_new[j] = s
            j += 1
            s = 0
        f_obs_new[j] = s
        
        return (list(filter(lambda f: f!=0, f_obs_new)))
    def plot(self):
    
        plt.figure(figsize=(6, 5))
        plt.plot(self.bins_ranges, self.f_obs , lw=2, color=blue, label='Плотность')

        plt.bar(self.bins_ranges, self.f_exp, color='green', label='Приближение',bottom=5, edgecolor ="black")
     
        plt.title('Точность приближения в критерии хи-квадрат')
        plt.show()

        
class PlotChi2(FigureCanvas):
    def __init__(self, data,  parent=None):
        
        fig, self.ax = plt.subplots(figsize=(6, 5), dpi=100)
        self.ax.tick_params(axis='both', which='major', labelsize=12)
        super().__init__(fig)
        self.setParent(parent)
        """ 
        Matplotlib Script
        """
        self.ax.plot(data.bins_ranges, data.f_obs , lw=2, color=blue, label='Плотность')
        self.ax.bar(data.bins_ranges, data.f_exp, color='green', label='Приближение', bottom=5, edgecolor ="black")
        self.ax.set_title('Точность приближения в критерии хи-квадрат', fontsize=12)
        self.ax.grid()

def integralF(x):
            return (1/math.sqrt(2*math.pi))*(math.exp(-(x**2)/2))
class kolm():
    def __init__(self) -> None:
        self.f_obs = [1992,2048]
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
        

        df_ks = pd.DataFrame({
                "Income" : self.x_i,
                "F_control": self.acumulate_exp,
                "F_treatment":  self.acumulate_obs}, index=None)
   
        print(df_ks.head())

        k = np.argmax( np.abs(df_ks['F_control'] - df_ks['F_treatment']))
        ks_stat = np.abs(df_ks['F_treatment'][k] - df_ks['F_control'][k])

        print(k)
        print(ks_stat)

        y = (df_ks['F_treatment'][k] + df_ks['F_control'][k])/2

        plt.plot('Income', 'F_control', data=df_ks, label='Control')
        plt.plot('Income', 'F_treatment', data=df_ks, label='Treatment')
        plt.errorbar(x=df_ks['Income'][k], y=y, yerr=ks_stat/2, color='k',
            capsize=2, mew=3, label=f"Test statistic: {ks_stat:.4f}")
        plt.legend(loc='upper left', fontsize=10)
        plt.title("Kolmogorov-Smirnov Test")
        plt.show()
        rng = np.random.default_rng()
        self.f_obs = sps.laplace.rvs(size=2)
        print(self.f_obs[:5])
        self.f_obs = [1992/4040,2048/4040]
        stat, p_value = sps.kstest(self.f_obs, 'norm', alternative="less", method="exact")
        print(f" Kolmogorov-Smirnov Test: statistic={stat:.4f}, p-value={p_value:.4f}")




if __name__ == "__main__":
    pass
    """
    table = TableForX2(n=5, alpha = 0.05)
    print(table)
    print(table.lent)
    print(table.Emean)
    print(table.dispersion)
    print(table.f_exp_new)
    print(f" хи квадрат : {table.chi_2}")
    print(f" хи квадрат таблица : {table.X2_table}")
    #table.plot()
    #kol = kolm()
    """





    
