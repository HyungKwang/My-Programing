## Intro

 This script helps to give quick view of Infiniband Fabric congestion related.
 It sorts down based on ibdiagnet file.

 

## How to run

 ### My script coded/developed/runs on Window. In Apple MAC, it does not work

> If you want to run it in WSL

     
```
jun@HYUNGKWANGC-LT:/mnt/c/TEST$$ sudo apt install python3-pip
jun@HYUNGKWANGC-LT:/mnt/c/TEST$$ pip3 install pandas

jun@HYUNGKWANGC-LT:/mnt/c/TEST$ python3 check_ib_link_status_v20.py  -h
```

 ### You must install python related libarary. 

> From my system
     
```
[root@My_test_lab ~]# python3 --version

 Python 3.6.8
 Prerequisites:
 Python 3.8+
 Pandas library
 OpenPyXL library

[root@My_test_lab ~]# pip3 install pandas
[root@My_test_lab ~]# pip3 install openpyxl 
[root@My_test_lab ~]# pip3 list

 DEPRECATION: The default format will switch to columns in the future. You can use --format=(legacy|columns) (or define a 
 format=(legacy|columns) in your pip.conf under the [list] section) to disable this warning.
 backports.entry-points-selectable (1.1.1)
 certifi (2021.10.8)
 chardet (3.0.4)
 charset-normalizer (2.0.10)
 distlib (0.3.4)
 filelock (3.4.0)
 idna (2.10)
 importlib-metadata (4.8.2)
 importlib-resources (5.4.0)
 numpy (1.19.5)
 pandas (1.1.5) <===========
 pip (9.0.3)
 platformdirs (2.4.0)
 pynetbox (6.5.0)
 PySocks (1.6.8)
 python-dateutil (2.8.2)
 pytz (2021.3)
 requests (2.27.1)
 setuptools (39.2.0)
 six (1.16.0)
 typing-extensions (4.0.1)
 urllib3 (1.25.6)
 virtualenv (20.10.0)
 zipp (3.6.0)

```

 ### Runing
      

```
$python check_ib_link_status_v17.py -h

usage: usage: check_ib_link_status_v17.py [-h] -i IBDIAGNET_FOLDER [-o OUTPUT_FILE] [-n TOP_N] [-s LID_CHECKING] [-a] [-v]

Examples (How to run) > :

  #python check_ib_link_status_v15.py -i ./tem/ibdiagnet2
  #python check_ib_link_status_v15.py -i ./tem/ibdiagnet2 -a
  #python check_ib_link_status_v15.py -i ./tem/ibdiagnet2 -a -n 20
  #python check_ib_link_status_v15.py -i ./tem/ibdiagnet2 -a -n 20 -o  C:\Python39\study\save_backdata.xlsx
  #python check_ib_link_status_v15.py -i ./tem/ibdiagnet2 -a -n 20 -s lid_checking -o C:\Python39\study\save_backdata.xlsx

optional arguments:
  -h, --help            show this help message and exit
  -i IBDIAGNET_FOLDER, --ibdiagnet-folder IBDIAGNET_FOLDER
                        read data from ibdiagnet2 output folder
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        write results to xlsx file
  -n TOP_N, --top-n TOP_N
                        print first N entries(by default, n = 10)
  -s LID_CHECKING, --lid_checking LID_CHECKING
                        lid_checking : Skip Invalid LID & Mcast LID checking
  -a, --all             Display all TX/RX Bandwidth & Lost Bandwidth in details
  -v, --version         print current script version
```

![Untitled](https://github.com/HyungKwang/My-Programing/assets/91254602/676325c9-ac19-4a87-a6c6-92b05f78cf45)


## For further details, please refer to the manaul.
