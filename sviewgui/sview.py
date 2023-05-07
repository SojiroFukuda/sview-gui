import sys
from PyQt6 import QtCore as Qc, QtGui as Qg, QtWidgets as Qw   
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import matplotlib
matplotlib.use("Qt5Agg")
import os
import re
import glob
import numpy as np
import pandas as pd
import random
# from . import sgui as gui # switch
import sgui as gui   # 
import matplotlib.cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as mcolors # default colour pallete 
from matplotlib import style
from matplotlib.font_manager import FontProperties

from matplotlib.lines import Line2D # default markars 
from pathlib import Path
# from PyQt5.Qt import PYQT_VERSION_STR
from datetime import datetime

import scipy.stats as st

import cmocean
import cmocean.cm
import seaborn as sns

import pygments
from pygments import formatters, lexers

#==================
# Display pandas dataframe at QTableWidget
#==================
class PandasModel(Qc.QAbstractTableModel): 
    def __init__(self, df = pd.DataFrame(), parent=None): 
        Qc.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole): 
        if role != Qt.ItemDataRole.DisplayRole:
            return Qc.QVariant()

        if orientation == Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError, ):
                return Qc.QVariant()
        elif orientation == Qt.Vertical:
            try:
                return self._df.index.tolist()[section]
            except (IndexError, ):
                return Qc.QVariant()

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return Qc.QVariant()

        if not index.isValid():
            return Qc.QVariant()

        return Qc.QVariant(str(self._df.iloc[index.row(), index.column()])) 

    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        return True

    def rowCount(self, parent=Qc.QModelIndex()): 
        return len(self._df.index)

    def columnCount(self, parent=Qc.QModelIndex()): 
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending= order == Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()


