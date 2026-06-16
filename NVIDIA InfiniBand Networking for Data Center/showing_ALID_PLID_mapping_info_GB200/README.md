## Intro

On NVIDIA Blackwell systems, new concepts and terminology have been introduced, such as ALID, PLID, and others.
In the case of GB200 NVL72, however, the system is extremely large, which makes it difficult to understand how ALIDs, PLIDs, and switch ASICs are mapped to each other.
This script provides a quick mapping overview and visual representations that show how these components are connected.
The script was implemented using Cursor. If you understand the underlying principles, you can also adapt it to your own preferred ¡°vibe coding¡± style.


## How to run

 ### It installs lib needed for this script.

> From my window CMD
     
```
#pip install -r "c:\E\nmx-c\requirements-nvlsm-viz.txt"
```

 ### Running 

```
#python "...\nmx-c\nvlsm_mapping_visualizer.py" --nvlsm-dir "...\nvlsm" --out "diagram.png" --mode topology --gpu-index 0

```
 ## Diagram

<img width="1478" height="741" alt="Image" src="https://github.com/user-attachments/assets/1a2f83cc-2f98-471a-8f58-91e322f9be46" />

 ### Running 

```
#python "...\nvlsm_mapping_visualizer.py" --nvlsm-dir "...\nvlsm" --out "mapping.csv" --mode csv
```
 ## mapping.csv

<img width="784" height="259" alt="Image" src="https://github.com/user-attachments/assets/9ed19372-e533-4754-a4f3-83dd273f6305" />