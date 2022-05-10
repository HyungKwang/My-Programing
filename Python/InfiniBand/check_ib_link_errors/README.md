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
$ python check_ib_link_errors_v5.py -h
usage: show_ib_inventory.py [-h] -i IBDIAGNET_FOLDER [-o OUTPUT_FILE] [-f] [-s] [-v]
optional arguments:
-h, --help show this help message and exit
-i IBDIAGNET_FOLDER, --ibdiagnet-folder IBDIAGNET_FOLDER
read data from ibdiagnet2 output folder
-o OUTPUT_FILE, --output-file OUTPUT_FILE
write IB SW and HCA inventory info to xlsx file
-f, --show-ib-hosts print detailed HCA inventory info
-s, --show-ib-switches
print detailed IB switch inventory info
-v, --version print current script version

```

```
$ python check_ib_link_errors_v5.py -i /var/tmp/ibdiagnet2 -o Saving_data
Running command: ibdiagnet --extended_speeds all --pm_per_lane --get_phy_info --get_cable_info --pc --reset_phy_info -o ./ibdiagnet_1st_reset_phy_info/
Start to parse ibdiagnet2.net_dump ...
Start to parse ibdiagnet2.db_csv ...
Start to parse ibdiagnet2.net_dump_ext ...
INFO: The --top-n option is not set, only the first 10 records will be listed here.
LinkDowned Counters:
##################################################
SrcDevice SrcPort SrcGUID LinkDownedCounter DstDevice DstGUID DstPort
SIB30183 74 0x0c42a103000ef7c6 4 MT4123 ConnectX6 Mellanox Technologies 0x0c42a10300389dc8 1
SIB30237 37 0x0c42a103000ef206 1 n08509 HCA-1 0x0c42a10300407088 1
MF0;G1-IB-CORE-SW05A:MCS8500/S02/U1 15 0xb8599f0300f7d9e6 1 MF0;G1-IB-CORE-SW05A:MCS8500/L15/U1 0x0c42a103000fd750 22
XmitDidscard Counters:
##################################################
SrcDevice SrcPort SrcGUID PortXmitDiscards DstDevice DstGUID DstPort
n08509 HCA-1 1 0x0c42a10300407088 290 SIB30237 0x0c42a103000ef206 37
SIB30237 37 0x0c42a103000ef206 192 n08509 HCA-1 0x0c42a10300407088 1
SIB30183 74 0x0c42a103000ef7c6 87 MT4123 ConnectX6 Mellanox Technologies 0x0c42a10300389dc8 1
MF0;G1-IB-CORE-SW05A:MCS8500/L15/U1 22 0x0c42a103000fd750 4 MF0;G1-IB-CORE-SW05A:MCS8500/S02/U1 0xb8599f0300f7d9e6 15
Port FEC Uncorrectable Counters:
##################################################
SrcDevice SrcPort SrcGUID PortFECUncorrectableBlockCounter DstDevice DstGUID DstPort
MF0;G2-IB-CORE-SW6A:MCS8500/S13/U1 12 0x0c42a103000501aa 4608243 MF0;G2-IB-CORE-SW6A:MCS8500/L12/U1 0x0c42a103000fdc30 33
MF0;G1-IB-CORE-SW04A:MCS8500/L03/U2 4 0x0c42a1030017d37c 2402008 SIB30064 0x0c42a103000eeca6 19
MF0;G1-IB-CORE-SW05A:MCS8500/L12/U1 2 0x0c42a103000fdbd0 1558267 SIB30022 0x0c42a103000be30e 16
INFO: ExcessiveBufferOverrunErrors counters are 0 on all links.
Congestion Indexes > 10:
##################################################
SrcDevice SrcPort SrcGUID PortXmitWaitExt PortXmitPktsExtended CongestionIndexExt DstDevice DstGUID DstPort
n00110 HCA-1 1 0x0c42a10300619450 561153409 1 561153409.0 SIB30003 0x0c42a103001268d0 62
n00235 HCA-1 1 0x0c42a10300330432 557213155 1 557213155.0 SIB30008 0x0c42a103000be12e 9
n00225 HCA-1 1 0x0c42a1030036bb58 463507299 1 463507299.0 SIB30008 0x0c42a103000be12e 65
Effective BER Counters > 1e-12:
##################################################
SrcDevice SrcPort SrcGUID EffectiveBER SymbolBER DstDevice DstGUID DstPort
MF0;G2-IB-CORE-SW6A:MCS8500/S13/U1 12 0x0c42a103000501aa 5.000000e-08 1.500000e-254 MF0;G2-IB-CORE-SW6A:MCS8500/L12/U1 0x0c42a103000fdc30 33
MF0;G1-IB-CORE-SW04A:MCS8500/L10/U2 15 0x0c42a103000fd200 3.000000e-08 1.500000e-254 SIB30095 0x0c42a103000ef0a6 20
MF0;G1-IB-CORE-SW04A:MCS8500/L03/U2 4 0x0c42a1030017d37c 2.000000e-08 1.000000e-12 SIB30064 0x0c42a103000eeca6 19
Symbol BER Counters > 1e-13:
##################################################
SrcDevice SrcPort SrcGUID EffectiveBER SymbolBER DstDevice DstGUID DstPort
MF0;G1-IB-CORE-SW04A:MCS8500/L03/U2 4 0x0c42a1030017d37c 2.000000e-08 1.000000e-12 SIB30064 0x0c42a103000eeca6 19

```


## For further details, please refer to the manaul "IB Fabric Congestion Analysis v5.0.pdf"