#==================
## Main Window #####
#==================
class Csviwer(Qw.QMainWindow):
    SCATTER = 0; DENSITY = 1; HISTGRAM = 2; LINE = 3; BOXPLOT = 4;
    STYLE = "monokai"           
    def __init__(self, parent=None, data=None):        
        super().__init__(parent)
        self.initUI(data)
    
    def initUI(self,data):
        # ui setting
        self.ui = gui.Ui_MainWindow()  
        self.ui.setupUi(self)               
        self.ui.logbox.setStyleSheet("background-color: rgb(39, 40, 34);")
        self.ui.logbox.document().setDefaultStyleSheet(formatters.HtmlFormatter(style=Csviwer.STYLE).get_style_defs('.highlight'))
        
        self.ui.button_csvPath.clicked.connect(self.readcsv) # type: ignore
        self.ui.cmb_x.currentIndexChanged.connect(self.setXaxis) # type: ignore
        self.ui.cmb_y.currentIndexChanged.connect(self.setYaxis) # type: ignore
        self.ui.cmb_color.currentIndexChanged.connect(self.setColor) # type: ignore
        self.ui.cmb_sort.currentIndexChanged.connect(self.setSort) # type: ignore
        self.ui.cmb_subcolor.currentIndexChanged.connect(self.setSubColor) # type: ignore
        self.ui.cmb_subsort.currentIndexChanged.connect(self.setSubSort) # type: ignore
        self.ui.cmb_subsubcolor.currentIndexChanged.connect(self.setSubsubColor) # type: ignore
        self.ui.cmb_subsubsort.currentIndexChanged.connect(self.setSubsubSort) # type: ignore
        self.ui.cmb_plot.currentIndexChanged.connect(self.setPlotType) # type: ignore
        self.ui.button_preview.clicked.connect(self.graphDraw) # type: ignore
        self.ui.button_save.clicked.connect(self.saveFigure) # type: ignore
        self.ui.cb_colorbar.stateChanged.connect(self.useColorbarI) # type: ignore
        self.ui.cb_subcolorbar.stateChanged.connect(self.useColorbarII) # type: ignore
        self.ui.cb_subsubcolorbar.stateChanged.connect(self.useColorbarIII) # type: ignore
        
        
        # Preamble log ===
        initial_str = "#This code is automatically generated by SView"+"\n"\
            +"#Based on matplotlib and seaborn"+"\n"\
            +"#========================"+"\n"\
            +"# package ----"+"\n"\
            +"import numpy as np"+"\n"\
            +"import pandas as pd"+"\n"\
            +"from matplotlib import style"+"\n"\
            +"import matplotlib.pyplot as plt"+"\n"\
            +"import matplotlib.colors as mcolors"+"\n"\
            +"from matplotlib.lines import Line2D"+"\n"\
            +"import seaborn as sns"+"\n"\
            +"import cmocean"+"\n"\
            +"# -------------"
        # highlight syntax ===
        lexer = lexers.get_lexer_by_name('python3')
        formatter = formatters.get_formatter_by_name('html')
        html = pygments.highlight(initial_str,lexer,formatter)
        self.ui.logbox.append(html)
        self.ui.logbox.moveCursor(Qg.QTextCursor.MoveOperation.End)
        self.isPandas = False
        self.CSV_PATH = "" # Path of csv
        self.HEADER_LIST = [] # List of header name of CSV file
        self.NUMERIC_HEADER_LIST = [] # List of header name of CSV file (only numeric data)
        self.SAVE_DIR = "" # Folda path where the graph will be exported
        self.SAVE_FILE_NAME = "" # Name of output graph
        self.SAVE_PATH = "" #  Path of saved graph
        self.isNumericMode = False
        self.setWindowTitle('CSV analyzer')
        #Graph area setting
        style.use('default')
        plt.rcParams['font.family'] ='arial' # Font
        plt.rcParams['xtick.direction'] = 'in'
        plt.rcParams['ytick.direction'] = 'in'
        plt.rcParams['legend.title_fontsize'] = 8
        fontP = FontProperties()
        fontP.set_size('x-small')
        # Prepare the figure canvas
        self.fig = Figure()
        self.fig.patch.set_facecolor('#98AFC7')
        self.ax1 = self.fig.add_subplot(111)
        self.canv = FigureCanvas(self.fig)
        self.canv.setSizePolicy(Qw.QSizePolicy.Policy.Expanding, Qw.QSizePolicy.Policy.Expanding)
        self.canv.updateGeometry()
        self.layout = Qw.QGridLayout(self.ui.canvas)
        self.layout.addWidget(self.canv)
        self.ui.cmb_cmap.addItems(cmocean.cm.cmap_d.keys())
        self.ui.cmb_style.addItems(sorted(style.available))
        self.PLOT_TYPE = Csviwer.SCATTER
        if data == None:
            pass
        else:
            self.loadData(data)


    def onStringChanged(self,value):
        # Log #--------------
        date_log = "<span style=\" font-size:13pt; font-weight:600; color:#8178FF;\" >"+"#"
        date_log += datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        date_log += "</span>" + "\n"
        # Syntax highlight
        self.ui.logbox.append(date_log)
        lexer = lexers.get_lexer_by_name('python3')
        formatter = formatters.get_formatter_by_name('html')
        html = pygments.highlight(value,lexer,formatter)
        self.ui.logbox.document().setDefaultStyleSheet(formatters.HtmlFormatter(style=Csviwer.STYLE).get_style_defs('.highlight'))
        self.ui.logbox.append(html)
        self.ui.logbox.moveCursor(Qg.QTextCursor.MoveOperation.End)

    def initToolBar(self):
        #==================
        # Init Tool bar
        #==================
        self.ui.frame_graph.setEnabled(True)
        self.ui.cmb_sort.setEnabled(False)
        self.ui.cmb_subsort.setEnabled(False)
        self.ui.cmb_subsubsort.setEnabled(False)
        self.ui.cb_colorbar.setEnabled(True)
        self.ui.cb_subcolorbar.setEnabled(False)
        self.ui.cb_subsubcolorbar.setEnabled(False)
        self.HEADER_LIST = self.csv.columns
        self.ui.cmb_color.clear()
        self.ui.cmb_subcolor.clear()
        self.ui.cmb_subsubcolor.clear()
        self.ui.cmb_x.clear()
        self.ui.cmb_y.clear()
        self.ui.cmb_color.addItem("None_")
        self.ui.cmb_subcolor.addItem("None_")
        self.ui.cmb_subsubcolor.addItem("None_") 
        
    def addHeaderName(self,HEADER_LIST):
        for i,item in enumerate(HEADER_LIST):
            self.ui.cmb_color.addItem(item)
            self.ui.cmb_subcolor.addItem(item)
            self.ui.cmb_subsubcolor.addItem(item)
            self.ui.cmb_x.addItem(item)
            self.ui.cmb_y.addItem(item)
            # add only numeric data into X and Y axis lists
            isNumeric = True
            for comp in self.csv[item]:
                if isinstance(comp,str):
                    isNumeric = False
                    break
            if isNumeric:
                self.NUMERIC_HEADER_LIST.append(item)
        self.setXaxis()
        self.setYaxis()
        
    def loadData(self,data): #import csv file path
        # import CSV
        strflag = 0
        if type(data) == None:
            return
        if isinstance(data,str) and data != 'None':
            self.CSV_PATH = data
            try:
                data = pd.read_csv(data)
            except FileNotFoundError as e:
                raise e
            except:
                print("Unexpected error:",sys.exc_info()[0])
                raise
            finally:
                strflag = 1
                self.ui.textbox_csvPath.setText(self.CSV_PATH)

        if strflag == 0:
            self.ui.textbox_csvPath.setText("")

            self.isPandas = True
        self.csv = data
        self.csv["Row_INDEX_"] = np.linspace(1,len(self.csv),len(self.csv))
        self.data = data
        self.data["Row_INDEX_"] = np.linspace(1,len(self.data),len(self.data))
        # set Table
        model = PandasModel(self.csv)
        self.ui.table_summary.setModel(model)
        #==================
        # Init Tool bar
        #==================
        self.initToolBar()
        #==================
        # add header name into lists
        #==================
        self.addHeaderName(self.HEADER_LIST)

    def readcsv(self): #import csv file path
        # import CSV
        path = self.openFile()
        if path == '':
            return
        self.ui.textbox_csvPath.setText(path)
        self.CSV_PATH = path
        self.csv = pd.read_csv(path)
        self.csv["Row_INDEX_"] = np.linspace(1,len(self.csv),len(self.csv))
        self.data = pd.read_csv(path)
        self.data["Row_INDEX_"] = np.linspace(1,len(self.data),len(self.data))
        # set Table
        model = PandasModel(self.csv)
        self.ui.table_summary.setModel(model)
        #==================
        # Init Tool bar
        #==================
        self.initToolBar()
        #==================
        # add header name into lists
        #==================
        self.addHeaderName(self.HEADER_LIST)
                

    def setPlotType(self):
        self.PLOT_TYPE = self.ui.cmb_plot.currentIndex()
        if self.PLOT_TYPE == Csviwer.HISTGRAM: #Histogram
            self.ui.cmb_y.setEnabled(False)
            self.ui.cmb_x.setEnabled(True)
        elif self.PLOT_TYPE == Csviwer.SCATTER:
            self.ui.cmb_y.setEnabled(True)
            self.ui.cmb_x.setEnabled(True)
        elif self.PLOT_TYPE == Csviwer.DENSITY:
            self.ui.cmb_y.setEnabled(True)
            self.ui.cmb_x.setEnabled(True)
        elif self.PLOT_TYPE == Csviwer.LINE:
            self.ui.cmb_y.setEnabled(True)
            self.ui.cmb_x.setEnabled(True)
        elif self.PLOT_TYPE == Csviwer.BOXPLOT:
            self.ui.cmb_y.setEnabled(True)
            self.ui.cmb_x.setEnabled(True)

    def openFile(self): # select csv file
        filePath, _ = Qw.QFileDialog.getOpenFileName(self, "Open File",
                self.CSV_PATH, "csv files (*.csv)")
        return filePath

    def setXaxis(self):
        self.x_var = str(self.ui.cmb_x.currentText())
        if self.x_var in self.NUMERIC_HEADER_LIST:
            self.ax1.set_xlim( min(self.csv[self.x_var].replace([np.inf, -np.inf], np.nan).dropna()) - abs(min(self.csv[self.x_var].replace([np.inf, -np.inf], np.nan).dropna())/10), max(self.csv[self.x_var].replace([np.inf, -np.inf], np.nan).dropna()) + abs(max(self.csv[self.x_var].replace([np.inf, -np.inf], np.nan).dropna())/10) )
            self.ui.dsb_xmin.setEnabled(True); self.ui.dsb_xmax.setEnabled(True)
            self.ui.dsb_xmin.setRange(-np.inf,np.inf); self.ui.dsb_xmax.setRange(-np.inf,np.inf)
            self.ui.dsb_xmin.setValue( min(self.csv[self.x_var].replace([np.inf, -np.inf], np.nan).dropna()) - abs(min(self.csv[self.x_var].replace([np.inf, -np.inf], np.nan).dropna())/10) )
            self.ui.dsb_xmax.setValue( max(self.csv[self.x_var].replace([np.inf, -np.inf], np.nan).dropna()) + abs(max(self.csv[self.x_var].replace([np.inf, -np.inf], np.nan).dropna())/10) )
        else:
            self.ui.dsb_xmin.setEnabled(False); self.ui.dsb_xmax.setEnabled(False)
            self.ui.dsb_xmin.setRange(0,0); self.ui.dsb_xmax.setRange(0,0)
    def setYaxis(self):
        self.y_var = str(self.ui.cmb_y.currentText())
        if self.y_var in self.NUMERIC_HEADER_LIST:
            self.ax1.set_ylim( min(self.csv[self.y_var].replace([np.inf, -np.inf], np.nan).dropna()) - abs(min(self.csv[self.y_var].replace([np.inf, -np.inf], np.nan).dropna())/10), max(self.csv[self.y_var].replace([np.inf, -np.inf], np.nan).dropna()) + abs(max(self.csv[self.y_var].replace([np.inf, -np.inf], np.nan).dropna())/10) )
            self.ui.dsb_ymin.setEnabled(True); self.ui.dsb_ymax.setEnabled(True)
            self.ui.dsb_ymin.setRange(-np.inf,np.inf); self.ui.dsb_ymax.setRange(-np.inf,np.inf)
            self.ui.dsb_ymin.setValue( min(self.csv[self.y_var].replace([np.inf, -np.inf], np.nan).dropna()) - abs(min(self.csv[self.y_var].replace([np.inf, -np.inf], np.nan).dropna())/10) )
            self.ui.dsb_ymax.setValue( max(self.csv[self.y_var].replace([np.inf, -np.inf], np.nan).dropna()) + abs(max(self.csv[self.y_var].replace([np.inf, -np.inf], np.nan).dropna())/10) )
        else:
            self.ui.dsb_ymin.setEnabled(False); self.ui.dsb_ymax.setEnabled(False)
            self.ui.dsb_ymin.setRange(0,0); self.ui.dsb_ymax.setRange(0,0)

    def useColorMapI(self):
        pass
    def useColorMapII(self):
        pass
    def useColorMapIII(self):
        pass

    def setColor(self):
        ind = self.ui.cmb_color.currentIndex()
        tex = str(self.ui.cmb_color.currentText())
        self.color_var = tex
        if ind > 0:
            # self.color_var = tex
            # self.group_var = self.color_var
            isNumeric = True
            # isInteger = False
            for comp in self.csv[self.color_var]:
                if isinstance(comp,str):
                    isNumeric = False
                    break
            if isNumeric:
                self.ui.cmb_sort.clear()
                self.ui.cmb_sort.setEnabled(False)
                self.isNumericMode = True
                self.ui.cb_colorbar.setChecked(True)
                self.ui.cb_colorbar.setEnabled(True)
                self.ui.dsb_cmin.setRange(-np.inf,np.inf); self.ui.dsb_cmax.setRange(-np.inf,np.inf)
                if len( str(min( self.csv[self.color_var].replace([np.inf, -np.inf], np.nan).dropna() )).split('.') )==2:
                    dec = max( len(str(min( self.csv[self.color_var].replace([np.inf, -np.inf], np.nan).dropna() )).split('.')[1]), len(str(max( self.csv[self.color_var].replace([np.inf, -np.inf], np.nan).dropna() )).split('.')[1]))
                else:
                    dec = 0
                self.ui.dsb_cmin.setDecimals(dec+2); self.ui.dsb_cmax.setDecimals(dec+2)
                self.ui.dsb_cmin.setSingleStep(np.power(0.1,dec+2));self.ui.dsb_cmax.setSingleStep(np.power(0.1,dec+2))
                self.ui.dsb_cmin.setValue( min( self.csv[self.color_var].replace([np.inf, -np.inf], np.nan).dropna() ) )
                self.ui.dsb_cmax.setValue( max( self.csv[self.color_var].replace([np.inf, -np.inf], np.nan).dropna() ) )
            else:
                self.isNumericMode = False
                self.ui.cmb_sort.setEnabled(True)
                self.ui.cmb_subcolor.setEnabled(True)
                self.ui.cmb_subsort.setEnabled(True)
                self.ui.cmb_sort.clear()
                self.ui.cmb_sort.addItem("All_")
                self.ui.cb_colorbar.setChecked(False)
                self.ui.cb_colorbar.setEnabled(False)
                sort_list = pd.unique(self.csv[self.color_var])
                for i,sort_item in enumerate(sort_list):
                    self.ui.cmb_sort.addItem(str(sort_item))
        else:
            # self.color_var = tex
            # self.group_var = self.color_var
            self.isNumericMode = False
            self.ui.cmb_sort.clear()
            self.ui.cmb_subcolor.clear()
            self.ui.cmb_subsort.clear()
            self.ui.cmb_subsubcolor.clear()
            self.ui.cmb_subsubsort.clear()
            self.ui.cmb_sort.setEnabled(False)
            self.ui.cmb_subcolor.setEnabled(False)
            self.ui.cmb_subsort.setEnabled(False)
            self.ui.cmb_subsubcolor.setEnabled(False)
            self.ui.cmb_subsubsort.setEnabled(False)
            self.ui.cb_colorbar.setChecked(False)
            self.ui.cb_colorbar.setEnabled(False)
            self.ui.cb_subcolorbar.setChecked(False)
            self.ui.cb_subcolorbar.setEnabled(False)
            self.ui.cb_subsubcolorbar.setChecked(False)
            self.ui.cb_subsubcolorbar.setEnabled(False)

    def setSort(self):
        ind = self.ui.cmb_sort.currentIndex()
        tex = self.ui.cmb_sort.currentText()
        if ind > 0:
            self.ui.cmb_subcolor.setEnabled(True)
            self.ui.cmb_subsort.setEnabled(True)
            if self.ui.cmb_subcolor.count()==1:
                # self.ui.cmb_color.addItem("None_")
                # self.ui.cmb_subcolor.addItem("None_")
                # self.ui.cmb_subsubcolor.addItem("None_") 
                for i,item in enumerate(self.HEADER_LIST):
                    # self.ui.cmb_color.addItem(item)
                    self.ui.cmb_subcolor.addItem(item)
                    # self.ui.cmb_subsubcolor.addItem(item)
            if tex.isdecimal():
                self.data = self.csv.loc[self.csv[self.color_var]==float(tex)]
            else:
                self.data = self.csv.loc[self.csv[self.color_var]==tex]
        else:
            self.ui.cmb_subcolor.setEnabled(False)
            self.ui.cmb_subsort.setEnabled(False)
            self.ui.cmb_subsubcolor.setEnabled(False)
            self.ui.cmb_subsubsort.setEnabled(False)
            self.ui.cmb_subcolor.clear()
            self.ui.cmb_subsort.clear()
            self.ui.cmb_subsubcolor.clear()
            self.ui.cmb_subsubsort.clear()
             # self.ui.cmb_color.addItem("None_")
            self.ui.cmb_subcolor.addItem("None_")
            self.ui.cmb_subsubcolor.addItem("None_") 

            self.data = self.csv
        model = PandasModel(self.data)
        self.ui.table_sorted.setModel(model)   

    def setSubColor(self):
        ind = self.ui.cmb_subcolor.currentIndex()
        tex = self.ui.cmb_subcolor.currentText()
        self.subcolor_var = tex
        if ind > 0:
            # self.subcolor_var = tex
            # self.group_var = self.subcolor_var
            isNumeric = True
            # isInteger = False
            for comp in self.data[self.subcolor_var]:
                if isinstance(comp,str):
                    isNumeric = False
                    break
            if isNumeric:
                self.ui.cmb_subsort.clear()
                self.ui.cmb_subsort.setEnabled(False)
                self.ui.cb_subcolorbar.setChecked(True)
                self.ui.cb_subcolorbar.setEnabled(True)
                self.ui.dsb_cmin.setRange(-np.inf,np.inf); self.ui.dsb_cmax.setRange(-np.inf,np.inf)
                self.ui.dsb_cmin.setValue( min( self.data[self.subcolor_var].replace([np.inf, -np.inf], np.nan).dropna() ) )
                self.ui.dsb_cmax.setValue( max( self.data[self.subcolor_var].replace([np.inf, -np.inf], np.nan).dropna() ) )
                self.isNumericMode = True
            else:
                self.isNumericMode = False
                self.ui.cmb_subsort.setEnabled(True)
                self.ui.cb_subcolorbar.setChecked(False)
                self.ui.cb_subcolorbar.setEnabled(False)
                self.ui.cmb_subsort.clear()
                self.ui.cmb_subsort.addItem("All_")
                sort_list = pd.unique(self.csv[self.subcolor_var])
                for i,sort_item in enumerate(sort_list):
                    self.ui.cmb_subsort.addItem(str(sort_item))
        else:
            # self.subcolor_var = tex
            # self.group_var = self.color_var
            self.isNumericMode = False
            self.ui.cmb_subsort.clear()
            self.ui.cmb_subsubcolor.clear()
            self.ui.cmb_subsubsort.clear()
            self.ui.cmb_subsort.setEnabled(False)
            self.ui.cmb_subsubcolor.setEnabled(False)
            self.ui.cmb_subsubsort.setEnabled(False)
            self.ui.cb_subcolorbar.setChecked(False)
            self.ui.cb_subcolorbar.setEnabled(False)


    def setSubSort(self):
        if self.ui.cmb_sort.currentText() == '':
             return
        ind = self.ui.cmb_subsort.currentIndex()
        tex = self.ui.cmb_subsort.currentText()
        if ind > 0:
            self.ui.cmb_subsubcolor.setEnabled(True)
            self.ui.cmb_subsubsort.setEnabled(True)
            if self.ui.cmb_subsubcolor.count()==1: 
                for i,item in enumerate(self.HEADER_LIST):
                    self.ui.cmb_subsubcolor.addItem(item)
            if self.ui.cmb_sort.currentText().isdecimal():
                data_temp = self.csv.loc[self.csv[self.color_var] == float(self.ui.cmb_sort.currentText())]
            else:
                data_temp = self.csv.loc[self.csv[self.color_var] == self.ui.cmb_sort.currentText()]
            # data_temp = self.csv.loc[self.csv[self.color_var]==self.ui.cmb_sort.currentText()]
            if tex.isdecimal():
                self.data = data_temp.loc[data_temp[self.subcolor_var]==float(tex)]
            else:
                self.data = data_temp.loc[data_temp[self.subcolor_var]==tex]
            # self.data = data_temp.loc[data_temp[self.subcolor_var]==tex]
        else:
            self.ui.cmb_subsubcolor.setEnabled(False)
            self.ui.cmb_subsubsort.setEnabled(False)
            self.ui.cmb_subsubcolor.clear()
            self.ui.cmb_subsubsort.clear()
            # self.ui.cmb_subcolor.addItem("None_")
            self.ui.cmb_subsubcolor.addItem("None_") 
            if self.ui.cmb_sort.currentText().isdecimal():
                self.data = self.csv.loc[self.csv[self.color_var]==float(self.ui.cmb_sort.currentText())]
            else:
                self.data = self.csv.loc[self.csv[self.color_var]==self.ui.cmb_sort.currentText()]
            # self.data = self.csv.loc[self.csv[self.color_var]==self.ui.cmb_sort.currentText()]
        model = PandasModel(self.data)
        self.ui.table_sorted.setModel(model)   

    def setSubsubColor(self):
        ind = self.ui.cmb_subsubcolor.currentIndex()
        tex = str(self.ui.cmb_subsubcolor.currentText())
        self.subsubcolor_var = tex
        if ind > 0:
            # self.group_var = self.subsubcolor_var
            isNumeric = True
            # isInteger = False
            for comp in self.data[ self.subsubcolor_var]:
                if isinstance(comp,str):
                    isNumeric = False
                    break
            if isNumeric:
                self.ui.cmb_subsubsort.clear()
                self.ui.cmb_subsubsort.setEnabled(False)
                self.ui.cb_subsubcolorbar.setChecked(True)
                self.ui.cb_subsubcolorbar.setEnabled(True)
                self.ui.dsb_cmin.setRange(-np.inf,np.inf); self.ui.dsb_cmax.setRange(-np.inf,np.inf)
                self.ui.dsb_cmin.setValue( min( self.data[self.subsubcolor_var].replace([np.inf, -np.inf], np.nan).dropna() ) )
                self.ui.dsb_cmax.setValue( max( self.data[self.subsubcolor_var].replace([np.inf, -np.inf], np.nan).dropna() ) )
                self.isNumericMode = True
            else:
                self.isNumericMode = False
                self.ui.cmb_subsubsort.setEnabled(True)
                self.ui.cb_subsubcolorbar.setChecked(False)
                self.ui.cb_subsubcolorbar.setEnabled(False)
                self.ui.cmb_subsubsort.clear()
                self.ui.cmb_subsubsort.addItem("All_")
                sort_list = pd.unique(self.csv[self.subsubcolor_var])
                for i,sort_item in enumerate(sort_list):
                    self.ui.cmb_subsubsort.addItem(str(sort_item))
        else:
            # self.subsubcolor_var = "None_"
            # self.group_var = self.subcolor_var
            self.isNumericMode = False
            self.ui.cmb_subsubsort.clear()
            self.ui.cmb_subsubsort.setEnabled(False)
            self.ui.cb_subsubcolorbar.setChecked(False)
            self.ui.cb_subsubcolorbar.setEnabled(False)


    def setSubsubSort(self):
        if self.ui.cmb_subsort.currentText() == '':
             return
        ind = self.ui.cmb_subsubsort.currentIndex()
        tex = str(self.ui.cmb_subsubsort.currentText())
        if ind > 0:
            if self.ui.cmb_sort.currentText().isdecimal():
                data_temp = self.csv.loc[self.csv[self.color_var] == float(self.ui.cmb_sort.currentText())]
            else:
                data_temp = self.csv.loc[self.csv[self.color_var] == self.ui.cmb_sort.currentText()]
            # data_temp = self.csv.loc[self.csv[self.color_var]==self.ui.cmb_sort.currentText()]
            if self.ui.cmb_subsort.currentText().isdecimal():
                data_temp = data_temp.loc[data_temp[self.subcolor_var]==float(self.ui.cmb_subsort.currentText())]
            else:
                data_temp = data_temp.loc[data_temp[self.subcolor_var]==self.ui.cmb_subsort.currentText()]
            if tex.isdecimal():
                self.data = data_temp.loc[data_temp[self.subsubcolor_var]==float(tex)]
            else:
                self.data = data_temp.loc[data_temp[self.subsubcolor_var]==tex]
        else:
            data_temp = self.csv.loc[self.csv[self.color_var]==self.ui.cmb_sort.currentText()]
            self.data = data_temp.loc[data_temp[self.subcolor_var]==self.ui.cmb_subsort.currentText()]
        model = PandasModel(self.data)
        self.ui.table_sorted.setModel(model)


    def checkPlot(self):
        pass
    
    def useColorbarI(self):
        checked = self.ui.cb_colorbar.isChecked()
        self.ui.cmb_sort.clear()
        if checked:
            self.isNumericMode = True
            self.ui.cmb_sort.setEnabled(False)
        else:
            self.isNumericMode = False
            self.ui.cmb_sort.setEnabled(True)
            self.ui.cmb_sort.addItem("All_")
            if self.color_var == 'None_':
                pass
            else:
                sort_list = pd.unique(self.csv[self.color_var])
                for i,sort_item in enumerate(sort_list):
                    self.ui.cmb_sort.addItem(str(sort_item))


    def useColorbarII(self):
        checked = self.ui.cb_subcolorbar.isChecked()
        self.ui.cmb_subsort.clear()
        if checked:
            self.isNumericMode = True
            self.ui.cmb_subsort.setEnabled(False)
        else:
            self.isNumericMode = False
            self.ui.cmb_subsort.setEnabled(True)
            self.ui.cmb_subsort.addItem("All_")
            if self.subcolor_var == 'None_':
                pass
            else:
                sort_list = pd.unique(self.csv[self.subcolor_var])
                for i,sort_item in enumerate(sort_list):
                    self.ui.cmb_subsort.addItem(str(sort_item))
    
    def useColorbarIII(self):
        checked = self.ui.cb_subsubcolorbar.isChecked()
        self.ui.cmb_subsubsort.clear()
        if checked:
            self.isNumericMode = True
            self.ui.cmb_subsubsort.setEnabled(False)
        else:
            self.isNumericMode = False
            self.ui.cmb_subsubsort.setEnabled(True)
            self.ui.cmb_subsubsort.addItem("All_")
            if self.subsubcolor_var == 'None_':
                pass
            else:
                sort_list = pd.unique(self.csv[self.subsubcolor_var])
                for i,sort_item in enumerate(sort_list):
                    self.ui.cmb_subsubsort.addItem(str(sort_item))
                
    def load_magicNum(self):
        SCATTER = 0; DENSITY = 1; HISTGRAM = 2; LINE = 3; BOXPLOT = 4; ALL_SORT = 0
        return (SCATTER,DENSITY,HISTGRAM,LINE,BOXPLOT,ALL_SORT)
    
    def diagnose(self,array):
        def isfloat(s):
            try:
                float(s)
            except ValueError:
                return False
            else:
                return True
        def isnan(s):
            try:
                np.isnan(s)
            except TypeError:
                return False
            else:
                return np.isnan(s)
        float_ind = [ isfloat(var) for var in array] # booleans if a value is compativle with float
        num_str = len(float_ind) - np.sum(float_ind) # Number of non-float values (mostly string)
        float_array = [float(var) for var in [array[ind] for ind,val in enumerate(float_ind) if val == True] ] # float-compatible
        nan_ind = [isnan(var) for var in float_array]  
        num_nan = np.sum(nan_ind) # Number of NaN
        nan_safe_array = [float(float_array[ind]) for ind,val in enumerate(nan_ind) if val == False]
        inf_ind = [np.isinf(var) for var in nan_safe_array]
        num_inf = np.sum(inf_ind) # Number of Inf
        inf_safe_array = [float(nan_safe_array[ind]) for ind,val in enumerate(inf_ind) if val == False]
        return {'Total':len(array),'Numeric':len(inf_safe_array) ,'String':num_str,'NaN':num_nan,'Inf':num_inf}
    
    def isLightColor(self,rgbColor=[0,128,255]):
        [r,g,b]=rgbColor
        hsp = np.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b))
        if (hsp>100):
            return True
        else:
            return False
    def rgb2gray(self,rgb):
        r, g, b = rgb[0], rgb[1], rgb[2]
        gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
        return gray
    #############################
    
    #      DRAW GRAH
    
    #############################
    def graphDraw(self):
        style.use(str(self.ui.cmb_style.currentText()))
            
        if self.isNumericMode:
