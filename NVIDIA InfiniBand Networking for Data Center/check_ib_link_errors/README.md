## Intro

 This script helps to give quick view of Infiniband Fabric congestion related.
 It sorts down based on ibdiagnet file.

 

## How to run

 ### You must install python related libarary. 

> From my system
     
```
[root@My_test_lab ~]# python --version
Python 3.8.0

[root@My_test_lab ~]# pip3 install pandas
[root@My_test_lab ~]# pip3 install openpyxl 
[root@My_test_lab ~]# pip3 list

[root@My_test_lab ~]#pip3 list
Package         Version
--------------- -----------
et-xmlfile         1.1.0
numpy            1.24.4
openpyxl         3.1.3  <=========
pandas            2.0.3   <=========
pip                24.1
PyQt5             5.15.10
PyQt5-Qt5       5.15.2
PyQt5-sip        12.13.0
XlsxWriter        3.2.0   <=======
```

 ### Runing 

```python
$python check_ib_link_status_v29.py -h

usage: usage: check_ib_link_status_v29.py [-h] -i IBDIAGNET_FOLDER [-o OUTPUT_FILE] [-n TOP_N] [-s] [-c] [-a] [-v]

Examples (How to run) > :

  #python check_ib_link_status_v15.py -i ./tem/ibdiagnet2
  #python check_ib_link_status_v29.py -i ./tem/ibdiagnet2 -a
  #python check_ib_link_status_v29.py -i ./tem/ibdiagnet2 -a -n 20
  #python check_ib_link_status_v29.py -i ./tem/ibdiagnet2 -a -n 20 -o  C:\Python39\study\save_backdata.xlsx
  #python check_ib_link_status_v29.py -i ./tem/ibdiagnet2 -a -n 20 -s -o C:\Python39\study\save_backdata.xlsx
  #python check_ib_link_status_v29.py -i ./tem/ibdiagnet2 -a -n 20 -c -s -o C:\Python39\study\save_backdata.xlsx

optional arguments:
  -h, --help            show this help message and exit
  -i IBDIAGNET_FOLDER, --ibdiagnet-folder IBDIAGNET_FOLDER
                        read data from ibdiagnet2 output folder
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        write results to xlsx file
  -n TOP_N, --top-n TOP_N
                        print first N entries(by default, n = 10)
  -s, --skip-lid-checking
                        skip_lid_checking : Skip Invalid LID & Mcast LID checking
  -c, --skip-cable-checking
                        reading ibdiagnet2.cables (if file size big), it takes much time. So, To skip cables/optic chcecking
  -a, --all             Display all TX/RX Bandwidth & Lost Bandwidth in details
  -v, --version         print current script version


```

![Untitled](https://github.com/HyungKwang/My-Programing/assets/91254602/676325c9-ac19-4a87-a6c6-92b05f78cf45)


## For further details, please refer to the manaul.
