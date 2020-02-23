# sview-gui

PyQt5 GUI for data visualisation of csv file or pandas' DataFrame.
This GUI is based on the matplotlib and you can visualize your csv file in various ways.
Here are the main features;

- Scatter, line, density, histgram, and box plot for visualisation your csv
- Detail setting for the marker size, line width, number of bins of histgram, color map (from cmocean)
- Save figure as editable PDF
- Source code of the graph you plotted are recorded in the log window

# Usage

This package has only one method: buildGUI(). 
This method takes zero or one arguments like bellow.

```python
## Sample Code 1 ##
import sviewgui.sview as sv

sv.buildGUI()
```

Also you can use the file path of your csv file.

```python
## Sample Code 2 ##
import sviewgui.sview as sv

FILE_PATH = "User/Documents/yourdata.csv"
sv.buildGUI(FILE_PATH)
```

You can use pandas' DataFrame object for the argument.

```python
## Sample Code 3 ##
import sviewgui.sview as sv
import pandas as pd

FILE_PATH = "User/Documents/yourdata.csv"

df = pd.read_csv(FILE_PATH)
sv.buildGUI(df)
```

# About license
© 2019 Sojiro Fukuda All Rightss Reserved.
Free to modify and redistribute by your own responsibility.