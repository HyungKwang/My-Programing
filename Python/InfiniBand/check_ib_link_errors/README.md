## Intro

 This script helps to give quick view of Infiniband Fabric congestion related.
 It sorts down based on ibdiagnet file.

 

## How to run

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
$python check_ib_link_status_v12.py -h
usage: usage: check_ib_link_status_v12.py [-h] -i IBDIAGNET_FOLDER [-o OUTPUT_FILE] [-n TOP_N] [-a] [-v]

Examples (How to run) > :

  #python check_ib_link_status_v10.py -i ./tem/ibdiagnet2
  #python check_ib_link_status_v12.py -i ./tem/ibdiagnet2 -a
  #python check_ib_link_status_v12.py -i ./tem/ibdiagnet2 -a -n 20
  #python check_ib_link_status_v12.py -i ./tem/ibdiagnet2 -a -n 20 -o  C:\Python39\study\save_backdata.xlsx

optional arguments:
  -h, --help            show this help message and exit
  -i IBDIAGNET_FOLDER, --ibdiagnet-folder IBDIAGNET_FOLDER
                        read data from ibdiagnet2 output folder
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        write results to xlsx file
  -n TOP_N, --top-n TOP_N
                        print first N entries(by default, n = 10)
  -a, --all             Display TX/RX Bandwiths in details
  -v, --version         print current script version


```

```
$ python check_ib_link_status_v12.py -i ./tem/ibdiagnet2 -a -n 20 -o  C:\Python39\study\save_backdata.xlsx

   Running command: ibdiagnet --extended_speeds all --pm_per_lane --get_phy_info --get_cable_info --pc --reset_phy_info -o ./ibdiagnet_1st_reset_phy_info/

   LinkDowned Counters:
   ##################################################
    SrcDevice            SrcPort            SrcGUID LinkDownedCounter DstDevice                     DstGUID   DstPort
    SIB30183                  74 0x0c42a10300bbbbbb                4   MT4123 ConnectX6   0x0c42a1030aaaaaaa         1
    SIB30237                  37 0x0c42a10300aaaaaa                1   n08509 HCA-1       0x0c42a10300407088         1
    CORE-SW05A:MCS8500/S02/U1 15 0xb8599f0300dddddd                1   CORE-SW05A:/L15/U1 0x0c42a10300ssssss        22
   
   XmitDidscard Counters:
  ##################################################
    SrcDevice    SrcPort            SrcGUID PortXmitDiscards DstDevice DstGUID           DstPort
    n08509 HCA-1       1 0x0c42a10301111111              290  SIB30237 0x0c42a10322222222     37
   ~
   ~


```


## For further details, please refer to the manaul.
