import numpy as np
from scipy.stats import norm, anderson
import scipy
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
class Anderson():
    def __init__(self, data, alpha=0.01) -> None:
        
        self.data = data
        self.alpha = alpha
        # Оцениваем среднее и стандартное отклонение
        self.mu, self.std = np.mean(data), np.std(data)

        # Вычисляем значение статистики критерия Андерсона-Дарлинга
        self.result = scipy.stats.anderson(data, dist='norm')
        self.statistic = self.result.statistic
        criticals = self.result.critical_values
        if (0 < self.alpha <= 0.01):
            self.critical_value = criticals[4]
        elif(0.01 < self.alpha <= 0.025):
            self.critical_value = criticals[3]
        elif(0.025 < self.alpha <=0.05):
            self.critical_value = criticals[2]
        elif(0.05 < self.alpha <= 0.1):
            self.critical_value = criticals[1]
        else:
            self.critical_value = criticals[0]




class PlotAnderson(FigureCanvas):
    def __init__(self, data,  parent=None):
        
        
        fig, self.ax = plt.subplots(figsize=(6, 5), dpi=100)
        self.ax.tick_params(axis='both', which='major', labelsize=12)
        super().__init__(fig)
        self.setParent(parent)
        """ 
        Matplotlib Script
        """
        # Строим гистограмму выборки
        self.ax.hist(data.data, density=True, alpha=0.5)

        # Строим график нормального распределения
        x = np.linspace(min(data.data), max(data.data), 100)
        self.ax.plot(x, norm.pdf(x, data.mu, data.std))

        # Добавляем подписи осей и заголовок
        self.ax.set_xlabel('Значения выборки', fontsize=12)
        self.ax.set_ylabel('Плотность вероятности',fontsize=12)
        self.ax.set_title('Тест на нормальность',fontsize=12)

        # Выводим значение статистики критерия Андерсона-Дарлинга
        #plt.text(13, 0.18, 'Статистика = {:.3f}'.format(statistic))

        self.ax.grid()
 
if __name__ =="__main__":
    pass