#             self.graphDraw_Numeric_Syntax()
            try:
               self.graphDraw_Numeric_Syntax()
            except ValueError as e:
                print(e)
                self.fig.clf()
                self.ax1.clear()
                self.ax1 = self.fig.add_subplot(111)
                Error_str = 'ValueError'+'\n'+'Something wrong happened.'+ '\n' + 'Please check if youd original data contains Nan or Inf values, which might be a pottential cause of this error.'+'n'\
                +'X axis: '+str(self.x_var) +'\n'\
                +'Y axis: '+str(self.y_var) +'\n'\
                +'#== Initial diagnosis ===#' + '\n'\
                +'Selected data:'+str(len(self.data[self.x_var]))+' from '+str(len(self.csv[self.x_var]))+' data points'+'\n'\
                +'X axis:' + str(self.diagnose(self.data[self.x_var])) + '\n'\
                +'Y axis:'+str(self.diagnose(self.data[self.y_var]))
                self.ax1.text(0.1, 0.7, Error_str, transform=self.ax1.transAxes, weight='bold')
                self.fig.canvas.draw_idle()
                self.ui.tab_pca.setCurrentIndex(2)
            except TypeError as e:
                print(e)
                self.fig.clf()
                self.ax1.clear()
                self.ax1 = self.fig.add_subplot(111)
                Error_str = 'TypeError'+'\n'+'Please check your axes setting or original data' + '\n' + 'Tip: Either X or Y axis should be a numeric data.'+'\n'\
                +'X axis: '+str(self.x_var) +'\n'\
                +'Y axis: '+str(self.y_var) +'\n'\
                +'#== Initial diagnosis ===#' + '\n'\
                +'Selected data:'+str(len(self.data[self.x_var]))+' from '+str(len(self.csv[self.x_var]))+' data points'+'\n'\
                +'X axis:' + str(self.diagnose(self.data[self.x_var])) + '\n'\
                +'Y axis:'+str(self.diagnose(self.data[self.y_var]))
                self.ax1.text(0.1, 0.7, Error_str, transform=self.ax1.transAxes, weight='bold')
                self.fig.canvas.draw_idle()
                self.ui.tab_pca.setCurrentIndex(2)
        else:
