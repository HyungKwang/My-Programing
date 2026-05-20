## Intro

 This script gives a quick overview of Infiniband Fabric status based on ibdiagnet collection.


## Running environment
 I've coded it based on Window CMD. It works well in Window CMD
 It may not work MAC or Linux server. The reason why,, because my labtop is Window.
 If there is a request from MAC/Linux users, i can make it.

## How to run

 ### step.1 : please run & collect ibdiagnet files. (refer to below 2 running commands as an example)
```
#ibdiagnet -r -P all=1 --extended_speeds all --pm_per_lane --get_phy_info --get_cable_info 
#tar cvf ibdiagnet_A.tar /var/tmp/ibdiagnet2/

#ibdiagnet -r --pc --pm_pause_time 100 -P all=1 --extended_speeds all --pm_per_lane --reset_phy_info  --get_phy_info  --get_cable_info 
#tar cvf ibdiagnet_B.tar /var/tmp/ibdiagnet2/
```

 ### step.2 : You must install python related libararies in your Window to run the script.

> From my Window Laptop
     
```
[root@My_test_lab ~]# python --version
Python 3.8.0

[root@My_test_lab ~]# pip3 install pandas
[root@My_test_lab ~]# pip3 install openpyxl 
[root@My_test_lab ~]# pip3 list

[root@My_test_lab ~]#pip3 list
Package         Version
--------------- -----------
et-xmlfile       1.1.0
numpy            1.24.4
openpyxl         3.1.3   <=========
pandas           2.0.3   <=========
pip              24.1
PyQt5            5.15.10
PyQt5-Qt5        5.15.2
PyQt5-sip        12.13.0
XlsxWriter       3.2.0   <=======
```

 ### step.3 : Open up Window CMD. Then run the command referring to below examples & adding useful several parameters. 

```
C:\Python_3.13.3\Study>python check_ib_link_status_v39.py -h
usage: usage: check_ib_link_status_v39.py [-h] -i IBDIAGNET_FOLDER [-o OUTPUT_FILE] [-n TOP_N] [-s] [-c] [-d] [-a] [-v]

Examples (How to run) > :

  #python check_ib_link_status_v37.py -i ./tem/ibdiagnet2
  #python check_ib_link_status_v37.py -i ./tem/ibdiagnet2 -a
  #python check_ib_link_status_v37.py -i ./tem/ibdiagnet2 -a -n 20
  #python check_ib_link_status_v37.py -i ./tem/ibdiagnet2 -a -n 20 -o  C:\Python39\study\save_backdata.xlsx
  #python check_ib_link_status_v37.py -i ./tem/ibdiagnet2 -a -n 20 -s -o C:\Python39\study\save_backdata.xlsx
  #python check_ib_link_status_v37.py -i ./tem/ibdiagnet2 -a -n 20 -c -s -o C:\Python39\study\save_backdata.xlsx
  #python check_ib_link_status_v37.py -i ./tem/ibdiagnet2 -d

options:
  -h, --help            show this help message and exit
  -i, --ibdiagnet-folder IBDIAGNET_FOLDER
                        read data from ibdiagnet2 output folder
  -o, --output-file OUTPUT_FILE
                        write results to xlsx file
  -n, --top-n TOP_N     print first N entries(by default, n = 10)
  -s, --skip-lid-checking
                        Skip Invalid LID & Mcast LID checking
  -c, --skip-cable-checking
                        reading ibdiagnet2.cables. if file size big, it takes much time. So, To skip cables checking
  -d, --debug           Collecting all row data to a csv format file for debugging purpose
  -a, --all             Display all TX/RX Bandwidth & Lost Bandwidth in details
  -v, --version         print current script version
```
## Script running output

