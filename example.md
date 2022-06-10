# Sample Code

```python
## Sample Code 1
import sviewgui.sview as sv
sv.buildGUI()
```

```python
## Sample Code 2
import sviewgui.sview as sv
FILE_PATH = "User/Documents/yourdata.csv"
sv.buildGUI(FILE_PATH)
```

```python
## Sample Code 3
import sviewgui.sview as sv
import seaborn as sns
import pandas as pd

df = sns.load_dataset('penguins')
sv.buildGUI(df)
```