#             self.graphDraw_nonNumeric_Syntax()
            try:
               self.graphDraw_nonNumeric_Syntax()
            except ValueError as e:
                print(e)
                self.fig.clf()
                self.ax1.clear()
                self.ax1 = self.fig.add_subplot(111)
                Error_str = 'ValueError'+'\n'+'Something wrong happened.'+ '\n' + 'Please check if youd original data contains Nan or Inf values, which might be a pottential cause of this error.'+'n'\
                +'X axis: '+str(self.x_var) +'\n'\
                +'Y axis: '+str(self.y_var) +'\n'\
                +'#== Initial diagnosis ===#' + '\n'\
                +'Selected data:'+str(len(self.data[self.x_var]))+' from '+str(len(self.csv[self.x_var]))+' data points'+'\n'\
                +'X axis:' + str(self.diagnose(self.data[self.x_var])) + '\n'\
                +'Y axis:'+str(self.diagnose(self.data[self.y_var]))
                self.ax1.text(0.1, 0.7, Error_str, transform=self.ax1.transAxes, weight='bold')
                self.fig.canvas.draw_idle()
                self.ui.tab_pca.setCurrentIndex(2)
            except TypeError as e:
                print(e)
                self.fig.clf()
                self.ax1.clear()
                self.ax1 = self.fig.add_subplot(111)
                Error_str = 'TypeError'+'\n'+'Please check your axes setting or original data' + '\n' + 'Tip: Either X or Y axis should be a numeric data.'+'\n'\
                +'X axis: '+str(self.x_var) +'\n'\
                +'Y axis: '+str(self.y_var) +'\n'\
                +'#== Initial diagnosis ===#' + '\n'\
                +'Selected data:'+str(len(self.data[self.x_var]))+' from '+str(len(self.csv[self.x_var]))+' data points'+'\n'\
                +'X axis:' + str(self.diagnose(self.data[self.x_var])) + '\n'\
                +'Y axis:'+str(self.diagnose(self.data[self.y_var]))
                self.ax1.text(0.1, 0.7, Error_str, transform=self.ax1.transAxes, weight='bold')
                self.fig.canvas.draw_idle()
                self.ui.tab_pca.setCurrentIndex(2)
        # Adjust backgroun color
        if self.rgb2gray( np.array( mcolors.to_rgb( mcolors.to_hex( self.ax1.xaxis.label.get_color() ) ) )*255 ) < 160:
            self.fig.patch.set_facecolor('#98AFC7')
        else:
            self.fig.patch.set_facecolor('black')
        self.fig.canvas.draw_idle()
                

    def scatterplot(self,data,x_var,y_var,keyDict,withColorbar=False):
        logstring = ''
        if withColorbar == False:
            self.ax1.scatter(data[x_var].replace([np.inf, -np.inf], np.nan),
                             data[y_var].replace([np.inf, -np.inf], np.nan),
                             s = keyDict['msize'],
                             color = keyDict['color'],
                             alpha = keyDict['alpha'],
                             label = keyDict['label']
                            )
            # Log #-----------------------
            logstring += 'ax.scatter('+keyDict['data_var_str']+'["'+x_var+'"].replace([np.inf, -np.inf], np.nan), '+keyDict['data_var_str']+'["'+y_var+'"].replace([np.inf, -np.inf], np.nan), s = '+str(keyDict['msize'])+', alpha ='+str(keyDict['alpha'])+',color="' + str(keyDict['color'])+'", label=\''+ str(keyDict['label']) +'\')' + '\n'
            # ----------------------------
        elif withColorbar:
            if keyDict['logc']:
                clb = plt.colorbar(self.ax1.scatter(data[x_var].replace([np.inf, -np.inf],np.nan), 
                                                    data[y_var].replace([np.inf, -np.inf], np.nan),
                                                    c = data[keyDict['cvar']],
                                                    cmap = "cmo."+ keyDict['cmap'],
                                                    s = keyDict['msize'],
                                                    alpha = keyDict['alpha'],
                                                    norm=mcolors.SymLogNorm(min(abs(data[keyDict['cvar']])),vmin=keyDict['vmin'],vmax=keyDict['vmax'])
                                                   ),
                                   ax=self.ax1
                                  )
                # Log #-----------------------
                logstring += 'clb = plt.colorbar( ax.scatter('+keyDict['data_var_str']+'["'+str(x_var)+'"].replace( [np.inf, -np.inf], np.nan ), '+keyDict['data_var_str']+'["'+str(y_var)+'"].replace( [np.inf, -np.inf], np.nan), c = '+keyDict['data_var_str']+'["' + str(keyDict['cvar']) + '"], cmap = "cmo." + "'+str(keyDict['cmap'])+'", s = '+str(keyDict['msize'])+', alpha='+str(keyDict['alpha'])+',norm=mcolors.SymLogNorm(min(abs('+str(keyDict['data_var_str'])+'[\''+str(keyDict['cvar'])+'\'])),vmin='+str(keyDict['vmin'])+',vmax='+str(keyDict['vmax'])+') ), ax = ax) ' + '\n'
                logstring += 'clb.ax.set_title("' + str(keyDict['cvar']) + '")' + '\n'
                # ----------------------------
            else:
                clb = plt.colorbar(self.ax1.scatter(data[x_var].replace([np.inf, -np.inf],np.nan), 
                                                    data[y_var].replace([np.inf, -np.inf],np.nan),
                                                    c = data[keyDict['cvar']],
                                                    cmap = "cmo."+ keyDict['cmap'],
                                                    s = keyDict['msize'],
                                                    alpha = keyDict['alpha'],
                                                    vmin=keyDict['vmin'],
                                                    vmax=keyDict['vmax']
                                                   ),
                                   ax=self.ax1
                                  )
                # Log #-----------------------
                logstring += 'clb = plt.colorbar( ax.scatter('+keyDict['data_var_str']+'["'+str(x_var)+'"].replace( [np.inf, -np.inf], np.nan ), '+keyDict['data_var_str']+'["'+str(y_var)+'"].replace( [np.inf, -np.inf], np.nan), c = '+keyDict['data_var_str']+'["' + str(keyDict['cvar']) + '"], cmap = "cmo." + "'+str(keyDict['cmap'])+'", s = '+str(keyDict['msize'])+', vmin = '+str(keyDict['vmin'])+', vmax = ' + str(keyDict['vmax']) + '  , alpha = '+str(keyDict['alpha'])+'), ax = ax) ' + '\n'
                logstring += 'clb.ax.set_title("' + str(keyDict['cvar']) + '")' + '\n'
                # ----------------------------
            clb.ax.set_title(str(keyDict['cvar']))
            
        return logstring
    
    
    def lighten_color(self,color, amount=0.5):
        """
        Lightens the given color by multiplying (1-luminosity) by the given amount.
        Input can be matplotlib color string, hex string, or RGB tuple.

        Examples:
        >> lighten_color('g', 0.3)
        >> lighten_color('#F034A3', 0.6)
        >> lighten_color((.3,.55,.1), 0.5)
        """
        import colorsys
        try:
            c = mcolors.cnames[color]
        except:
            c = color
        c = colorsys.rgb_to_hls(*mcolors.to_rgb(c))
        return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])
    
    def densityplot(self,data,x_var,y_var,keyDict,isMultiplePlot=False):
        log_str = ''
        if isMultiplePlot:
            if len(data) != 0:
                
                newpalette = [self.lighten_color(var,keyDict['alpha']) for var in plt.rcParams['axes.prop_cycle'].by_key()['color']]
                sns.scatterplot(data=data.replace([np.inf, -np.inf], np.nan), x = x_var, y = y_var, hue = keyDict['cvar'], alpha=keyDict['alpha'], palette=newpalette[0:len(pd.unique(data[keyDict['cvar']]))], ax=self.ax1)
                sns.kdeplot(data=data.replace([np.inf, -np.inf], np.nan), x = x_var, y = y_var, hue = keyDict['cvar'],legend=keyDict['legend'], ax = self.ax1)
                # Log #-----------------------
                log_str += 'def lighten_color(color, amount=0.5):' + '\n'
                log_str += '    '+'import colorsys' + '\n'
                log_str += '    '+'try:' + '\n'
                log_str += '    '+'    c = mcolors.cnames[color]' + '\n'
                log_str += '    '+'except:' + '\n'
                log_str += '    '+'    c = color' + '\n'
                log_str += '    '+'c = colorsys.rgb_to_hls(*mcolors.to_rgb(c))' + '\n'
                log_str += '    '+'return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])' + '\n' + '\n'
                log_str += 'newpalette = [lighten_color(var,'+str(keyDict['alpha'])+') for var in plt.rcParams[\'axes.prop_cycle\'].by_key()[\'color\']]' + '\n'
                log_str += 'sns.scatterplot(data='+keyDict['data_var_str']+'.replace([np.inf, -np.inf], np.nan), x ="' + str(x_var) + '", y ="' + str(y_var) + '", hue = "' + str(keyDict['cvar']) + '", alpha='+str(keyDict['alpha'])+', palette=newpalette[0:len(pd.unique('+keyDict['data_var_str']+'["' + str(keyDict['cvar']) + '"]))], ax=ax)' + '\n'
                log_str += 'sns.kdeplot(data='+keyDict['data_var_str']+', x = "' + str(x_var) + '", y = "' + str(y_var) + '", hue = "' + str(keyDict['cvar']) + '",legend='+str(keyDict['legend'])+', ax = ax)'+ '\n'
                # ----------------------------
        else:
            if len(data) != 0:
                newpalette = [self.lighten_color(var,keyDict['alpha']) for var in plt.rcParams['axes.prop_cycle'].by_key()['color']]
                sns.scatterplot(x = data[x_var], y = data[y_var], alpha=keyDict['alpha'], palette=newpalette[0], ax=self.ax1)
                sns.kdeplot( x = data[x_var], y = data[y_var], ax = self.ax1 )
                # Log #-----------------------
                log_str += 'def lighten_color(color, amount=0.5):' + '\n'
                log_str += '    '+'import colorsys' + '\n'
                log_str += '    '+'try:' + '\n'
                log_str += '    '+'    c = mcolors.cnames[color]' + '\n'
                log_str += '    '+'except:' + '\n'
                log_str += '    '+'    c = color' + '\n'
                log_str += '    '+'c = colorsys.rgb_to_hls(*mcolors.to_rgb(c))' + '\n'
                log_str += '    '+'return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])' + '\n' + '\n'
                log_str += 'newpalette = [lighten_color(var,'+str(keyDict['alpha'])+') for var in plt.rcParams[\'axes.prop_cycle\'].by_key()[\'color\']]' + '\n'
                log_str += 'sns.scatterplot(x='+keyDict['data_var_str']+'["' + str(x_var) + '"], y='+keyDict['data_var_str']+'["' + str(y_var) + '"], alpha='+str(keyDict['alpha'])+', palette=newpalette[0], ax=ax)' + '\n'
                log_str +=  'sns.kdeplot(x='+keyDict['data_var_str']+'["' + str(x_var) + '"], y='+keyDict['data_var_str']+'["' + str(y_var) + '"], ax = ax)' + '\n'
                # ----------------------------
        return log_str

        
        
        
    def histgram(self,data,x_var,y_var,keyDict,isMultiplePlot=False):
        log_str = ''
        if isMultiplePlot:
            sns.histplot(data.replace([np.inf, -np.inf], np.nan).dropna(),x=x_var,hue=keyDict['cvar'],stat='probability',bins=keyDict['bins_num'],log_scale=keyDict['log_scale'],element="step",legend=keyDict['legend'],ax=self.ax1)
            # Log #-----------------------
            log_str +=  'sns.histplot('+keyDict['data_var_str']+'.replace([np.inf, -np.inf], np.nan).dropna(),x=\''+str(x_var)+'\',hue=\''+str(keyDict['cvar'])+'\',stat=\'probability\', bins = ' + str(keyDict['bins_num']) + ', log_scale='+str(keyDict['log_scale'])+', element=\'step\',legend='+str(keyDict['legend'])+' ,ax = ax)' + '\n'
            # ----------------------------
        else:
            sns.histplot(data[x_var].replace([np.inf, -np.inf], np.nan).dropna(),stat='probability',bins=keyDict['bins_num'],log_scale=keyDict['log_scale'],element="step",legend=False,alpha=keyDict['alpha'],ax=self.ax1)
            # Log #-----------------------
            log_str +=  'sns.histplot('+keyDict['data_var_str']+'["'+str(x_var)+'"].replace([np.inf, -np.inf], np.nan).dropna(),stat=\'probability\', bins = ' + str(keyDict['bins_num']) + ', log_scale='+str(keyDict['log_scale'])+', element=\'step\',legend=False, alpha ='+str(keyDict['alpha'])+',ax = ax )' + '\n'
            # ----------------------------
        return log_str
    
    
    
    
    def lineplot(self,data,x_var,y_var,keyDict,isMultiplePlot=False):
        log_str = ''
        self.ax1.plot(data[x_var].replace([np.inf, -np.inf], np.nan), data[y_var].replace([np.inf, -np.inf], np.nan), linewidth = keyDict['msize'], alpha = keyDict['alpha'], color = keyDict['color'])
        # Log #-----------------------
        log_str +=  'ax.plot('+keyDict['data_var_str']+'["'+str(x_var)+'"].replace([np.inf, -np.inf], np.nan), '+keyDict['data_var_str']+'["'+str(y_var)+'"].replace([np.inf, -np.inf], np.nan), linewidth = '+str(keyDict['msize'])+', alpha ='+str(keyDict['alpha'])+ ', color = "' + str(keyDict['color']) + '" )' + '\n'
        # ----------------------------
        return log_str
    
    
    
    
    def boxplot(self,data,x_var,y_var,keyDict,isMultiplePlot=False):
        log_str = ''
        if isMultiplePlot:
            sns.boxplot(y=y_var, x=x_var, hue = keyDict['cvar'], data=data, ax=self.ax1)
            # Log #-----------------------
            log_str +=  'sns.boxplot( x = "'+str(x_var)+'", y = "'+str(y_var)+'", hue = '+ str(keyDict['cvar'])+',data='+keyDict['data_var_str']+'.replace([np.inf, -np.inf], np.nan).dropna(),ax=ax )' + '\n'
            # ----------------------------
        else:
            
            data_safe = data.replace([np.inf, -np.inf], np.nan).dropna()
            sns.boxplot(y=y_var,x=x_var,data=data_safe,ax=self.ax1)
            # Log #-----------------------
            log_str +=  'sns.boxplot( x = "'+str(x_var)+'", y = "'+str(y_var)+'", data='+keyDict['data_var_str']+'.replace([np.inf, -np.inf], np.nan).dropna(),ax=ax )' + '\n'
            # ----------------------------
        return log_str
    
    
    
    
    def textlog_init(self,isPandas,csv_path=''):
        if isPandas == False:
            log_str = 'style.use(\''+str(self.ui.cmb_style.currentText())+'\')'+'\n'
            log_str += '#- Import CSV as DataFrame ---------- ' + '\n'
            log_str += 'FILE_PATH = \'' + csv_path + '\'' + '\n'
            log_str += 'DATA = pd.read_csv(FILE_PATH)' + '\n'
        elif isPandas == True:
            log_str = '#- DataFrame ---------- ' + '\n'
            log_str += 'DATA = ## Put Your DataFrame Object name here ##  ' + '\n' + '\n'
        log_str += '#- Axes Setting ---------- ' + '\n'
        log_str += 'fig, ax = plt.subplots()' + '\n'
        return log_str
        
        
        
        
    def textlog_dPlot(self,PLOT_TYPE,x_var,y_var,keyDict):
        log_str = ''
        SCATTER,DENSITY,HISTGRAM,LINE,BOXPLOT,ALL_SORT = self.load_magicNum()
        if PLOT_TYPE == BOXPLOT:
            log_str +=   'sns.boxplot( x = "' + str(x_var) + '", y = "' + str(y_var) + '", hue = "' + str(keyDict['cvar']) + '", data ='+keyDict['data_var_str']+'.replace([np.inf, -np.inf], np.nan).dropna(), ax = ax )' + '\n'
        elif PLOT_TYPE == HISTGRAM:
            log_str +=  'sns.histplot('+keyDict['data_var_str']+'.replace([np.inf, -np.inf], np.nan).dropna(),x=\''+str(x_var)+'\',hue=\''+str(keyDict['cvar'])+'\',stat=\'probability\', bins = ' + str(keyDict['bins_num']) + ', log_scale='+str(keyDict['log_scale'])+', element=\'step\',legend='+str(keyDict['legend'])+' ,ax = ax)' + '\n'
        elif PLOT_TYPE == DENSITY:
            log_str += 'def lighten_color(color, amount=0.5):' + '\n'
            log_str += '    '+'import colorsys' + '\n'
            log_str += '    '+'try:' + '\n'
            log_str += '    '+'    c = mcolors.cnames[color]' + '\n'
            log_str += '    '+'except:' + '\n'
            log_str += '    '+'    c = color' + '\n'
            log_str += '    '+'c = colorsys.rgb_to_hls(*mcolors.to_rgb(c))' + '\n'
            log_str += '    '+'return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])' + '\n' + '\n'
            log_str += 'newpalette = [lighten_color(var,'+str(keyDict['alpha'])+') for var in plt.rcParams[\'axes.prop_cycle\'].by_key()[\'color\']]' + '\n'
            log_str += 'sns.scatterplot(data='+keyDict['data_var_str']+'.replace([np.inf, -np.inf], np.nan), x ="' + str(x_var) + '", y ="' + str(y_var) + '", hue = "' + str(keyDict['cvar']) + '", alpha='+str(keyDict['alpha'])+', palette=newpalette[0:len(pd.unique('+keyDict['data_var_str']+'["' + str(keyDict['cvar']) + '"]))], ax=ax)' + '\n'
            log_str += 'sns.kdeplot(data='+keyDict['data_var_str']+', x = "' + str(x_var) + '", y = "' + str(y_var) + '", hue = "' + str(keyDict['cvar']) + '",legend='+str(keyDict['legend'])+', ax = ax)'+ '\n'
        else:
            log_str +=   'groups = '+keyDict['data_var_str']+'.groupby("' + str(keyDict['cvar']) + '")' + '\n'
            log_str +=   'for i, group_zip in enumerate(groups):' + '\n'
            log_str +=   '    ' + 'value, group = group_zip' + '\n'
            if PLOT_TYPE == SCATTER:
                log_str +=   '    ' + 'colors =  plt.rcParams[\'axes.prop_cycle\'].by_key()[\'color\']' + '\n'
                log_str +=   '    ' + 'markers = Line2D.filled_markers' + '\n'
                log_str +=   '    ' + 'c_index = i%len(colors)' + '\n'
                log_str +=   '    ' + 'm_index = i%len(markers)' + '\n'
                log_str +=   '    ' + 'ax.scatter( group["'+ str(x_var) +'"].replace([np.inf, -np.inf], np.nan), group["'+ str(y_var) +'"].replace([np.inf, -np.inf], np.nan), color = colors[c_index], marker = markers[m_index], alpha = '+str(keyDict['alpha'])+', s = '+str(keyDict['msize'])+', label = value)' + '\n'
            elif PLOT_TYPE == LINE:
                log_str +=   '    ' + 'colors =  plt.rcParams[\'axes.prop_cycle\'].by_key()[\'color\']' + '\n'
                log_str +=   '    ' + 'c_index = i%len(colors)' + '\n'
                log_str +=   '    ' + 'ax.plot( group["'+ str(x_var) +'"].replace([np.inf, -np.inf], np.nan), group["'+ str(y_var) +'"].replace([np.inf, -np.inf], np.nan), color = colors[c_index], alpha = '+str(keyDict['alpha'])+', linewidth = '+str(keyDict['msize'])+', label = value )' + '\n'
        return log_str
    
    
    
    def get_pallete(self):
        return (plt.rcParams['axes.prop_cycle'].by_key()['color'], list(Line2D.filled_markers), list(cmocean.cm.cmap_d.keys()) )
    
    
    
    
    def get_setting(self):
        # ( 
        #   name of selected cmap
        #   alpha of plot,
        #   num of bins for histgram,
        #   alpha for histgram 
        #   size of marker
        # )
        return (self.ui.cmb_cmap.currentText(), self.ui.dsb_alpha.value(), self.ui.spb_bins.value(), self.ui.dsb_alpha.value(),self.ui.dsb_markerSize.value() )
    
    
    
    def set_axes(self):
        log_str = ''
        titleText = self.ui.text_title.text()
        SCATTER,DENSITY,HISTGRAM,LINE,BOXPLOT,ALL_SORT = self.load_magicNum()
        if titleText != '':
            self.ax1.set_title(str(titleText))
            # Log #-----------------------
            log_str += 'ax.set_title( "' + str(titleText) + '")' + '\n'
            # ----------------------------
        self.ax1.set_xlabel( self.x_var )
        # Log #-----------------------
        log_str += 'ax.set_xlabel( "' + str(self.x_var) + '")' + '\n'
        # ----------------------------
        if self.PLOT_TYPE != HISTGRAM: 
            self.ax1.set_ylabel( self.y_var )
            # Log #-----------------------
            log_str += 'ax.set_ylabel( "' + str(self.y_var) + '" )' + '\n'
            # ----------------------------
        elif self.PLOT_TYPE == HISTGRAM:
            self.ax1.set_ylabel('Frequency')
            # Log #-----------------------
            log_str += 'ax.set_ylabel( "Frequency" )' + '\n'
            # ----------------------------

        # x axis setting
        if self.PLOT_TYPE != HISTGRAM and self.ui.cb_logx.isChecked(): # Hist
            self.ax1.set_xscale('symlog',linthresh=min(abs(self.data[self.x_var])) )
            # Log #-----------------------
            log_str += 'ax.set_xscale( \'symlog\',linthresh= '+str(min(abs(self.data[self.x_var])))+' )' + '\n'
            # ----------------------------
        if self.x_var in self.NUMERIC_HEADER_LIST:
            xmax = 0
            if self.ui.dsb_xmax.value() < self.ui.dsb_xmin.value():
                xmax = self.ui.dsb_xmin.value()
            else:
                xmax = self.ui.dsb_xmax.value()
            self.ax1.set_xlim( self.ui.dsb_xmin.value() , xmax )
            # Log #-----------------------           
            log_str += 'ax.set_xlim(min(DATA[\'' + str(self.x_var) + '\'].replace([np.inf, -np.inf], np.nan ).dropna() ) - abs( min(DATA[\'' + str(self.x_var) + '\'].replace([np.inf, -np.inf], np.nan ).dropna() )/10), max(DATA[\''+str(self.x_var)+'\'].replace([np.inf, -np.inf], np.nan).dropna()) + abs(max(DATA[\''+str(self.x_var)+'\'].replace([np.inf, -np.inf], np.nan).dropna())/10)  )' + '\n'
            # ----------------------------
        # y axis setting
        if self.PLOT_TYPE != HISTGRAM: # Hist
            if self.ui.cb_logy.isChecked():
                self.ax1.set_yscale('symlog',linthresh=min(abs(self.data[self.y_var])))
                # Log #-----------------------
                log_str += 'ax.set_yscale( \'symlog\',linthresh= '+str(min(abs(self.data[self.y_var])))+' )' + '\n'
                # ----------------------------
        if self.y_var in self.NUMERIC_HEADER_LIST and self.PLOT_TYPE != self.HISTGRAM:
            ymax = 0
            if self.ui.dsb_ymax.value() < self.ui.dsb_ymin.value():
                ymax = self.ui.dsb_ymin.value()
            else:
                ymax = self.ui.dsb_ymax.value()
            self.ax1.set_ylim( self.ui.dsb_ymin.value() , ymax )
            # Log #-----------------------
            log_str += 'ax.set_ylim( min(DATA[\''+str(self.y_var) + '\'].replace([np.inf, -np.inf], np.nan ).dropna() ) - abs( min(DATA[\'' + str(self.y_var) + '\'].replace([np.inf, -np.inf], np.nan ).dropna() )/10), max(DATA[\''+str(self.y_var)+'\'].replace([np.inf, -np.inf], np.nan).dropna()) + abs(max(DATA[\''+str(self.y_var)+'\'].replace([np.inf, -np.inf], np.nan).dropna())/10)  )' + '\n'
            # ----------------------------
        return log_str
    
    
    def graphDraw_nonNumeric_Syntax(self):
        # Syntax Coloring Setting #--------------------------
        
        # Log #-----------------------
        File_log_str = self.textlog_init(self.isPandas,self.CSV_PATH)
        # ----------------------------

        #- plot initial setting -------------------------------------
        ALL_SORT = 0
        colors, markers, cmap_list = self.get_pallete()
        cmap, alpha, bins_num, hist_alpha, marker_size = self.get_setting()
        SCATTER,DENSITY,HISTGRAM,LINE,BOXPLOT,ALL_SORT = self.load_magicNum()
        isNumeric = self.isNumericMode
        keyDict = {'alpha':alpha,
                   'bins_num':bins_num,
                   'hist_alpha':hist_alpha,
                   'color':colors[0],
                   'marker':markers[0],
                   'label':'',
                   'cmap':cmap,
                   'clen':len( colors ),
                   'mlen':len( markers ),
                   'cmaplen':len( cmap_list ),
                   'msize':marker_size,
                   'edgecolor':'black',
                   'edge_width':0,
                   'data_var_str':'DATA',
                   'legend':self.ui.cb_legend.isChecked(),
                   'log_scale': self.ui.cb_logx.isChecked(),
                   'logc':self.ui.cb_logc.isChecked()
                  }
        
        self.fig.clf()
        self.ax1.clear()
        self.ax1 = self.fig.add_subplot(111)
        File_log_str += self.set_axes()
        #========================================================
        # DATA PLOT
        #========================================================
        File_log_str += '#- PLOT ------------------ ' + '\n'
        if self.color_var == "None_": # simple plot (scatter)
            keyDict['label'] = ''
            if self.PLOT_TYPE == SCATTER:
                File_log_str += self.scatterplot(self.csv,self.x_var,self.y_var,keyDict,withColorbar=False)
            elif self.PLOT_TYPE == DENSITY: #density
                File_log_str += self.densityplot(self.csv,self.x_var,self.y_var,keyDict,isMultiplePlot=False)
            elif self.PLOT_TYPE == HISTGRAM: #Histgoram
                File_log_str += self.histgram(self.csv,self.x_var,self.y_var,keyDict,isMultiplePlot=False)
            elif self.PLOT_TYPE == LINE: # line
                File_log_str += self.lineplot(self.csv,self.x_var,self.y_var,keyDict,isMultiplePlot=False)
            elif self.PLOT_TYPE == BOXPLOT:
                File_log_str += self.boxplot(self.csv,self.x_var,self.y_var,keyDict,isMultiplePlot=False)
        else: # When the first category is selected
            if self.ui.cmb_sort.currentIndex() == ALL_SORT: # use discrete colors and plot all
                keyDict['cvar'] = self.color_var
                if self.PLOT_TYPE == BOXPLOT:
                    self.boxplot(self.data,self.x_var,self.y_var,keyDict,isMultiplePlot=True)
                elif self.PLOT_TYPE == HISTGRAM:
                    self.histgram(self.data,self.x_var,self.y_var,keyDict,isMultiplePlot=True)
                elif self.PLOT_TYPE == DENSITY: #density
                    self.densityplot(self.data,self.x_var,self.y_var,keyDict,isMultiplePlot=True)
                else:
                    for i, value in enumerate(pd.unique(self.data[self.color_var])):
                        keyDict['color'] = colors[i%keyDict['clen']]
                        keyDict['marker'] = markers[i%keyDict['mlen']]
                        keyDict['label'] = value
                        data = self.data.loc[ self.data[self.color_var] == value ]
                        if self.PLOT_TYPE == SCATTER:
                            self.scatterplot(data,self.x_var,self.y_var,keyDict,withColorbar=False)
