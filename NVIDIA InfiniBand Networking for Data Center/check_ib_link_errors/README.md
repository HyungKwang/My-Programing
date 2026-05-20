## Intro

 This script gives a quick overview of Infiniband Fabric status based on ibdiagnet collection.


## Running environment
 I've coded it based on Window CMD. It works well in Window CMD
 It may not work MAC or Linux server. The reason why,, because my labtop is Window.
 If there is a request from MAC/Linux users, i can make it.

## How to run

 ### step.1 : please run & collect ibdiagnet files. please refer to below 2 running command examples. 
'''
#ibdiagnet -r -P all=1 --extended_speeds all --pm_per_lane --get_phy_info --get_cable_info 
#tar cvf ibdiagnet_A.tar /var/tmp/ibdiagnet2/

#ibdiagnet -r --pc --pm_pause_time 100 -P all=1 --extended_speeds all --pm_per_lane --reset_phy_info  --get_phy_info  --get_cable_info 
#tar cvf ibdiagnet_B.tar /var/tmp/ibdiagnet2/
'''

 ### step.2 You must install python related libararies in your Window to run the script.

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

 ### step.1 : Open up Window CMD. Then run the command referring to below examples & adding useful several parameters. 

```
C:\Python_3.13.3\Study>python check_ib_link_status_v37.py -h
usage: usage: check_ib_link_status_v37.py [-h] -i IBDIAGNET_FOLDER [-o OUTPUT_FILE] [-n TOP_N] [-s] [-c] [-d] [-a] [-v]

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
## Results

```bash
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
PSID: DEL0000000036 => CX-7 (DELL, NDR 1-Port OSFP IB Adapter Card)
--------------------------------------------------
FW Ver.:       28.36.1010       Qty.:      1
FW Ver.:       28.41.1000       Qty.:   1983
FW Ver.:       28.43.2026       Qty.:     55
FW Ver.:       28.44.1036       Qty.:      8
--------------------------------------------------
PSID: DEL0000000051 => CX-7 (DELL, NDR 1-Port VPI OSFP Adapter)
--------------------------------------------------
FW Ver.:       28.43.2026       Qty.:      1
--------------------------------------------------
PSID: MT_0000000691 => CX-6 (NVIDIA, HDR dual-port QSFP56)
--------------------------------------------------
FW Ver.:       20.39.2048       Qty.:      2
FW Ver.:       20.39.5050       Qty.:      2
--------------------------------------------------
PSID: MT_0000000838 => CX-7 (NVIDIA, NDR IB 1-port OSFP)
--------------------------------------------------
FW Ver.:       28.36.1010       Qty.:      1
FW Ver.:       28.39.1002       Qty.:     22
FW Ver.:       28.39.3560       Qty.:      8
FW Ver.:       28.40.1000       Qty.:      8
FW Ver.:       28.41.1000       Qty.:   3562
FW Ver.:       28.42.1000       Qty.:     40
FW Ver.:       28.43.1014       Qty.:     71
FW Ver.:       28.43.2026       Qty.:     88
FW Ver.:       28.43.2566       Qty.:     40
FW Ver.:       28.44.1036       Qty.:     24
FW Ver.:       28.45.1020       Qty.:      8
FW Ver.:       28.46.1006       Qty.:      8
FW Ver.:       28.47.1026       Qty.:     16
--------------------------------------------------
PSID: MT_0000000970 => CX-7 (HPE, NDR InfiniBand 1-port OSFP)
--------------------------------------------------
FW Ver.:       28.45.1200       Qty.:   2034
--------------------------------------------------



No Invalid LID & Mcast LID found
##################################


LinkDowned Counters > 0 (Qt :150):
##################################################
         SrcDevice SrcPort            SrcGUID  LinkDownedCounter                                DstDevice DstPort            DstGUID
   5h-slg1-leaf-08       3 0xfc6a1c0300d58700                255                       run-pod-121 mlx5_4       1 0x9c63c00300756e8e
