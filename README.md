# Houdini Lip-sync

## Installation

Download the four files to the folder: `"C:\Users\<your_username>\Documents\houdini17.0\toolbar"`

Next, set up environment variables and system paths in your Houdini Python shell:
```python
>>> import os
>>> import sys
>>> path = "C:/Users/<your_username>/Documents/houdini17.0/toolbar"
>>> os.environ['TOOLBAR_PATH'] = path
>>> sys.path.append(path)
```

## Usage