```console
C:\Python_3.13.3\Study>python check_ib_link_status_v39.py -i ./del/ibdiagnet_A/var/tmp/ibdiagnet2 -o C:\Python_3.13.3\Study\del\A.xlsx -c

INFO: The --top-n option is not set, only the first 10 records will be listed here.


Running command:   /opt/ufm/opensm/bin/ibdiagnet -r -P all=1 --extended_speeds all --pm_per_lane --get_phy_info --get_cable_info


IB Switch Inventory Summary:
Total IB SW/ASIC: 639
##################################################
--------------------------------------------------
PSID: MT_0000000579 => QM9790 (NVIDIA_Unmanaged_switch,NDR)
--------------------------------------------------
FW Ver.:     31.2012.1068       Qty.:      1
FW Ver.:     31.2012.2148       Qty.:     71
FW Ver.:     31.2014.2084       Qty.:    567
--------------------------------------------------

HCA Inventory Summary:
Total HCAs : 7982
##################################################
--------------------------------------------------
PSID: MT_0000000838 => CX-7 (NVIDIA, NDR IB 1-port OSFP)
--------------------------------------------------
FW Ver.:       28.36.1010       Qty.:      1
FW Ver.:       28.39.1002       Qty.:     22


No Invalid LID & Mcast LID found
##################################


LinkDowned Counters > 0 (Qt :150):
##################################################
         SrcDevice SrcPort            SrcGUID  LinkDownedCounter              DstDevice DstPort            DstGUID
      leaf-08       3 0x116a1c0300d58700                255               lab121 mlx5_4       1 0x1263c00300756e8e
lab121 mlx5_4       1 0x1263c00300756e8e                255                     leaf-08       3 0x116a1c0300d58700


XmitDidscard Counters > 0 (Qt :162)
##################################################
      SrcDevice SrcPort           SrcGUID  PortXmitDiscards             DstDevice DstPort            DstGUID
 node004 HCA-7       1 0x58a2e10300a783ce             29943                         leaf3      22 0x116a1c0300ba7d40
       leaf-08       3 0x116a1c0300d58700             15235                 lab121 mlx5_4       1 0x1263c00300756e8e


Port FEC Uncorrectable Counters (Qt :1290)
##################################################
 SrcDevice SrcPort         SrcGUID  PortFECUncorrectableBlockCounter      DstDevice DstPort            DstGUID
 leaf-01      38 0x116a1c0300d56980                         169408964              spine-02   1/1/2 0x116a1c0300f3b580
   leaf8      32 0x116a1c0300bf3e00                          27337479         node148 HCA-8       1 0x1263c00300074bb4


Buffer overrun Counters > 0 (Qt : 0):
##################################################

Max Retransmission_rate : > 500 (Qt : 0):
##################################################


Raw BER Counters > 1e-5 (Qt :93)
##################################################
     SrcDevice SrcPort            SrcGUID  RawBER           DstDevice DstPort            DstGUID
         leaf8      32 0x116a1c0300bf3e00  0.0004       node148 HCA-8       1 0x1263c00300074bb4
       leaf-06      30 0x116a1c0300d41040  0.0003      HGX-190 mlx5_8       1 0x58a2e103001a5f4a

Effective BER Counters > 1e-13 (Qt :69)
##################################################
     SrcDevice SrcPort           SrcGUID  EffectiveBER      DstDevice DstPort           DstGUID
 lab010 HCA-1       1 0x58a2e10300a76fd6  5.000000e-06          leaf6       8 0x116a1c0300ba8f80
      leaf-01      38 0x116a1c0300d56980  2.000000e-07       spine-02   1/1/2 0x116a1c0300f3b580


Symbol BER Counters > 1e-13, or Err > 0 (Qt :2)
##################################################
    SrcDevice SrcPort            SrcGUID    SymbolBER     DstDevice DstPort            DstGUID
lab011 HCA-2       1 0x58a2e10300a77fe6 4.000000e-08          leaf6      11 0x116a1c0300ba6c80
lab010 HCA-1       1 0x58a2e10300a76fd6 1.000000e-12          leaf6       8 0x116a1c0300ba8f80


Congestion Indexes > 10 (will be deprecated):
##################################################
   SrcDevice SrcPort            SrcGUID  PortXmitWaitExt  PortXmitPktsExtended  CongestionIndexExt  DstDevice DstPort  DstGUID


IB Device temperature > 70c or IB Switch Asic temperature > 70c (Qt : 783)
##################################################
          NodeGUID    NodeDesc  IbDeviceTemperature  SwitchAsicTemperature
0x116a1c0300ba85c0 lab7-15                 79.0                   79.0
0x116a1c0300bcf940 lab1-13                 79.0                   79.0


PSU problem regarding (IsPresent, IsFRU, DCState, AlertState )
##################################################

Saving to Excel file:
##################################################

Data is written successfully to Excel File: C:\Python_3.13.3\Study\del\A.xlsx
```