run-pod-121 mlx5_4       1 0x9c63c00300756e8e                255                          5h-slg1-leaf-08       3 0xfc6a1c0300d58700
   4h-slg2-leaf-01      20 0xfc6a1c0300d54fc0                255 MT4129 ConnectX7   Mellanox Technologies     N/A 0xa088c20300b479d2
   4h-slg7-leaf-01      20 0xfc6a1c0300d3f500                156 MT4129 ConnectX7   Mellanox Technologies     N/A 0xa088c20300b479be
     p2-slg7-leaf2      23 0xfc6a1c0300ba6dc0                 17                            zoho022 HCA-7       1 0x58a2e10300a7734e
     p2-slg1-leaf6       8 0xfc6a1c0300ba8f80                  7                            zoho010 HCA-1       1 0x58a2e10300a76fd6
     zoho010 HCA-1       1 0x58a2e10300a76fd6                  7                            p2-slg1-leaf6       8 0xfc6a1c0300ba8f80
     p2-slg8-leaf2      23 0xfc6a1c0300ba5e00                  3                            zoho022 HCA-8       1 0x58a2e10300a773be
     p1-slg4-leaf3       5 0xfc6a1c0300bf21c0                  2                            zoho031 HCA-4       1 0xa088c20300e01afe
     p1-slg4-leaf3       6 0xfc6a1c0300bf21c0                  2                            zoho032 HCA-6       1 0xa088c20300e67af8


XmitDidscard Counters > 0 (Qt :162)
##################################################
             SrcDevice SrcPort            SrcGUID  PortXmitDiscards                                DstDevice DstPort            DstGUID
bodhanai-node004 HCA-7       1 0x58a2e10300a783ce             29943                            p1-slg7-leaf3      22 0xfc6a1c0300ba7d40
       5h-slg1-leaf-08       3 0xfc6a1c0300d58700             15235                       run-pod-121 mlx5_4       1 0x9c63c00300756e8e
    run-pod-121 mlx5_4       1 0x9c63c00300756e8e             11646                          5h-slg1-leaf-08       3 0xfc6a1c0300d58700
       4h-slg2-leaf-01      20 0xfc6a1c0300d54fc0              5503 MT4129 ConnectX7   Mellanox Technologies     N/A 0xa088c20300b479d2
         p2-slg7-leaf2      23 0xfc6a1c0300ba6dc0              1916                            zoho022 HCA-7       1 0x58a2e10300a7734e
       4h-slg7-leaf-01      20 0xfc6a1c0300d3f500              1188 MT4129 ConnectX7   Mellanox Technologies     N/A 0xa088c20300b479be
         p2-slg8-leaf2      23 0xfc6a1c0300ba5e00               928                            zoho022 HCA-8       1 0x58a2e10300a773be
       4h-slg3-leaf-08      10 0xfc6a1c0300d39f00               169                  beta360-h100-023 mlx5_8       1 0xa088c203006e308c
       4h-slg5-leaf-08      10 0xfc6a1c0300f25cc0               169                  beta360-h100-023 mlx5_2       1 0xa088c203006e39ce
       4h-slg7-leaf-08      10 0xfc6a1c0300d3fbc0               169                  beta360-h100-023 mlx5_1       1 0xa088c203006e3a54


Port FEC Uncorrectable Counters (Qt :1290)
##################################################
       SrcDevice SrcPort            SrcGUID  PortFECUncorrectableBlockCounter              DstDevice DstPort            DstGUID
 5h-slg7-leaf-01      38 0xfc6a1c0300d56980                         169408964       5h-slg7-spine-02   1/1/2 0xfc6a1c0300f3b580
   p2-slg8-leaf8      32 0xfc6a1c0300bf3e00                          27337479 soketlab-node148 HCA-8       1 0x9c63c00300074bb4
 5h-slg3-leaf-06      30 0xfc6a1c0300d41040                          12043266      P5-HGX-190 mlx5_8       1 0x58a2e103001a5f4a
     core-cg7-07      18 0xfc6a1c0300bd0240                           3448266         p2-slg1-spine7  1/23/2 0xfc6a1c0300bf2300
   p2-slg8-leaf2      48 0xfc6a1c0300ba5e00                           2779708         p2-slg8-spine4   1/4/2 0xfc6a1c0300ba5d80
 5h-slg4-leaf-08      12 0xfc6a1c0300d41140                           1074364      run-pod-27 mlx5_9       1 0x9c63c003006b123a
   p2-slg3-leaf3       5 0xfc6a1c0300bf3700                            268541 kepler-h100-009 mlx5_4       1 0xa088c20300e01c36
