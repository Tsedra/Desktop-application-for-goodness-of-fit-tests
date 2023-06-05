import sys
from PyQt5.QtWidgets import QMainWindow, QToolTip, QAction, QWidget, \
    QPushButton, QGridLayout, QSpinBox, QDoubleSpinBox, QTableView, QHBoxLayout, QApplication, QLabel
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap, QStandardItemModel, QStandardItem
from criterias.chi2kol import  TableForX2, PlotChi2
from check import DataCheck
from criterias.kolmogorov import Kolm, PlotKolm
from criterias.perm import Permutation, PlotPerm
from criterias.ttstud import Ttest, PlotTtest
from criterias.ander import Anderson, PlotAnderson
from helpers.but_criterions import Сriterion, Submits

class MainWindow(QMainWindow):
    def __init__(self):
    
        QMainWindow.__init__(self)
        
        menuBar = self.menuBar()
        helpMenu = menuBar.addMenu("&О программе")
        self.help_action = QAction("Вывести", self)
        helpMenu.addAction(self.help_action)

        QToolTip.setFont(QFont('SansSerif', 10))
        self.help_action.setStatusTip('Эта программа предназначена для обработки данных')
        self.help_action.setToolTip('Эта программа предназначена для обработки данных')

        self.pl = None
        self.labels_end = None
        self.setWindowIcon(QIcon('pictures/icon.png'))
        
        self.setMinimumSize(QSize(1080, 520))         
        self.setWindowTitle("Критерии Согласия")   
        central_widget = QWidget(self)             
        self.setCentralWidget(central_widget)   
      
        self.grid_layout = QGridLayout(central_widget)  
        central_widget.setStyleSheet("QWidget{background-color: #f0f7f4;}")

        self.but_chi2 = Сriterion("\u03A7². Критерий Пирсона")
        self.but_kolm = Сriterion("Критерий Колмгорова")
        self.but_perm = Сriterion("Пермутационное тестирование")
        self.but_ttest = Сriterion("Критерий Стьюдента")
        self.but_anderson = Сriterion("Критерий Андерсона-Дарлинга")
        self.clear = QPushButton("Очистить")
        self.but_submit = Submits("Вычислить")
        
        self.current_but = 0
        self.all_criteria = {"chi2": self.but_chi2, "kolm": self.but_kolm, "perm": self.but_perm, "ttest": self.but_ttest, "ander": self.but_anderson}
        self.label = QLabel('0')


        lab = QLabel()
        lab.setPixmap(QPixmap("pictures/done.png"))

        self.widget_right = QWidget()
        self.widget_left = QWidget()
        
        self.widget_left.setMaximumWidth(290)
        
        self.grid_right = QGridLayout(self.widget_right)
        self.grid_left = QGridLayout(self.widget_left)
 

        self.grid_layout.addWidget(self.widget_left, 0, 0)
        self.grid_layout.addWidget(self.widget_right, 0, 1)
      

        self.upload_but = Submits("Сохранить данные")
        self.download_but = Submits("Выгрузить данные")
        self.grid_left.addWidget(self.but_chi2, 0, 0)
        self.grid_left.addWidget(self.but_kolm, 1, 0)
        self.grid_left.addWidget(self.but_perm, 2, 0)
        self.grid_left.addWidget(self.but_ttest, 3, 0)
        self.grid_left.addWidget(self.but_anderson, 4, 0)
        self.grid_left.addWidget(self.clear, 5, 0)
        
        self.alpha = 0.01
        
        self.spinBox = QSpinBox()
        self.spinBox.setRange(0, int(1e4))
        self.spinBox.setAccelerated(True)
        self.spinBox.setStyleSheet(
            """QSpinBox {
                border: 1px solid black;
                border-radius: 2px;
                padding: 2px;
            }""")
    
        self.dSpinBox = QDoubleSpinBox(minimum=0, maximum=1, singleStep=0.01, value=0.01)
        self.dSpinBox.setWrapping(True)
        self.dSpinBox.setStyleSheet(
            """QDoubleSpinBox {
                border: 1px solid black;
                border-radius: 2px;
                padding: 2px;
            }""")
    
        self.text_alpha = QLabel(text="Значение \u03B1:")
        self.text_size = QLabel(text="Число групп выборки:")
        self.Error = QLabel("Неправильный тип данных. Ошибка")
        self.Error.setStyleSheet("QLabel{ color: #eb1433;}")
        self.clear.setStyleSheet("""QPushButton {
                background-color: #f2f2f2;
                border-style: outset;
                border-width: 1px;
                border-radius: 9px;
                border-color: #000000;
                font: 14px;
                padding: 8px;}
            QPushButton:disabled  {
                
                background-color: #4f5c56;
                color: #b3b3b3;
                border-style: outset;
                border-width: 1px;
                border-radius: 9px;
                border-color: #000000;
                font: 14px;
                padding: 5px;
                }
            QPushButton:hover {
                color: #d93f53;
                background-color: #d1a9af;
            }
            """)

        self.table = QTableView()
        self.table.setStyleSheet('''
            QTableView {
               
                border: 1px solid black;
                border-radius: 4px;
                padding: 12px;
            }
            QTableView::item:selected {
                background-color: #CCCCCC;
                color: #FFFFFF;
            }
        ''')
     
        self.model = QStandardItemModel(2, 0)
        self.table.horizontalHeader().setVisible(False)

        self.dSpinBox.valueChanged.connect(self.editing_handler)

        self.but_chi2.clicked.connect(self.click_chi2)
        self.but_kolm.clicked.connect(self.click_kolm)
        self.but_perm.clicked.connect(self.click_perm)
        self.but_ttest.clicked.connect(self.click_ttest)
        self.but_anderson.clicked.connect(self.click_anderson)
        self.clear.clicked.connect(self.clearRightGrid)
        self.upload_but.clicked.connect(self.upload_model)
        self.download_but.clicked.connect(self.download_model)
        
        self.old_value = {"chi2": 0, "kolm": 0, "perm": 0, "ttest": 0, "ander": 0}
        self.old_alpha = {"chi2": 0, "kolm": 0, "perm": 0, "ttest": 0, "ander": 0}

        self.clear.setDisabled(True)
        self.widget_right.hide()
        
        self.saved_model = 0
        self.size = 0
        
    def upload_model(self):
        self.saved_model = self.model 

    def download_model(self):
        
        self.model = self.saved_model
        self.table.setModel(self.model)
        self.ui_criter()
        
    def editing_size_kolm(self):

       
        newColumnCount = self.spinBox.value()
        currentColumnCount = self.model.columnCount()

        if newColumnCount > currentColumnCount:
            for i in range(currentColumnCount, newColumnCount):
                self.model.insertColumn(i)
                item = QStandardItem(str(i + 1))
                self.model.setItem(0, i, item)
                self.table.setColumnWidth(i, 50)
        elif newColumnCount < currentColumnCount:
            for i in range(currentColumnCount - 1, newColumnCount - 1, -1):
                self.model.removeColumn(i)

        self.size = self.model.columnCount()
        self.table.setModel(self.model)
        self.ui_criter()
    def editing_size_standart(self, headers=0, n=0):
    
        newColumnCount = self.spinBox.value()
        currentColumnCount = self.model.columnCount()

        if newColumnCount > currentColumnCount:
            for i in range(currentColumnCount, newColumnCount):
                self.model.insertColumn(i)
                if(headers):
                    item = QStandardItem(headers)
                    self.model.setItem(0, i, item)
                    self.table.setColumnWidth(i, 90)
        elif newColumnCount < currentColumnCount:
            for i in range(currentColumnCount - 1, newColumnCount - 1, -1):
                self.model.removeColumn(i)

        self.size = self.model.columnCount()
        
        self.table.setModel(self.model)
        self.ui_criter()

    def editing_handler(self):
        print(round(self.dSpinBox.value(), 2))
        self.alpha = round(self.dSpinBox.value(), 2)

    def ui_criter(self):
        
        if(self.Error.parent()):
            self.Error.setParent(None)
        self.clear.setDisabled(False)
        self.widget_right.show()
        if(self.pl):
            self.pl.setParent(None)
            self.pl = None
        if self.labels_end:
            for w in self.wgds:
                w.setParent(None)
                w = None
            self.labels_end.setParent(None)
        self.spinBox.setValue(self.model.columnCount())
        self.dSpinBox.setValue(self.alpha)
        self.grid_right.addWidget(self.text_alpha, 0, 0, Qt.AlignRight)
        self.grid_right.addWidget(self.dSpinBox, 0, 1)
        self.grid_right.addWidget(self.text_size, 0, 2, Qt.AlignRight)
        self.grid_right.addWidget(self.spinBox, 0, 3)
        self.grid_right.addWidget(self.table, 1, 0, 1, 4)
        self.grid_right.addWidget(self.but_submit, 2, 3, 1, 1)
        if(self.saved_model):
            self.grid_right.addWidget(self.download_but, 2, 1, 1, 1)
        self.grid_right.addWidget(self.upload_but, 2, 0, 1, 1)

    def click_chi2(self):
       
        self.lock_button("chi2")
        self.clicks(["Интервалы", "n"], "chi2", 2, False)
        self.but_submit.clicked.connect(self.submit_chi2)
        self.spinBox.valueChanged.connect(lambda: self.editing_size_standart("[   ,   )"))
       
    def submit_chi2(self):
        
        a = [[0] * self.model.columnCount() for i in range(self.model.rowCount())]
        for x in range(self.model.rowCount()):
            for y in range(self.model.columnCount()):
                a[x][y] = self.model.item(x,y).text()
        try:
            chi2 = TableForX2([int(i) for i in a[1]], DataCheck.toCheck(a[0]), self.size, self.alpha)
        except Exception:
            
            self.grid_right.addWidget(self.Error, 2, 1, 1, 1)
            return

        if(chi2.chi_2 == self.old_value["chi2"] and chi2.alpha == self.old_alpha["chi2"]):
            return
        else:
            self.old_value["chi2"] = chi2.chi_2
            self.old_alpha["chi2"] = chi2.alpha
            self.ui_criter()
        
        self.labels_end = QHBoxLayout()
        self.H0orH1(chi2.chi_2, chi2.X2_table, self.labels_end, "pictures/chi2.png")
        self.grid_right.addLayout(self.labels_end, 3, 0, 1, 3)
        self.pl = PlotChi2(chi2)
        
        self.grid_right.addWidget(self.pl, 4, 0, 1, 4)
    

    def click_kolm(self):

        self.lock_button("kolm")
        self.spinBox.setValue(0)
        self.dSpinBox.setValue(0.01)
        self.but_submit.disconnect()
        self.model = QStandardItemModel(2, 0)
        self.model.setVerticalHeaderLabels(["x", "p"])
        self.table.setModel(self.model)
        verticalHeader = self.table.verticalHeader()
        verticalHeader.setMinimumWidth(50)  
        self.ui_criter()
        self.old_value["kolm"] = 0
        self.but_submit.clicked.connect(self.submit_kolm)
        self.spinBox.valueChanged.connect(self.editing_size_kolm)
        
        
    def submit_kolm(self):
        a = [[0] * self.model.columnCount() for i in range(self.model.rowCount())]
    
        for x in range(self.model.rowCount()):
            for y in range(self.model.columnCount()):
                a[x][y] = self.model.item(x,y).text()
       
        try:
            kolm = Kolm([float(i) for i in a[1]], self.size, self.alpha)
        except Exception:
            self.grid_right.addWidget(self.Error, 2, 1, 1, 1)
            return
        if(kolm.ks_stat == self.old_value["kolm"] and  kolm.alpha == self.old_alpha["kolm"] ):
            return
        else:
            self.old_alpha["kolm"] = kolm.alpha
            self.old_value["kolm"] = kolm.ks_stat
            self.ui_criter()
            
        
        self.labels_end = QHBoxLayout()
        self.H0orH1(kolm.ks_stat, kolm.critical_value, self.labels_end)
        self.grid_right.addLayout(self.labels_end, 3, 0, 1, 3)
        self.pl = PlotKolm(kolm)
        
        self.grid_right.addWidget(self.pl, 4, 0, 1, 4)




    def click_perm(self):
        self.lock_button("perm")
        self.clicks(["Группа №1", "Группа №2"], "perm", 2,  True)
        self.but_submit.clicked.connect(self.submit_perm)
        
    def submit_perm(self):
        a = [[0] * self.model.columnCount() for i in range(self.model.rowCount())]
    
        for x in range(self.model.rowCount()):
            for y in range(self.model.columnCount()):
                a[x][y] = self.model.item(x,y).text()
       
        try:
            perm = Permutation([int(i) for i in self.e(a[0])], [int(i) for i in self.e(a[1])], self.alpha)
        except Exception:
            self.grid_right.addWidget(self.Error, 2, 1, 1, 3)
            return
        if(perm.p_value == self.old_value["perm"] and  perm.alpha== self.old_alpha["perm"] ):
            return
        else:
            self.old_alpha["perm"] = perm.alpha
            self.old_value["perm"] = perm.p_value
            self.ui_criter()
            
        self.labels_end = QHBoxLayout()
        self.H0orH1(1-perm.p_value, 1-perm.alpha, self.labels_end)
        self.grid_right.addLayout(self.labels_end, 3, 0, 1, 3)
        self.pl = PlotPerm(perm)
        
        self.grid_right.addWidget(self.pl, 4, 0, 1, 4)

    def click_ttest(self):
        self.lock_button("ttest")
        self.clicks(["Группа №1", "Группа №2"], "ttest", 2,  True)
        self.but_submit.clicked.connect(self.submit_ttest)
    def submit_ttest(self):
        a = [[0] * self.model.columnCount() for i in range(self.model.rowCount())]
    
        for x in range(self.model.rowCount()):
            for y in range(self.model.columnCount()):
                try:
                    a[x][y] = self.model.item(x,y).text()
                except Exception:
                    a[x][y] = ''

       
        try:
            ttest = Ttest([int(i) for i in self.e(a[0])], [int(i) for i in self.e(a[1])], self.alpha)
        except Exception:
            self.grid_right.addWidget(self.Error, 2, 1, 1, 3)
            return
        if(ttest.p_value == self.old_value["ttest"] and  ttest.alpha== self.old_alpha["ttest"] ):
            return
        else:
            self.old_alpha["ttest"] = ttest.alpha
            self.old_value["ttest"] = ttest.p_value
            self.ui_criter()
            
        
        self.labels_end = QHBoxLayout()
        self.H0orH1(1-ttest.p_value, 1-ttest.alpha, self.labels_end)
        self.grid_right.addLayout(self.labels_end, 3, 0, 1, 3)
        self.pl = PlotTtest(ttest)
        self.grid_right.addWidget(self.pl, 4, 0, 1, 4)
    def click_anderson(self):
        self.lock_button("ander")
        self.clicks(["Выборка"], "ander", 1,  True)
        self.but_submit.clicked.connect(self.submit_anderson)
    def submit_anderson(self):
        a = [[0] * self.model.columnCount() for i in range(self.model.rowCount())]
    
        for x in range(self.model.rowCount()):
            for y in range(self.model.columnCount()):
                a[x][y] = self.model.item(x,y).text()
       
        try:
            
            ander = Anderson([int(i) for i in self.e(a[0])], self.alpha)
        except Exception:
            self.grid_right.addWidget(self.Error, 2, 1, 1, 3)
            return
        if(ander.statistic == self.old_value["ander"] and  ander.alpha== self.old_alpha["ander"] ):
            return
        else:
            self.old_alpha["ander"] = ander.alpha
            self.old_value["ander"] = ander.statistic
            self.ui_criter()
            
        
        self.labels_end = QHBoxLayout()
        self.H0orH1(ander.statistic, ander.critical_value, self.labels_end)
        self.grid_right.addLayout(self.labels_end, 3, 0, 1, 3)
        self.pl = PlotAnderson(ander)
        self.grid_right.addWidget(self.pl, 4, 0, 1, 4)

    def clearRightGrid(self):

        self.clear.setDisabled(True)
        self.widget_right.hide()
    def e(self,a):
        return  list(filter(lambda x: x!='', a))
    def clicks(self, headers, name, n, standart = False):
        self.dSpinBox.setValue(0.01)
        self.spinBox.setValue(0)
        self.but_submit.disconnect()
        self.model = QStandardItemModel(n, 0)
        self.model.setVerticalHeaderLabels(headers)
        self.table.setModel(self.model)
      
        self.ui_criter()
        self.old_value[name] = 0
        if(standart):
            self.spinBox.valueChanged.connect(lambda: self.editing_size_standart())
    def lock_button(self, locked):
        self.spinBox.disconnect()
        for k in self.all_criteria:
            self.all_criteria[k].setDisabled(False)
        self.all_criteria[locked].setDisabled(True)

    def H0orH1(self, threshold, critical, layout, path='pictures/arrow.png'):
        
        
        pict = QLabel()
        pict.setPixmap(QPixmap(path))
        label_1 = QLabel(str(round(threshold, 5)))
        label_2 = QLabel(str(round(critical, 5)))
        if(threshold <= critical):
            
            l = QLabel(" < ")
            label_1.setStyleSheet("QLabel{  color: #08b929;}")
            done = QLabel()
            done.setPixmap(QPixmap("pictures/done.png"))
        
            H0 = QLabel("Нет оснований отвергнуть проверяемую гипотезу")
            self.wgds = [pict, label_1, l, label_2, done, H0]
            for w in self.wgds:
                layout.addWidget(w)
        else:
            r = QLabel(" > ")
            label_1.setStyleSheet("QLabel{ color: #eb1433;}")
            H1 = QLabel("Отвергаем проверяемую гипотезу")
            close = QLabel()
            close.setPixmap(QPixmap("pictures/close.png"))
            
            self.wgds = [pict, label_1, r, label_2, close, H1]
            for w in self.wgds:
                layout.addWidget(w)

    def toList(self):
        a = [[0] * self.table.columnCount()] * self.table.rowCount()
        for x in range(self.table.rowCount()):
            for y in range(self.table.columnCount()):
                a[x][y] = int(self.table.item(x,y).text())
        
        print(a)

 
if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setStyleSheet("* { font-family: Arial; font-size: 16px; }")
    mainWindow = MainWindow()
    print(mainWindow.size)
    mainWindow.show()

    sys.exit(app.exec())