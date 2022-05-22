# sview-gui

PyQt5 GUI for data visualisation based on matplotlib and seaborn.
Have you ever felt that you are wasting a lot of time writing the code for a simple figure?
If so, this GUI will help you out to save your time. You can plot and save your figure by just pushing a couple of buttons on Sviewgui. Not only that, you can also get the source code of your plot so that you can copy and paste it to your environment to adjust minor settings.
Main features are
+ Scatter, line, kdeplot, histgram, and box plot
+ Detail setting for the style of plot, marker size, line width, number of bins of histgram, colormap, colorbar, etc.
+ Subdevide your data based on the columns of DataFrame and use different colors for each subset in your plot.
+ Save figure as editable PDF
+ Source code of the graph you plotted are recorded in the log window

# Usage

This package has only one method: buildGUI(). 
You can use the file path of your csv file as an argument.
Also, you can use pandas' DataFrame object for the argument.

# Recent updata

+ Fixed minor bugs.
+ log scale for negative columns, colorbar, histgram
+ Adjustable style
+ kdeplot with scatter plot.

# About license
© 2019 Sojiro Fukuda All Rightss Reserved.
Free to modify and redistribute by your own responsibility.
