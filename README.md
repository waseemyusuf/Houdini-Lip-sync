# Houdini Lip-sync

The shelf tool UI:
<p align="center">
  <img src="https://github.com/waseemyusuf/Houdini-Lip-sync/raw/master/imgs/shelf_tool_ui.PNG" width="500"/>
</p>
The generated CHOP network:
<p align="center">
  <img src="https://github.com/waseemyusuf/Houdini-Lip-sync/raw/master/imgs/chop_network.PNG"width="500"/>
</p>

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

