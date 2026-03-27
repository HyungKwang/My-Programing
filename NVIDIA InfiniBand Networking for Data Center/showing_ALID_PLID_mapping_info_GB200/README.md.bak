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

 ### Runing 

```
#python "...\nmx-c\nvlsm_mapping_visualizer.py" --nvlsm-dir "...\nvlsm" --out "diagram.png" --mode topology --gpu-index 0

#python "...\nvlsm_mapping_visualizer.py" --nvlsm-dir "...\nvlsm" --out "mapping.csv" --mode csv
```
 ### Running Output 
 
![Image](https://github.com/user-attachments/assets/9fa51bfe-7048-4fd3-9b2f-2dcfca6b8ed2)
> mapping.csv

```
GPU#	GPU_guid			GPU_ALID	GPU_ALID_hex		GPU_Port_guid		GPU_PLID		GPU_PLID_hex		NVSwitch_ASIC#	NVSwitch_guid		NVSwitch_LID	NVSwitch_LID_hex
1		0xc9acaafcd4dcea00	1025		0x0401				0xc9acaafcd4dcea0c	3090			0x0c12					1			0x6433aa030026af00		2					0x0002
1		0xc9acaafcd4dcea00	1025		0x0401				0xc9acaafcd4dcea0d	5122			0x1402					2			0x6433aa030026af20		3					0x0003
1		0xc9acaafcd4dcea00	1025		0x0401				0xc9acaafcd4dcea06	7170			0x1c02					3			0x6433aa030026ae40		4					0x0004
1		0xc9acaafcd4dcea00	1025		0x0401				0xc9acaafcd4dcea04	9218			0x2402					4			0x6433aa030026b440		5					0x0005
1		0xc9acaafcd4dcea00	1025		0x0401				0xc9acaafcd4dcea08	11266			0x2c02					5			0x6433aa030033e640		6					0x0006
1		0xc9acaafcd4dcea00	1025		0x0401				0xc9acaafcd4dcea07	13314			0x3402					6			0x6433aa030026ae60		7					0x0007
1		0xc9acaafcd4dcea00	1025		0x0401				0xc9acaafcd4dcea05	15362			0x3c02					7			0x6433aa030026b460		8					0x0008
1		0xc9acaafcd4dcea00	1025		0x0401				0xc9acaafcd4dcea09	17410			0x4402					8			0x6433aa030033e660		9					0x0009
1		0xc9acaafcd4dcea00	1025		0x0401				0xc9acaafcd4dcea02	19474			0x4c12					9			0x6433aa030026af80		1					0x0001
1		0xc9acaafcd4dcea00	1025		0x0401				0xc9acaafcd4dcea0e	21506			0x5402					10			0x6433aa030026b580		10					0x000a
1		0xc9acaafcd4dcea00	1025		0x0401				0xc9acaafcd4dcea10	23554			0x5c02					11			0x6433aa030026b780		11					0x000b
1		0xc9acaafcd4dcea00	1025		0x0401				0xc9acaafcd4dcea03	25620			0x6414					12			0x6433aa030026afa0		12					0x000c
1		0xc9acaafcd4dcea00	1025		0x0401				0xc9acaafcd4dcea0f	27650			0x6c02					13			0x6433aa030026b5a0		13					0x000d
1		0xc9acaafcd4dcea00	1025		0x0401				0xc9acaafcd4dcea11	29698			0x7402					14			0x6433aa030026b7a0		14					0x000e
1		0xc9acaafcd4dcea00	1025		0x0401				0xc9acaafcd4dcea00	31745			0x7c01					15			0x6433aa030033e8c0		15					0x000f
1		0xc9acaafcd4dcea00	1025		0x0401				0xc9acaafcd4dcea01	33793			0x8401					16			0x6433aa030033e8e0		16					0x0010
1		0xc9acaafcd4dcea00	1025		0x0401				0xc9acaafcd4dcea0a	35889			0x8c31					17			0x6433aa03000ffc80		17					0x0011
1		0xc9acaafcd4dcea00	1025		0x0401				0xc9acaafcd4dcea0b	37891			0x9403					18			0x6433aa03000ffca0		18					0x0012

```