#                         elif self.PLOT_TYPE == DENSITY: #density
#                             self.densityplot(data,self.x_var,self.y_var,keyDict,isMultiplePlot=True)
#                         elif self.PLOT_TYPE == HISTGRAM: #Histgoram
#                             self.histgram(data,self.x_var,self.y_var,keyDict,isMultiplePlot=True)
                        elif self.PLOT_TYPE == LINE: # line
                            self.lineplot(data,self.x_var,self.y_var,keyDict,isMultiplePlot=True)
                File_log_str += self.textlog_dPlot(self.PLOT_TYPE,self.x_var,self.y_var,keyDict)
            else:  # Sorting by specific value
                value = pd.unique(self.csv[self.color_var])[self.ui.cmb_sort.currentIndex() - 1] 
                # data = self.csv.loc[ self.csv[self.color_var] == pd.unique(self.csv[self.color_var])[value] ]
                # Log #-----------------------
                if isNumeric:
                    File_log_str +=  'sub_data = DATA.loc[ DATA["' + str(self.color_var) + '"] == '+str(value)+']' + '\n'
                    print('# Numeric plot is happening in Non-numeric-syntax function! Check source')
                else:
                    File_log_str +=  'sub_data = DATA.loc[ DATA["' + str(self.color_var) + '"] == "'+str(value)+'"]' + '\n'
                keyDict['data_var_str'] = 'sub_data'
                # ----------------------------
                if self.subcolor_var == 'None_': 
                    # scatter graph
                    if self.PLOT_TYPE == SCATTER:
                        File_log_str += self.scatterplot(self.data,self.x_var,self.y_var,keyDict,withColorbar=False)
                    elif self.PLOT_TYPE == DENSITY: #density
                        File_log_str += self.densityplot(self.data,self.x_var,self.y_var,keyDict,isMultiplePlot=False)
                    elif self.PLOT_TYPE == HISTGRAM: #Histgoram
                        File_log_str += self.histgram(self.data,self.x_var,self.y_var,keyDict,isMultiplePlot=False)
                    elif self.PLOT_TYPE == LINE: # line
                        File_log_str += self.lineplot(self.data,self.x_var,self.y_var,keyDict,isMultiplePlot=False)
                    elif self.PLOT_TYPE == BOXPLOT:
                        File_log_str += self.boxplot(self.data,self.x_var,self.y_var,keyDict,isMultiplePlot=False)
                else: # When the second category is selected
                    if self.ui.cmb_subsort.currentIndex() == ALL_SORT: # use discrete colors and plot all
                        keyDict['cvar'] = self.subcolor_var
                        if self.PLOT_TYPE == BOXPLOT:
                            self.boxplot(data,self.x_var,self.y_var,keyDict,isMultiplePlot=True)
                        elif self.PLOT_TYPE == DENSITY: #density
                            self.densityplot(self.data,self.x_var,self.y_var,keyDict,isMultiplePlot=True)
                        elif self.PLOT_TYPE == HISTGRAM: #Histgoram
                            self.histgram(self.data,self.x_var,self.y_var,keyDict,isMultiplePlot=True)
                        else:
                            for i, value in enumerate(pd.unique(self.data[self.subcolor_var])):
                                keyDict['color'] = colors[i%keyDict['clen']]
                                keyDict['marker'] = markers[i%keyDict['mlen']]
                                keyDict['label'] = value
                                data = self.data.loc[ self.data[self.subcolor_var] == value ]
                                if self.PLOT_TYPE == SCATTER:
                                    self.scatterplot(data,self.x_var,self.y_var,keyDict,withColorbar=False)
