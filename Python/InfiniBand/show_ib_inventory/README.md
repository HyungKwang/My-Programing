## Intro

 This script helps to give quick view of Infiniband device & each FW info.
 It extracts from ibdiagnet file.

 

## How to run

 ### You must install pandas libarary. 

> From my system
     
```
[root@My_test_lab ~]# python3 --version

 Python 3.6.8
 Prerequisites:
 Python 3.8+
 Pandas library
 OpenPyXL library

[root@My_test_lab ~]# pip3 install pandas
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
C:\Python39\study>show_ib_inventory.py -h
usage: show_ib_inventory.py [-h] -i IBDIAGNET_FOLDER [-o OUTPUT_FILE] [-f] [-s] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -i IBDIAGNET_FOLDER, --ibdiagnet-folder IBDIAGNET_FOLDER
                        read data from ibdiagnet2 output folder
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        write IB SW and HCA inventory info to xlsx file
  -f, --show-ib-hosts   print detailed HCA inventory info
  -s, --show-ib-switches
                        print detailed IB switch inventory info
  -v, --version         print current script version
```

![1](https://github.com/HyungKwang/My-Programing/assets/91254602/53af0a7a-5887-4751-bd52-248d1078db59)

