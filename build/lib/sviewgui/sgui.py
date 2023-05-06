# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sgui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(946, 806)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setMinimumSize(QtCore.QSize(240, 0))
        self.scrollArea.setMaximumSize(QtCore.QSize(350, 16777215))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 331, 845))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.frame_graph = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.frame_graph.setEnabled(False)
        self.frame_graph.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_graph.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_graph.setObjectName("frame_graph")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.frame_graph)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_6 = QtWidgets.QLabel(self.frame_graph)
        self.label_6.setObjectName("label_6")
        self.gridLayout_6.addWidget(self.label_6, 2, 0, 1, 1)
        self.cmb_y = QtWidgets.QComboBox(self.frame_graph)
        self.cmb_y.setObjectName("cmb_y")
        self.gridLayout_6.addWidget(self.cmb_y, 8, 2, 1, 1)
        self.cmb_cmap = QtWidgets.QComboBox(self.frame_graph)
        self.cmb_cmap.setObjectName("cmb_cmap")
        self.gridLayout_6.addWidget(self.cmb_cmap, 14, 2, 1, 1)
        self.dsb_cmin = QtWidgets.QDoubleSpinBox(self.frame_graph)
        self.dsb_cmin.setObjectName("dsb_cmin")
        self.gridLayout_6.addWidget(self.dsb_cmin, 17, 0, 1, 1)
        self.cmb_x = QtWidgets.QComboBox(self.frame_graph)
        self.cmb_x.setObjectName("cmb_x")
        self.gridLayout_6.addWidget(self.cmb_x, 5, 2, 1, 1)
        self.cmb_subsubcolor = QtWidgets.QComboBox(self.frame_graph)
        self.cmb_subsubcolor.setObjectName("cmb_subsubcolor")
        self.gridLayout_6.addWidget(self.cmb_subsubcolor, 26, 1, 1, 2)
        self.cmb_subsubsort = QtWidgets.QComboBox(self.frame_graph)
        self.cmb_subsubsort.setObjectName("cmb_subsubsort")
        self.gridLayout_6.addWidget(self.cmb_subsubsort, 27, 1, 1, 2)
        self.cb_logy = QtWidgets.QCheckBox(self.frame_graph)
        self.cb_logy.setObjectName("cb_logy")
        self.gridLayout_6.addWidget(self.cb_logy, 8, 1, 1, 1)
        self.dsb_xmax = QtWidgets.QDoubleSpinBox(self.frame_graph)
        self.dsb_xmax.setDecimals(5)
        self.dsb_xmax.setObjectName("dsb_xmax")
        self.gridLayout_6.addWidget(self.dsb_xmax, 7, 2, 1, 1)
        self.cmb_subcolor = QtWidgets.QComboBox(self.frame_graph)
        self.cmb_subcolor.setObjectName("cmb_subcolor")
        self.gridLayout_6.addWidget(self.cmb_subcolor, 22, 1, 1, 2)
        self.cmb_color = QtWidgets.QComboBox(self.frame_graph)
        self.cmb_color.setObjectName("cmb_color")
        self.gridLayout_6.addWidget(self.cmb_color, 19, 1, 1, 2)
        self.label_18 = QtWidgets.QLabel(self.frame_graph)
        self.label_18.setObjectName("label_18")
        self.gridLayout_6.addWidget(self.label_18, 5, 0, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.frame_graph)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")
        self.gridLayout_6.addWidget(self.label_22, 0, 0, 1, 3)
        self.label_19 = QtWidgets.QLabel(self.frame_graph)
        self.label_19.setObjectName("label_19")
        self.gridLayout_6.addWidget(self.label_19, 8, 0, 1, 1)
        self.label_28 = QtWidgets.QLabel(self.frame_graph)
        self.label_28.setObjectName("label_28")
        self.gridLayout_6.addWidget(self.label_28, 22, 0, 1, 1)
        self.label_24 = QtWidgets.QLabel(self.frame_graph)
        self.label_24.setObjectName("label_24")
        self.gridLayout_6.addWidget(self.label_24, 3, 0, 1, 1)
        self.dsb_ymax = QtWidgets.QDoubleSpinBox(self.frame_graph)
        self.dsb_ymax.setDecimals(5)
        self.dsb_ymax.setObjectName("dsb_ymax")
        self.gridLayout_6.addWidget(self.dsb_ymax, 9, 2, 1, 1)
        self.cb_legend = QtWidgets.QCheckBox(self.frame_graph)
        self.cb_legend.setObjectName("cb_legend")
        self.gridLayout_6.addWidget(self.cb_legend, 28, 0, 1, 1)
        self.cmb_sort = QtWidgets.QComboBox(self.frame_graph)
        self.cmb_sort.setObjectName("cmb_sort")
        self.gridLayout_6.addWidget(self.cmb_sort, 20, 1, 1, 2)
        self.label_bins = QtWidgets.QLabel(self.frame_graph)
        self.label_bins.setObjectName("label_bins")
        self.gridLayout_6.addWidget(self.label_bins, 12, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.frame_graph)
        self.label.setObjectName("label")
        self.gridLayout_6.addWidget(self.label, 14, 0, 1, 1)
        self.cb_logc = QtWidgets.QCheckBox(self.frame_graph)
        self.cb_logc.setObjectName("cb_logc")
        self.gridLayout_6.addWidget(self.cb_logc, 14, 1, 1, 1)
        self.dsb_cmax = QtWidgets.QDoubleSpinBox(self.frame_graph)
        self.dsb_cmax.setObjectName("dsb_cmax")
        self.gridLayout_6.addWidget(self.dsb_cmax, 17, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame_graph)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout_6.addWidget(self.label_5, 17, 1, 1, 1)
        self.label_29 = QtWidgets.QLabel(self.frame_graph)
        self.label_29.setObjectName("label_29")
        self.gridLayout_6.addWidget(self.label_29, 26, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame_graph)
        self.label_2.setObjectName("label_2")
        self.gridLayout_6.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.frame_graph)
        self.label_20.setObjectName("label_20")
        self.gridLayout_6.addWidget(self.label_20, 19, 0, 1, 1)
        self.cmb_plot = QtWidgets.QComboBox(self.frame_graph)
        self.cmb_plot.setObjectName("cmb_plot")
        self.cmb_plot.addItem("")
        self.cmb_plot.addItem("")
        self.cmb_plot.addItem("")
        self.cmb_plot.addItem("")
        self.cmb_plot.addItem("")
        self.gridLayout_6.addWidget(self.cmb_plot, 3, 1, 1, 2)
        self.dsb_xmin = QtWidgets.QDoubleSpinBox(self.frame_graph)
        self.dsb_xmin.setDecimals(5)
        self.dsb_xmin.setObjectName("dsb_xmin")
        self.gridLayout_6.addWidget(self.dsb_xmin, 7, 0, 1, 1)
        self.label_30 = QtWidgets.QLabel(self.frame_graph)
        self.label_30.setObjectName("label_30")
        self.gridLayout_6.addWidget(self.label_30, 13, 0, 1, 1)
        self.text_title = QtWidgets.QLineEdit(self.frame_graph)
        self.text_title.setObjectName("text_title")
        self.gridLayout_6.addWidget(self.text_title, 1, 1, 1, 2)
        self.cmb_subsort = QtWidgets.QComboBox(self.frame_graph)
        self.cmb_subsort.setObjectName("cmb_subsort")
        self.gridLayout_6.addWidget(self.cmb_subsort, 24, 1, 1, 2)
        self.button_save = QtWidgets.QPushButton(self.frame_graph)
        self.button_save.setObjectName("button_save")
        self.gridLayout_6.addWidget(self.button_save, 30, 0, 1, 3)
        self.label_3 = QtWidgets.QLabel(self.frame_graph)
        self.label_3.setObjectName("label_3")
        self.gridLayout_6.addWidget(self.label_3, 7, 1, 1, 1)
        self.cb_subcolorbar = QtWidgets.QCheckBox(self.frame_graph)
        self.cb_subcolorbar.setObjectName("cb_subcolorbar")
        self.gridLayout_6.addWidget(self.cb_subcolorbar, 24, 0, 1, 1)
        self.cb_subsubcolorbar = QtWidgets.QCheckBox(self.frame_graph)
        self.cb_subsubcolorbar.setObjectName("cb_subsubcolorbar")
        self.gridLayout_6.addWidget(self.cb_subsubcolorbar, 27, 0, 1, 1)
        self.cb_colorbar = QtWidgets.QCheckBox(self.frame_graph)
        self.cb_colorbar.setObjectName("cb_colorbar")
        self.gridLayout_6.addWidget(self.cb_colorbar, 20, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.frame_graph)
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout_6.addWidget(self.label_7, 18, 0, 1, 3)
        self.label_21 = QtWidgets.QLabel(self.frame_graph)
        self.label_21.setObjectName("label_21")
        self.gridLayout_6.addWidget(self.label_21, 11, 0, 1, 1)
        self.dsb_markerSize = QtWidgets.QDoubleSpinBox(self.frame_graph)
        self.dsb_markerSize.setMinimum(0.1)
        self.dsb_markerSize.setMaximum(30.0)
        self.dsb_markerSize.setSingleStep(0.1)
        self.dsb_markerSize.setProperty("value", 5.0)
        self.dsb_markerSize.setObjectName("dsb_markerSize")
        self.gridLayout_6.addWidget(self.dsb_markerSize, 11, 1, 1, 2)
        self.spb_bins = QtWidgets.QSpinBox(self.frame_graph)
        self.spb_bins.setMinimum(1)
        self.spb_bins.setMaximum(200)
        self.spb_bins.setProperty("value", 10)
        self.spb_bins.setObjectName("spb_bins")
        self.gridLayout_6.addWidget(self.spb_bins, 12, 1, 1, 2)
        self.dsb_alpha = QtWidgets.QDoubleSpinBox(self.frame_graph)
        self.dsb_alpha.setDecimals(1)
        self.dsb_alpha.setMinimum(0.1)
        self.dsb_alpha.setMaximum(1.0)
        self.dsb_alpha.setSingleStep(0.1)
        self.dsb_alpha.setProperty("value", 1.0)
        self.dsb_alpha.setObjectName("dsb_alpha")
        self.gridLayout_6.addWidget(self.dsb_alpha, 13, 1, 1, 2)
        self.button_preview = QtWidgets.QPushButton(self.frame_graph)
        self.button_preview.setObjectName("button_preview")
        self.gridLayout_6.addWidget(self.button_preview, 28, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frame_graph)
        self.label_4.setObjectName("label_4")
        self.gridLayout_6.addWidget(self.label_4, 9, 1, 1, 1)
        self.dsb_ymin = QtWidgets.QDoubleSpinBox(self.frame_graph)
        self.dsb_ymin.setDecimals(5)
        self.dsb_ymin.setObjectName("dsb_ymin")
        self.gridLayout_6.addWidget(self.dsb_ymin, 9, 0, 1, 1)
        self.cb_logx = QtWidgets.QCheckBox(self.frame_graph)
        self.cb_logx.setObjectName("cb_logx")
        self.gridLayout_6.addWidget(self.cb_logx, 5, 1, 1, 1)
        self.cmb_style = QtWidgets.QComboBox(self.frame_graph)
        self.cmb_style.setObjectName("cmb_style")
        self.cmb_style.addItem("")
        self.gridLayout_6.addWidget(self.cmb_style, 2, 1, 1, 2)
        self.gridLayout_5.addWidget(self.frame_graph, 1, 1, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.tab_pca = QtWidgets.QTabWidget(self.centralwidget)
        self.tab_pca.setTabPosition(QtWidgets.QTabWidget.North)
        self.tab_pca.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tab_pca.setObjectName("tab_pca")
        self.tn_summary = QtWidgets.QWidget()
        self.tn_summary.setObjectName("tn_summary")
        self.gridLayout = QtWidgets.QGridLayout(self.tn_summary)
        self.gridLayout.setObjectName("gridLayout")
        self.button_csvPath = QtWidgets.QPushButton(self.tn_summary)
        self.button_csvPath.setObjectName("button_csvPath")
        self.gridLayout.addWidget(self.button_csvPath, 0, 1, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.tn_summary)
        self.label_16.setObjectName("label_16")
        self.gridLayout.addWidget(self.label_16, 3, 0, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.tn_summary)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 0, 0, 1, 1)
        self.table_summary = QtWidgets.QTableView(self.tn_summary)
        self.table_summary.setObjectName("table_summary")
        self.gridLayout.addWidget(self.table_summary, 2, 0, 1, 2)
        self.table_sorted = QtWidgets.QTableView(self.tn_summary)
        self.table_sorted.setObjectName("table_sorted")
        self.gridLayout.addWidget(self.table_sorted, 4, 0, 1, 2)
        self.textbox_csvPath = QtWidgets.QLineEdit(self.tn_summary)
        self.textbox_csvPath.setObjectName("textbox_csvPath")
        self.gridLayout.addWidget(self.textbox_csvPath, 1, 0, 1, 2)
        self.tab_pca.addTab(self.tn_summary, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.tab_4)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.logbox = QtWidgets.QTextEdit(self.tab_4)
        self.logbox.setObjectName("logbox")
        self.gridLayout_12.addWidget(self.logbox, 0, 0, 1, 1)
        self.tab_pca.addTab(self.tab_4, "")
        self.tn_graph = QtWidgets.QWidget()
        self.tn_graph.setObjectName("tn_graph")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.tn_graph)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.canvas = QtWidgets.QScrollArea(self.tn_graph)
        self.canvas.setWidgetResizable(True)
        self.canvas.setObjectName("canvas")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.canvas.setWidget(self.scrollAreaWidgetContents_3)
        self.gridLayout_11.addWidget(self.canvas, 0, 0, 1, 1)
        self.tab_pca.addTab(self.tn_graph, "")
        self.gridLayout_2.addWidget(self.tab_pca, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 946, 27))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionPreference = QtWidgets.QAction(MainWindow)
        self.actionPreference.setObjectName("actionPreference")
        self.menuMenu.addAction(self.actionPreference)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(MainWindow)
        self.tab_pca.setCurrentIndex(0)
        self.button_csvPath.clicked.connect(MainWindow.readcsv) # type: ignore
        self.cmb_x.currentIndexChanged['int'].connect(MainWindow.setXaxis) # type: ignore
        self.cmb_y.currentIndexChanged['int'].connect(MainWindow.setYaxis) # type: ignore
        self.cmb_color.currentIndexChanged['int'].connect(MainWindow.setColor) # type: ignore
        self.cmb_sort.currentIndexChanged['int'].connect(MainWindow.setSort) # type: ignore
        self.cmb_subcolor.currentIndexChanged['int'].connect(MainWindow.setSubColor) # type: ignore
        self.cmb_subsort.currentIndexChanged['int'].connect(MainWindow.setSubSort) # type: ignore
        self.cmb_subsubcolor.currentIndexChanged['int'].connect(MainWindow.setSubsubColor) # type: ignore
        self.cmb_subsubsort.currentIndexChanged['int'].connect(MainWindow.setSubsubSort) # type: ignore
        self.cmb_plot.currentIndexChanged['int'].connect(MainWindow.setPlotType) # type: ignore
        self.button_preview.clicked.connect(MainWindow.graphDraw) # type: ignore
        self.button_save.clicked.connect(MainWindow.saveFigure) # type: ignore
        self.cb_colorbar.stateChanged['int'].connect(MainWindow.useColorbarI) # type: ignore
        self.cb_subcolorbar.stateChanged['int'].connect(MainWindow.useColorbarII) # type: ignore
        self.cb_subsubcolorbar.stateChanged['int'].connect(MainWindow.useColorbarIII) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_6.setText(_translate("MainWindow", "Style"))
        self.cb_logy.setText(_translate("MainWindow", "Log"))
        self.label_18.setText(_translate("MainWindow", "X-axis"))
        self.label_22.setText(_translate("MainWindow", "Graph Setting"))
        self.label_19.setText(_translate("MainWindow", "Y-axis"))
        self.label_28.setText(_translate("MainWindow", "subgroup"))
        self.label_24.setText(_translate("MainWindow", "Plot"))
        self.cb_legend.setText(_translate("MainWindow", "Legend"))
        self.label_bins.setText(_translate("MainWindow", "bins"))
        self.label.setText(_translate("MainWindow", "Color map"))
        self.cb_logc.setText(_translate("MainWindow", "Log"))
        self.label_5.setText(_translate("MainWindow", "–"))
        self.label_29.setText(_translate("MainWindow", "subsubgroup"))
        self.label_2.setText(_translate("MainWindow", "Title"))
        self.label_20.setText(_translate("MainWindow", "group"))
        self.cmb_plot.setItemText(0, _translate("MainWindow", "Scatter"))
        self.cmb_plot.setItemText(1, _translate("MainWindow", "kdeplot"))
        self.cmb_plot.setItemText(2, _translate("MainWindow", "Histogram"))
        self.cmb_plot.setItemText(3, _translate("MainWindow", "Line"))
        self.cmb_plot.setItemText(4, _translate("MainWindow", "Box plots"))
        self.label_30.setText(_translate("MainWindow", "alpha"))
        self.button_save.setText(_translate("MainWindow", "Save As..."))
        self.label_3.setText(_translate("MainWindow", "≤  x  ≤"))
        self.cb_subcolorbar.setText(_translate("MainWindow", "Colorbar"))
        self.cb_subsubcolorbar.setText(_translate("MainWindow", "Colorbar"))
        self.cb_colorbar.setText(_translate("MainWindow", "Colorbar"))
        self.label_7.setText(_translate("MainWindow", "Sort data by selected columns"))
        self.label_21.setText(_translate("MainWindow", "Size"))
        self.button_preview.setText(_translate("MainWindow", "Draw"))
        self.label_4.setText(_translate("MainWindow", "≤  y  ≤"))
        self.cb_logx.setText(_translate("MainWindow", "Log"))
        self.cmb_style.setItemText(0, _translate("MainWindow", "default"))
        self.button_csvPath.setText(_translate("MainWindow", "Select"))
        self.label_16.setText(_translate("MainWindow", "Sorted Data"))
        self.label_15.setText(_translate("MainWindow", "Imput CSV"))
        self.tab_pca.setTabText(self.tab_pca.indexOf(self.tn_summary), _translate("MainWindow", "CSV"))
        self.logbox.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'.SF NS Text\'; font-size:13pt;\"><br /></p></body></html>"))
        self.tab_pca.setTabText(self.tab_pca.indexOf(self.tab_4), _translate("MainWindow", "Log"))
        self.tab_pca.setTabText(self.tab_pca.indexOf(self.tn_graph), _translate("MainWindow", "Graph"))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.actionPreference.setText(_translate("MainWindow", "Preference"))