#                                 elif self.PLOT_TYPE == DENSITY: #density
#                                     self.densityplot(data,self.x_var,self.y_var,keyDict,isMultiplePlot=True)
#                                 elif self.PLOT_TYPE == HISTGRAM: #Histgoram
#                                     self.histgram(data,self.x_var,self.y_var,keyDict,isMultiplePlot=True)
                                elif self.PLOT_TYPE == LINE: # line
                                    self.lineplot(data,self.x_var,self.y_var,keyDict,isMultiplePlot=True)
                        File_log_str += self.textlog_dPlot(self.PLOT_TYPE,self.x_var,self.y_var,keyDict)
                    else:
                        value2 =pd.unique(self.csv[self.subcolor_var])[ self.ui.cmb_subsort.currentIndex() - 1 ]
                        # data2 = data.loc[ data[ self.subcolor_var ] == pd.unique(self.csv[self.subcolor_var])[value2] ]
                        # Log #-----------------------
                        if isNumeric:
                            File_log_str +=  'subsub_data = sub_data.loc[ sub_data["' + str(self.subcolor_var) + '"] == '+str(value2)+']' + '\n'
                        else:
                            File_log_str +=  'subsub_data = sub_data.loc[ sub_data["' + str(self.subcolor_var) + '"] == "'+str(value2)+'"]' + '\n'
                        keyDict['data_var_str'] = 'subsub_data'
                        # ----------------------------
                        if self.subsubcolor_var == 'None_':
                            if self.PLOT_TYPE == SCATTER:
                                File_log_str += self.scatterplot(self.data,self.x_var,self.y_var,keyDict,withColorbar=False)
                            elif self.PLOT_TYPE == DENSITY: #density
                                File_log_str += self.densityplot(self.data,self.x_var,self.y_var,keyDict,isMultiplePlot=False)
                            elif self.PLOT_TYPE == HISTGRAM: #Histgoram
                                File_log_str += self.histgram(self.data,self.x_var,self.y_var,keyDict,isMultiplePlot=False)
                            elif self.PLOT_TYPE == LINE: # line
                                File_log_str += self.lineplot(self.data,self.x_var,self.y_var,keyDict,isMultiplePlot=False)
                            elif self.PLOT_TYPE == BOXPLOT:
                                File_log_str += self.boxplot(self.data,self.x_var,self.y_var,keyDict,isMultiplePlot=False)
                        else:  # When the third category is selected
                            if self.ui.cmb_subsubsort.currentIndex() == ALL_SORT: # use discrete colors and plot all
                                keyDict['cvar'] = self.subsubcolor_var
                                if self.PLOT_TYPE == BOXPLOT:
                                    self.boxplot(self.data,self.x_var,self.y_var,keyDict,isMultiplePlot=True)
                                elif self.PLOT_TYPE == DENSITY: #density
                                    self.densityplot(self.data,self.x_var,self.y_var,keyDict,isMultiplePlot=True)
                                elif self.PLOT_TYPE == HISTGRAM: #Histgoram
                                    self.histgram(self.data,self.x_var,self.y_var,keyDict,isMultiplePlot=True)
                                else:
                                    for i, value in enumerate(pd.unique(self.data[self.subsubcolor_var])):
                                        keyDict['color'] = colors[i%keyDict['clen']]
                                        keyDict['marker'] = markers[i%keyDict['mlen']]
                                        keyDict['label'] = value
                                        data = self.data.loc[ self.data[self.subsubcolor_var] == value ]
                                        if self.PLOT_TYPE == SCATTER: # Scatter
                                            self.scatterplot(data,self.x_var,self.y_var,keyDict,withColorbar=False)
