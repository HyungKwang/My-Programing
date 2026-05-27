## Intro

 This script gives a quick overview of Infiniband Fabric status based on ibdiagnet collection.
 This MD created based on my script v.39

 ### My script will defect and display defective items, which gives quick IB Fabric overview 

```
IB Switch Inventory Summary
##################################################

HCA Inventory Summary
##################################################

GPU Inventory Summary
##################################################

Invalid LID number or Mcast LID found 
##################################################

LinkDowned Counters > 0 
##################################################

XmitDidscard Counters > 0 
##################################################

Port FEC Uncorrectable Counters 
##################################################

Buffer overrun Counters > 0 
##################################################

Max Retransmission_rate : > 500 
##################################################

Raw BER Counters > 1e-5 (Qt :{len(df_Raw_ber.index)}) 
##################################################

Effective BER Counters > 1e-13 
##################################################

Symbol BER Counters > 1e-13, or Err > 0 
##################################################

Congestion Indexes > 10
##################################################

Lost Bandwidth Summary 
##################################################

Lost Bandwidth Summary 
##################################################

#######################################################################
###########   Fabric link Rate in details + Lost Bandwidth   ##########
####################################################################### 

(Tier1 & Tier4) Switch -> Servers By RX Bandwidth 
#######################################################################################

 (Tier1 & Tier4) Servers -> Switch By TX Bandwidth   
#######################################################################################

 (Tier2 & Tier3) Switch <-> Switch By RX Bandwidth
#######################################################################################

 (Tier2 & Tier3) Switch <-> Switch By TX Bandwidth
#######################################################################################

 All_port_TX_RX_Bandwidth Bandwidth
#######################################################################################

IB Device temperature > 70c or IB Switch Asic temperature > 70c 
##################################################

3rd Party Cable used 
##################################################

Cable Temperature > 70c
##################################################

PSU problem regarding (IsPresent, IsFRU, DCState, AlertState )
##################################################

APort Symmetry Check finished with errors 
##################################################

 Links Speed Check finished with errors 
##################################################

Rail Optimized Topology Validation ended with
##################################################

Saving to Excel file:
##################################################

```

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

<img width="1060" height="1870" alt="Image" src="https://github.com/user-attachments/assets/520bab03-0f91-4566-871e-0d5c59c6dbf6" />

