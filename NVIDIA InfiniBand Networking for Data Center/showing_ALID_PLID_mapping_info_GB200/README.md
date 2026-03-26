## Intro

On NVIDIA Blackwell systems, new concepts and terminology have been introduced, such as ALID, PLID, and others.
In the case of GB200 NVL72, however, the system is extremely large, which makes it difficult to understand how ALIDs, PLIDs, and switch ASICs are mapped to each other.
This script provides a quick mapping overview and visual representations that show how these components are connected.
The script was implemented using Cursor. If you understand the underlying principles, you can also adapt it to your own preferred ¡°vibe coding¡± style.


## How to run

 ### It installed lib needed for this script.

> From my window CMD
     
```
pip install -r "c:\E\±â¼ú\...\nmx-c\requirements-nvlsm-viz.txt"
```

 ### Runing 

```
python "...\nmx-c\nvlsm_mapping_visualizer.py" --nvlsm-dir "...\nvlsm" --out "diagram.png" --mode topology --gpu-index 0

python "...\nvlsm_mapping_visualizer.py" --nvlsm-dir "...\nvlsm" --out "mapping.csv" --mode csv
```