#                                         elif self.PLOT_TYPE == DENSITY: #density
#                                             self.densityplot(data,self.x_var,self.y_var,keyDict,isMultiplePlot=True)
#                                         elif self.PLOT_TYPE == HISTGRAM: #Histgoram
#                                             self.histgram(data,self.x_var,self.y_var,keyDict,isMultiplePlot=True)
                                        elif self.PLOT_TYPE == LINE: # line
                                            self.lineplot(data,self.x_var,self.y_var,keyDict,isMultiplePlot=True)
                                File_log_str += self.textlog_dPlot(self.PLOT_TYPE,self.x_var,self.y_var,keyDict)
                            else:
                                value3 =pd.unique(self.csv[self.subsubcolor_var])[ self.ui.cmb_subsubsort.currentIndex() - 1 ]
                                # data2 = data.loc[ data[ self.subcolor_var ] == pd.unique(self.csv[self.subcolor_var])[value2] ]
                                # Log #-----------------------
                                if isNumeric:
                                    File_log_str +=  'subsubsub_data = subsub_data.loc[ subsub_data["' + str(self.subsubcolor_var) + '"] == '+str(value3)+']' + '\n'
                                else:
                                    File_log_str +=  'subsubsub_data = subsub_data.loc[ subsub_data["' + str(self.subsubcolor_var) + '"] == "'+str(value3)+'"]' + '\n'
                                keyDict['data_var_str'] = 'subsubsub_data'
                                # ----------------------------
                                if self.PLOT_TYPE == SCATTER:
                                    File_log_str += self.scatterplot(self.data,self.x_var,self.y_var,keyDict,withColorbar=False)
                                elif self.PLOT_TYPE == DENSITY: #density
                                    File_log_str += self.densityplot(self.data,self.x_var,self.y_var,keyDict,isMultiplePlot=False)
                                elif self.PLOT_TYPE == HISTGRAM: #Histgoram
                                    File_log_str += self.histgram(self.data,self.x_var,self.y_var,keyDict,isMultiplePlot=False)
                                elif self.PLOT_TYPE == LINE: # line
                                    File_log_str += self.lineplot(self.data,self.x_var,self.y_var,keyDict,isMultiplePlot=False)
                                elif self.PLOT_TYPE == BOXPLOT:
                                    File_log_str += self.boxplot(self.data,self.x_var,self.y_var,keyDict,isMultiplePlot=False)
        if self.PLOT_TYPE == HISTGRAM or self.PLOT_TYPE == DENSITY :
            pass
        else:
            if self.ui.cb_legend.isChecked():
                self.ax1.legend()
                self.ax1.legend().set_visible(True)
            else:
                self.ax1.legend().set_visible(False)
        self.fig.canvas.draw_idle()
        self.ui.tab_pca.setCurrentIndex(2)
        # Log #-----------------------
        File_log_str +=  'plt.show()' + '\n'
        File_log_str +=  'plt.close()' + '\n'
        # ----------------------------
        self.onStringChanged(File_log_str)


        
    def graphDraw_Numeric_Syntax(self):
        # Syntax Coloring Setting #--------------------------

        # Log #-----------------------
        File_log_str = self.textlog_init(self.isPandas,self.CSV_PATH)
        # ----------------------------

        #- plot initial setting -------------------------------------
        colors, markers, cmap_list = self.get_pallete()
        cmap, alpha, bins_num, hist_alpha, marker_size = self.get_setting()
        SCATTER,DENSITY,HISTGRAM,LINE,BOXPLOT,ALL_SORT = self.load_magicNum()
        isNumeric = self.isNumericMode
        keyDict = {'alpha':alpha,
                   'bins_num':bins_num,
                   'hist_alpha':hist_alpha,
                   'color':colors[0],
                   'marker':markers[0],
                   'label':'',
                   'cmap':cmap,
                   'clen':len( colors ),
                   'mlen':len( markers ),
                   'cmaplen':len( cmap_list ),
                   'msize':marker_size,
                   'edgecolor':'black',
                   'edge_width':0,
                   'data_var_str':'DATA',
                   'legend': self.ui.cb_legend.isChecked(),
                   'log_scale': self.ui.cb_logx.isChecked(),
                   'logc':self.ui.cb_logc.isChecked()
                  }
        self.fig.clf()
        self.ax1.clear()
        self.ax1 = self.fig.add_subplot(111)
        File_log_str += self.set_axes()
            
        #========================================================
        # DATA PLOT
        #========================================================
        File_log_str += '#- PLOT ------------------ ' + '\n'
        if self.color_var == "None_": # simple plot (scatter)
            keyDict['label'] = ''
            if self.PLOT_TYPE == SCATTER:
                File_log_str += self.scatterplot(self.csv,self.x_var,self.y_var,keyDict,withColorbar=False)
            elif self.PLOT_TYPE == DENSITY: #density
                File_log_str += self.densityplot(self.csv,self.x_var,self.y_var,keyDict,isMultiplePlot=False)
            elif self.PLOT_TYPE == HISTGRAM: #Histgoram
                File_log_str += self.histgram(self.csv,self.x_var,self.y_var,keyDict,isMultiplePlot=False)
            elif self.PLOT_TYPE == LINE: # line
                File_log_str += self.lineplot(self.csv,self.x_var,self.y_var,keyDict,isMultiplePlot=False)
            elif self.PLOT_TYPE == BOXPLOT:
                File_log_str += self.boxplot(self.csv,self.x_var,self.y_var,keyDict,isMultiplePlot=False)
        elif self.subcolor_var == 'None_':
            if self.ui.cmb_color.currentText() in self.NUMERIC_HEADER_LIST:
                if self.PLOT_TYPE == SCATTER:
                    keyDict['cvar'] = self.color_var
                    keyDict['vmin'] = self.ui.dsb_cmin.value()
                    keyDict['vmax'] = self.ui.dsb_cmax.value()
                    keyDict['label'] = ''
                    File_log_str += self.scatterplot(self.csv,self.x_var,self.y_var,keyDict,withColorbar=True)
        elif self.subsubcolor_var == 'None_':
            value = pd.unique(self.csv[self.color_var])[ self.ui.cmb_sort.currentIndex() - 1]
            keyDict['data_var_str'] = 'sub_data'
            # Log #-----------------------
            if isNumeric:
                File_log_str +=  'sub_data = DATA.loc[ DATA["' + str(self.color_var) + '"] == '+str(value)+']' + '\n'
            else:
                File_log_str +=  'sub_data = DATA.loc[ DATA["' + str(self.color_var) + '"] == "'+str(value)+'"]' + '\n'
            # ----------------------------
            if self.ui.cmb_subcolor.currentText() in self.NUMERIC_HEADER_LIST:
                if self.PLOT_TYPE == SCATTER:
                    keyDict['cvar'] = self.subcolor_var
                    keyDict['vmin'] = self.ui.dsb_cmin.value()
                    keyDict['vmax'] = self.ui.dsb_cmax.value()
                    keyDict['label'] = ''
                    File_log_str += self.scatterplot(self.data,self.x_var,self.y_var,keyDict,withColorbar=True)
        elif self.subsubcolor_var != 'None_':
            value = pd.unique(self.csv[self.color_var])[ self.ui.cmb_sort.currentIndex() - 1]
            # Log #-----------------------
            if isNumeric:
                File_log_str +=  'sub_data = DATA.loc[ DATA["' + str(self.color_var) + '"] == '+str(value)+']' + '\n'
            else:
                File_log_str +=  'sub_data = DATA.loc[ DATA["' + str(self.color_var) + '"] == "'+str(value)+'"]' + '\n'
            # ----------------------------
            value2 = pd.unique(self.csv[self.subcolor_var])[ self.ui.cmb_subsort.currentIndex() - 1 ]
            keyDict['data_var_str'] = 'subsub_data'
            # Log #-----------------------
            if isNumeric:
                File_log_str +=  'subsub_data = sub_data.loc[ sub_data["' + str(self.subcolor_var) + '"] == '+str(value2)+']' + '\n'
            else:
                File_log_str +=  'subsub_data = sub_data.loc[ sub_data["' + str(self.subcolor_var) + '"] == "'+str(value2)+'"]' + '\n'
            # ----------------------------
            if self.ui.cmb_subsubcolor.currentText() in self.NUMERIC_HEADER_LIST:
                if self.PLOT_TYPE == SCATTER:
                    keyDict['cvar'] = self.subsubcolor_var
                    keyDict['vmin'] = self.ui.dsb_cmin.value()
                    keyDict['vmax'] = self.ui.dsb_cmax.value()
                    keyDict['label'] = ''
                    File_log_str += self.scatterplot(self.data,self.x_var,self.y_var,keyDict,withColorbar=True)
        if self.PLOT_TYPE == HISTGRAM or self.PLOT_TYPE == DENSITY:
            pass
        else:
            self.ax1.legend()
            if self.ui.cb_legend.isChecked():
                self.ax1.legend().set_visible(True)
            else:
                self.ax1.legend().set_visible(False)
        self.fig.canvas.draw_idle()
        self.ui.tab_pca.setCurrentIndex(2)
        # Log #-----------------------
        File_log_str +=  'plt.show()' + '\n'
        File_log_str +=  'plt.close()' + '\n'
        # ----------------------------
        self.onStringChanged(File_log_str)


    def saveFigure(self):
        file_name, _ = Qw.QFileDialog.getSaveFileName(self)
        if len(file_name)==0:
            return
        file_name = str(Path(file_name).with_suffix(".pdf"))
        self.fig.savefig(file_name,bbox_inches='tight')


