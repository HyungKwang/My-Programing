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
1		0x2222222222222200	1025		0x0401				0x222222222222220c	3090			0x0c12					1			0xXXXXXXXXXX26af00		2					0x0002
1		0x2222222222222200	1025		0x0401				0x222222222222220d	5122			0x1402					2			0xXXXXXXXXXX26af20		3					0x0003
1		0x2222222222222200	1025		0x0401				0x2222222222222206	7170			0x1c02					3			0xXXXXXXXXXX26ae40		4					0x0004
1		0x2222222222222200	1025		0x0401				0x2222222222222204	9218			0x2402					4			0xXXXXXXXXXX26b440		5					0x0005
1		0x2222222222222200	1025		0x0401				0x2222222222222208	11266			0x2c02					5			0xXXXXXXXXXX33e640		6					0x0006
1		0x2222222222222200	1025		0x0401				0x2222222222222207	13314			0x3402					6			0xXXXXXXXXXX26ae60		7					0x0007
1		0x2222222222222200	1025		0x0401				0x2222222222222205	15362			0x3c02					7			0xXXXXXXXXXX26b460		8					0x0008
1		0x2222222222222200	1025		0x0401				0x2222222222222209	17410			0x4402					8			0xXXXXXXXXXX33e660		9					0x0009
1		0x2222222222222200	1025		0x0401				0x2222222222222202	19474			0x4c12					9			0xXXXXXXXXXX26af80		1					0x0001
1		0x2222222222222200	1025		0x0401				0x222222222222220e	21506			0x5402					10			0xXXXXXXXXXX26b580		10					0x000a
1		0x2222222222222200	1025		0x0401				0x2222222222222210	23554			0x5c02					11			0xXXXXXXXXXX26b780		11					0x000b
1		0x2222222222222200	1025		0x0401				0x2222222222222203	25620			0x6414					12			0xXXXXXXXXXX26afa0		12					0x000c
1		0x2222222222222200	1025		0x0401				0x222222222222220f	27650			0x6c02					13			0xXXXXXXXXXX26b5a0		13					0x000d
1		0x2222222222222200	1025		0x0401				0x2222222222222211	29698			0x7402					14			0xXXXXXXXXXX26b7a0		14					0x000e
1		0x2222222222222200	1025		0x0401				0x2222222222222200	31745			0x7c01					15			0xXXXXXXXXXX33e8c0		15					0x000f
1		0x2222222222222200	1025		0x0401				0x2222222222222201	33793			0x8401					16			0xXXXXXXXXXX33e8e0		16					0x0010
1		0x2222222222222200	1025		0x0401				0x222222222222220a	35889			0x8c31					17			0xXXXXXXXXXX0ffc80		17					0x0011
1		0x2222222222222200	1025		0x0401				0x222222222222220b	37891			0x9403					18			0xXXXXXXXXXX0ffca0		18					0x0012

```
