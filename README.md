# sview-gui

PyQt5 GUI for data visualisation based on matplotlib and seaborn.
Have you ever felt that you are wasting a lot of time writing the code for a simple figure?
If so, this GUI will help you out to save your time. 
You can plot and save your figure by just pushing a couple of buttons on Sviewgui.
All figures you made are recorded in the log window as their source code. 
You can reproduce and further modify your figures, copying and pasting the code from the log into your own editor.

Main features are
+ Scatter, line, kdeplot, histgram, and box plot
+ Detail setting for the style of plot, marker size, line width, number of bins of histgram, colormap, colorbar, etc.
+ Subdevide your data based on the columns of DataFrame and use different colors for each subset in your plot.
+ Save figure as editable PDF
+ Source code of the graph you plotted are recorded in the log window

# Usage

This package has only one method: buildGUI(). 
```python
import sviewgui.sview as sv

sv.buildGUI()
```
Then, GUI window will pop up, then you can choose your csv file via GUI.
Alternatively, you can also pass the path of your csv file,
```python
import sviewgui.sview as sv

csvpath = 'usr/mydata.csv'
sv.buildGUI(csvpath)
```
or pandas DataFrame object
```python
import sviewgui.sview as sv
from sklearn.datasets import load_iris
import pandas as pd

data = load_iris() # load iris data as series
df = pd.DataFrame(data=data.data, columns=data.feature_names)
sv.buildGUI(df)
```
Now, you are good to go. Have a fun with Sview.


# Recent updata

+ Fixed minor bugs.
+ log scale for negative columns, colorbar, histgram
+ Adjustable style (seaborn, ggplot, etc.)
+ kdeplot with scatter plot.

# About license
© 2019 Sojiro Fukuda All Rightss Reserved.
Free to modify and redistribute by your own responsibility.