5h-slg3-spine-01      11 0xfc6a1c0300f25ac0                            238215        5h-slg3-leaf-03  1/18/1 0xfc6a1c0300d41000
  p2-slg1-spine6      22 0xfc6a1c0300bf2640                            163886          p2-slg1-leaf6  1/27/2 0xfc6a1c0300ba8f80
 4h-slg8-leaf-03      25 0xfc6a1c0300f259c0                            157204    zoho-hpe-007 mlx5_3       1 0xa088c20300b48048


Buffer overrun Counters > 0 (Qt : 0):
##################################################

Max Retransmission_rate : > 500 (Qt : 0):
##################################################


Raw BER Counters > 1e-5 (Qt :93)
##################################################
             SrcDevice SrcPort            SrcGUID  RawBER              DstDevice DstPort            DstGUID
         p2-slg8-leaf8      32 0xfc6a1c0300bf3e00  0.0004 soketlab-node148 HCA-8       1 0x9c63c00300074bb4
       5h-slg3-leaf-06      30 0xfc6a1c0300d41040  0.0003      P5-HGX-190 mlx5_8       1 0x58a2e103001a5f4a
         p1-slg8-leaf8       4 0xfc6a1c0300bf28c0  0.0002 bm-p1-hgx-228 ibp193s0       1 0xa088c20300da1222
           core-cg7-07      18 0xfc6a1c0300bd0240  0.0002         p2-slg1-spine7  1/23/2 0xfc6a1c0300bf2300
           core-cg7-06      31 0xfc6a1c0300bd0280  0.0002         p2-slg8-spine7  1/22/1 0xfc6a1c0300ba5b80
       5h-slg7-leaf-01      38 0xfc6a1c0300d56980  0.0002       5h-slg7-spine-02   1/1/2 0xfc6a1c0300f3b580
      4h-slg1-spine-03      49 0xfc6a1c0300d58280  0.0002            core-cg3-09  1/17/1 0xfc6a1c0300bf3b80
         zoho010 HCA-1       1 0x58a2e10300a76fd6  0.0002          p2-slg1-leaf6       8 0xfc6a1c0300ba8f80
kepler-h100-013 mlx5_6       1 0xa088c20300e67868  0.0002          p2-slg5-leaf6      14 0xfc6a1c0300bd0640
         p2-slg5-leaf7      31 0xfc6a1c0300bd14c0  0.0001 kepler-h100-136 mlx5_6       1 0xa088c20300e02576


Effective BER Counters > 1e-13 (Qt :69)
##################################################
                 SrcDevice SrcPort            SrcGUID  EffectiveBER              DstDevice DstPort            DstGUID
             zoho010 HCA-1       1 0x58a2e10300a76fd6  5.000000e-06          p2-slg1-leaf6       8 0xfc6a1c0300ba8f80
           5h-slg7-leaf-01      38 0xfc6a1c0300d56980  2.000000e-07       5h-slg7-spine-02   1/1/2 0xfc6a1c0300f3b580
    kepler-h100-004 mlx5_8       1 0x58a2e10300a7a796  7.000000e-08          p2-slg7-leaf2       5 0xfc6a1c0300ba6dc0
             p2-slg8-leaf8      32 0xfc6a1c0300bf3e00  4.000000e-08 soketlab-node148 HCA-8       1 0x9c63c00300074bb4
    kepler-h100-067 mlx5_1       1 0xa088c20300d7ac7e  1.000000e-08          p1-slg2-leaf5      24 0xfc6a1c0300bf4700
simplismart-hpe-018 mlx5_2       1 0xa088c20300b48134  1.000000e-08        4h-slg5-leaf-01      25 0xfc6a1c0300d55100
           5h-slg3-leaf-06      30 0xfc6a1c0300d41040  1.000000e-08      P5-HGX-190 mlx5_8       1 0x58a2e103001a5f4a
               core-cg7-07      18 0xfc6a1c0300bd0240  5.000000e-09         p2-slg1-spine7  1/23/2 0xfc6a1c0300bf2300
               core-cg7-06      31 0xfc6a1c0300bd0280  4.000000e-09         p2-slg8-spine7  1/22/1 0xfc6a1c0300ba5b80
             p2-slg8-leaf2      48 0xfc6a1c0300ba5e00  4.000000e-09         p2-slg8-spine4   1/4/2 0xfc6a1c0300ba5d80


