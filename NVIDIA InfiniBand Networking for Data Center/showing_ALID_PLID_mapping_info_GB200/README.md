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
 
![Image](https://github.com/user-attachments/assets/bff800a9-5ce9-4091-b3ce-89872cf7ab2e)

> mapping.csv

```
gpu 	base_guid				alid	alid_hex		plane_idx		plid_hex		plid_dec		switch_guid			switch_lid_dec	switch_lid_hex
1		1111111111111111	1025		0x0401		      1				0x0c12			3090			xxxxxxxxxxxxxxxx				2					0x0002
1		1111111111111111	1025		0x0401		      2				0x1402			5122			xxxxxxxxxxxxxxxx				3					0x0003
1		1111111111111111	1025		0x0401    	  	3				0x1c02			7170			xxxxxxxxxxxxxxxx				4					0x0004
1		1111111111111111	1025		0x0401				4			0x2402			9218			xxxxxxxxxxxxxxxx				5					0x0005
1		1111111111111111	1025		0x0401				5			0x2c02			11266			xxxxxxxxxxxxxxxx				6					0x0006
1		1111111111111111	1025		0x0401				6			0x3402			13314			xxxxxxxxxxxxxxxx				7					0x0007
1		1111111111111111	1025		0x0401				7			0x3c02			15362			xxxxxxxxxxxxxxxx				8					0x0008
1		1111111111111111	1025		0x0401				8			0x4402			17410			xxxxxxxxxxxxxxxx				9					0x0009
1		1111111111111111	1025		0x0401				9			0x4c12			19474			xxxxxxxxxxxxxxxx				1					0x0001
1		1111111111111111	1025		0x0401				10			0x5402			21506			xxxxxxxxxxxxxxxx				10				0x000a
1		1111111111111111	1025		0x0401				11			0x5c02			23554			xxxxxxxxxxxxxxxx				11				0x000b
1		1111111111111111	1025		0x0401				12			0x6414			25620			xxxxxxxxxxxxxxxx				12				0x000c
1		1111111111111111	1025		0x0401				13			0x6c02			27650			xxxxxxxxxxxxxxxx				13				0x000d
1		1111111111111111	1025		0x0401				14			0x7402			29698			xxxxxxxxxxxxxxxx				14				0x000e
1		1111111111111111	1025		0x0401				15			0x7c01			31745			xxxxxxxxxxxxxxxx				15				0x000f
1		1111111111111111	1025		0x0401				16			0x8401			33793			xxxxxxxxxxxxxxxx				16				0x0010
1		1111111111111111	1025		0x0401				17			0x8c31			35889			xxxxxxxxxxxxxxxx				17				0x0011
1		1111111111111111	1025		0x0401				18			0x9403			37891			xxxxxxxxxxxxxxxx				18				0x0012
```