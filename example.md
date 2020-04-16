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
import pandas as pd

FILE_PATH = "User/Documents/yourdata.csv"
df = pd.read_csv(FILE_PATH)
sv.buildGUI(df)
```