Symbol BER Counters > 1e-13, or Err > 0 (Qt :2)
##################################################
    SrcDevice SrcPort            SrcGUID    SymbolBER     DstDevice DstPort            DstGUID
zoho011 HCA-2       1 0x58a2e10300a77fe6 4.000000e-08 p2-slg2-leaf6      11 0xfc6a1c0300ba6c80
zoho010 HCA-1       1 0x58a2e10300a76fd6 1.000000e-12 p2-slg1-leaf6       8 0xfc6a1c0300ba8f80


Congestion Indexes > 10 (will be deprecated):
##################################################
               SrcDevice SrcPort            SrcGUID  PortXmitWaitExt  PortXmitPktsExtended  CongestionIndexExt                DstDevice DstPort            DstGUID
  bodhanai-node004 HCA-7       1 0x58a2e10300a783ce    1946012260056               7710530           252383.72            p1-slg7-leaf3      22 0xfc6a1c0300ba7d40
         5h-slg1-leaf-04       2 0xfc6a1c0300f3c7c0     128146224693             346471981              369.86 hyperbolic-node001 HCA-5       1 0x9c63c003006b10fa
         5h-slg3-leaf-04       2 0xfc6a1c0300d40fc0     127132787931             348279886              365.03 hyperbolic-node001 HCA-7       1 0x9c63c003006b1142
         5h-slg2-leaf-04       2 0xfc6a1c0300d40e80     126772937940             347677008              364.63 hyperbolic-node001 HCA-6       1 0x9c63c0030074d922
hyperbolic-node002 HCA-5       1 0x58a2e1030023570c     128029266583             351489404              364.25          5h-slg1-leaf-04       3 0xfc6a1c0300f3c7c0
         5h-slg4-leaf-04       2 0xfc6a1c0300d412c0     126381301640             348092458              363.07 hyperbolic-node001 HCA-8       1 0x9c63c0030074d83e
hyperbolic-node002 HCA-7       1 0x58a2e103002356e0     127046633362             353407916              359.49          5h-slg3-leaf-04       3 0xfc6a1c0300d40fc0
hyperbolic-node002 HCA-6       1 0x58a2e1030023571c     126672498997             352699579              359.15          5h-slg2-leaf-04       3 0xfc6a1c0300d40e80
hyperbolic-node002 HCA-8       1 0x58a2e1030022d094     126290446505             353219835              357.54          5h-slg4-leaf-04       3 0xfc6a1c0300d412c0
         5h-slg5-leaf-04       2 0xfc6a1c0300d58800     138797426694             501551269              276.74 hyperbolic-node001 HCA-4       1 0x9c63c0030074d95a


IB Device temperature > 70c or IB Switch Asic temperature > 70c (Qt : 783)
##################################################
          NodeGUID    NodeDesc  IbDeviceTemperature  SwitchAsicTemperature
0xfc6a1c0300ba85c0 core-cg7-15                 79.0                   79.0
0xfc6a1c0300bcf940 core-cg1-13                 79.0                   79.0
0xfc6a1c0300ba7940 core-cg2-07                 79.0                   79.0
0xfc6a1c0300ba79c0 core-cg2-08                 79.0                   79.0
0xfc6a1c0300bcf700 core-cg1-15                 79.0                   79.0
0xfc6a1c0300bd0300 core-cg7-12                 79.0                   79.0
0xfc6a1c0300bf2a00 core-cg5-10                 79.0                   79.0
0xfc6a1c0300bf2a80 core-cg5-13                 79.0                   79.0
0xfc6a1c0300ba8840 core-cg6-01                 79.0                   79.0
0xfc6a1c0300ba8dc0 core-cg6-08                 79.0                   79.0

PSU problem regarding (IsPresent, IsFRU, DCState, AlertState )
##################################################

Saving to Excel file:
##################################################

Data is written successfully to Excel File: C:\Python_3.13.3\Study\del\A.xlsx
```