def generate_cmap(colors):
    """Return original color maps"""
    values = range(len(colors))
    vmax = np.ceil(np.max(values))
    color_list = []
    for v, c in zip(values, colors):
        color_list.append( ( v/ vmax, c) )
    return LinearSegmentedColormap.from_list('custom_cmap', color_list)

def kde2dgraphfill(ax,x,y,xmin,xmax,ymin,ymax):
    # Peform the kernel density estimate
    xx, yy = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    positions = np.vstack([xx.ravel(), yy.ravel()])
    values = np.vstack([x, y])
    noise_param = 1.0
    try:
        kernel = st.gaussian_kde(values)
    except np.linalg.linalg.LinAlgError:
        row = len(x)
        mean_x = np.mean(x)
        mean_y = np.mean(y)
        dev_x = np.std(x)
        dev_y = np.std(y)
        noise_param = mean_y + mean_x + dev_y + dev_x
        if noise_param == 0:
            noise_param = 1
        elif noise_param > 1:
            # noise_param = 1.0 / noise_param
            noise_param = noise_param / 2
        elif noise_param < 0:
            noise_param = -1*noise_param
        else:
            noise_param = noise_param
        ####################
        # CHECK HERE !!!!!!!
        ####################
        rd_array = np.random.rand(row) * noise_param * 1/1000
        x_dash = x + rd_array
        values = np.vstack([x_dash, y])
        kernel = st.gaussian_kde(values)
    # kernel = st.gaussian_kde(values)
    f = np.reshape(kernel(positions).T, xx.shape)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    # cm = generate_cmap(['aqua', 'lawngreen', 'yellow', 'coral'])
    # cm = generate_cmap(['ghostwhite', 'deepskyblue', 'mediumblue', 'darkblue'])
    cfset = ax.contourf(xx, yy, f, cmap=plt.cm.jet)
    cfset = ax.contourf(xx, yy, f, cmap="jet")
    # cfset = ax.contourf(xx, yy, f, cmap=cm)
    cset = ax.contour(xx, yy, f, colors='k')
    return cfset
    
def kde2dgraph(ax,x,y,xmin,xmax,ymin,ymax,cmap):
    # Peform the kernel density estimate
    xx, yy = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    positions = np.vstack([xx.ravel(), yy.ravel()])
    values = np.vstack([x, y])
    noise_param = 1.0
    try:
        kernel = st.gaussian_kde(values)
    except np.linalg.linalg.LinAlgError:
        row = len(x)
        mean_x = np.mean(x)
        mean_y = np.mean(y)
        dev_x = np.std(x)
        dev_y = np.std(y)
        noise_param = mean_y + mean_x + dev_y + dev_x
        if noise_param == 0:
            noise_param = 1
        elif noise_param > 1:
            # noise_param = 1.0 / noise_param
            noise_param = noise_param / 2
        elif noise_param < 0:
            noise_param = -1*noise_param
        else:
            noise_param = noise_param
        rd_array = np.random.rand(row) * noise_param * 1/1000
        x_dash = x + rd_array
        values = np.vstack([x_dash, y])
        kernel = st.gaussian_kde(values) 
    # except ValueError:
        # return "valueError"

    # kernel = st.gaussian_kde(values)
    f = np.reshape(kernel(positions).T, xx.shape)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    # cfset = ax.contourf(xx, yy, f, cmap=cmap)
    cset = ax.contour(xx, yy, f, cmap=cmap)
    return cset

def buildGUI(data = 'None'):
    app = Qw.QApplication(sys.argv)         
    wmain = Csviwer()
    wmain.show()
    if type(data) == pd.core.frame.DataFrame:
        wmain.loadData(data)
    elif isinstance(data,str) and data != 'None':
        wmain.loadData(data)
    sys.exit(app.exec())

if __name__ == '__main__':
    buildGUI()