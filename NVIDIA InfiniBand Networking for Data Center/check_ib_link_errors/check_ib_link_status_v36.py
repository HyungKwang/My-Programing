# =============================================================================
# File name: check_ib_link_status_v10.py
# Description: check common errors and congestion indexes on all IB links
# Author: <.....> , HyungKwang Choi
# Software: Python 3.8+, Pandas and OpenPyXL Libraries
# Revision:
# v1  : 7/29/2021  Initial Draft by Jie
# v2  : 3/15/2022  modified by HyungKwang  Fixed (script bug (FEC Uncorrectable))
# v3  : 4/14/2022  modified by HyungKwang  Fixed (script bug (Symbol BER/Err))
# v4  : 4/30/2022  modified by HyungKwang  Modified (BER threshold from ‘1e-12’ to ‘1e-13’)
# v5  : 5/1/2022   modified by HyungKwang  Added ("Max Retransmission_rate")
# v5.1: 5/11/2022  modified by HyungKwang  Modifed ("Running command" parsing code)
# v6.1: 5/13/2022  modified by HyungKwang  & Sam Fixed (In the Ibdiagnet "2.8.1", ibdiagnet2_db.csv files , data written like "-1". Which triggers an exception such as) "PortXmitWaitExt = -1")
# v6.2: 5/26/2022  modified by HyungKwang  Added (the lib "is_integer_dtype" which help to distingush PortXmitWaitExt data Int and Hex)
# v7.2: 5/26/2022  modified by HyungKwang  Added ("Lost Bandwitdh")
# v8.2: 5/26/2022  modified by HyungKwang  Added ("Raw BER")
# v8.3: 6/13/2022  modified by HyungKwang  & Dan Fixed ("unsupported extended counters (in older FDR device and old SX6710 GW device)")
# v9.3: 6/14/2022  modified by HyungKwang  Added  "Switch -> Servers By RX Bandwidth, Switch <-> Switch By RX Bandwidth"
# v10 : 6/15/2022  modified by HyungKwang  Changed Script name to "check_ib_link_status_v10.py"
# v11 : 6/16/2022  modified by HyungKwang  Changed output layout of "Fabric link Rate in details + Lost Bandwidth"
# v12 : 6/22/2022  modified by HyungKwang  Changed some of output layout, and removed unused libarary.
# v13 : 3/20/2023  modified by HyungKwang  df_pm.replace({'LSA': {'FDR10':'14'}},  inplace = True)
# v14 : 4/20/2023  modified by HyungKwang  Added new function for "df_all_port_TX_RX_Bandwidth"
# v15 : 5/11/2023  modified by HyungKwang  Added new function for "Checking Invalid LID number"
# v16 : 5/15/2023  modified by HyungKwang  Modified lid_checkig syntax
# v17 : 5/16/2023  modified by HyungKwang  Fixed a bug about "Checking Invalid LID number"
# v18 : 6/28/2023  modified by HyungKwang  Fixed a bug about "Checking Invalid LID number"
# v19 : 1/25/2024  modified by HyungKwang  integrated existing script "show_ib_inventory.py" 
# v20 : 3/13/2024  modified by HyungKwang  Enhanced some code in case there is no FW/Node info of SWITCH/NODE_INFO exist in ibdiagnet.db_csv
# v21 : 3/28/2024  modified by HyungKwang  Fixed bug displaying 'NaN' in case "#N" in ibdiagnet.net_dump is string other than number.
# v22 : 3/31/2024  modified by HyungKwang  Added a new feature to analyze ibdiagnet.cable as well. For now, it analyze cable "Temperature > 70" 
# v23 : 4/1/2024   modified by HyungKwang  Fixing bugs on "N/A" at "Temperature " field 
# v24 : 4/1/2024   modified by HyungKwang  Added a new feature to check "3rd party cables"
# v25 : 4/9/2024   modified by HyungKwang  Modified the term of "3rd party used" -> "3rd Party Cable used" 
# v26 : 4/9/2024   modified by HyungKwang  fixing the bug "Port FEC Uncorrectable Counters (Qt :0) <====" which does not summation
# v27 : 5/28/2024  modified by HyungKwang  fixed "3rd Party Cable used" which supports the cable vendor NVIDIA
# v28 : 6/13/2024  modified by HyungKwang  modified the code 'writer.save() ->   writer.close()' which deprecated in Pandas
# v29 : 9/10/2024  modified by HyungKwang  added new parameter to avoid checking 3rd party cables. Because if IB network is scale, it takes much time to retrive cables info. 
# v30 : 9/21/2024  modified by HyungKwang  added new check items for IB devices & IB switch Asic temperature. 
# v31 : 9/25/2024  modified by HyungKwang  Removed HCA_inventory_Details, IB_Switch_Details excel sheet being saved.
# v32 : 12/09/2024  modified by HyungKwang  changed some syntax because if you run lastest Pandas (ex 2.2.3), it will dispaly 'future warnning' due some syntax will not support in latest Pandas. So updated.
#                                          Update lost bandwidth formula 10^9 => 1000000000...Please refer to how to calculate Lost Bandwidth
#                                           df_pm["Lost_Bandwidth(Gbps)"] = ( 
#                                                  df_pm["PortXmitWaitExt"] * 64 / (pm_pause_time_value * 1000000000)
#                                              )
#                                           https://docs.nvidia.com/networking/display/ibdiagnetusermanualv213/congestion+assessment+on+infiniband+links
#v33 : 12/18/2024  modified by HyungKwang correcting 'help' command outputs
#v34 : 5/26/2025  modified by HyungKwang modifying "df_pm["max_retransmission_rate"] = df_pm["max_retransmission_rate"].astype(str)"
#v35 : 5/28/2025  modified by HyungKwang added new regular expression to append '\n' " ibdgnt_net_file_appending_new_line_character = re.sub(r"((\"(.{1,255})\", \w+, (\w+), LID \d+))", r"\n\1", ibdgnt_net_file)"
#                  Details: Ibdiagnet latest version, if you open up 'ibdiagnet2.net_dump' file, between switch outputs, there is no 'new line character' such as) '\n'
#
#                 ex) from ibdiagnet2.net_dump
#                   1/32/2     : 64  : ACT  : LINK UP    : 5   : 4x      : 100     : MLNX_RS_271_257_PLR : NO-RTR : 0x9c63c00300c98966 : B36D0F0/0/0 : 421  : "Metal-Cloud-GPU-H100-2504159632 mlx5_1"
#                   N/A        : 65  : DOWN : POLL       : N/A : N/A     : N/A     : N/A                 : N/A    :                    :             :      :  <===========There is no 'new line character' such as) '\n'
#               "HAN02-P1-IB-SPINE-7", Mellanox, 0xfc6a1c0300f86080, LID 514                                                                                   <== So, next ibswitch info are directly attached without space. it makes my script wrong.               
#                   #          : IB# : Sta  : PhysSta    : MTU : LWA     : LSA     : FEC mode            : Retran : Neighbor Guid      : N#          : NLID : Neighbor Description
#                   1/1/1      : 1   : ACT  : LINK UP    : 5   : 4x      : 100     : MLNX_RS_271_257_PLR : NO-RTR : 0xb0cf0e0300d0af40 : 1/23/1      : 266  : "HAN02-P1-IB-LEAF-26"
# v36 : 6/20/2025  modified by HyungKwang  added new section to check  "PSU problem regarding ". Which check PSU status (IsPresent, IsFRU, DCState, AlertState)
#==================================================================================
#
# 
# 
#     Debugging commands
#===save PANDAS to csv==============================================================
#  df_pm.to_csv("data") 
#===save LIST to csv=============
#  f = open("data.csv", "w")
#  writer = csv.writer(f)
#  writer.writerows(data) 
#  f.close()
#
#with open('test.csv', 'w',newline='') as f: 
#      
#    # using csv.writer method from CSV package 
#    write = csv.writer(f) 
#    write.writerow(row) 
   
# =================================================================================
import csv
import argparse
import io
import os
import re
import pandas as pd
from pandas.api.types import is_integer_dtype

parser = argparse.ArgumentParser()
parser.add_argument(
    "-i", "--ibdiagnet-folder", required=True,
    help="read data from ibdiagnet2 output folder",
)
parser.add_argument(
    "-o", "--output-file",
    help="write results to xlsx file",
)
parser.add_argument(
    "-n", "--top-n",
    type=int, default="10",
    help="print first N entries(by default, n = 10)",
)

parser.add_argument(
    "-s", "--skip-lid-checking", action="store_true", 
    help="Skip Invalid LID & Mcast LID checking ",
)

parser.add_argument(
    "-c", "--skip-cable-checking", action="store_true", 
    help="reading ibdiagnet2.cables. if file size big, it takes much time. So, To skip cables checking",
)

parser.add_argument(
    "-a", "--all", action="store_true",
    help="Display all TX/RX Bandwidth & Lost Bandwidth in details ",
)

parser.add_argument(
    "-v", "--version", action="version", version="%(prog)s ",
    help="print current script version",
)
usage = parser.format_usage()
command1 = "\n\nExamples (How to run) > : \n\n  #python check_ib_link_status_v30.py -i ./tem/ibdiagnet2 \n"
command2 = "  #python check_ib_link_status_v30.py -i ./tem/ibdiagnet2 -a \n"
command3 = "  #python check_ib_link_status_v30.py -i ./tem/ibdiagnet2 -a -n 20 \n"
command4 = "  #python check_ib_link_status_v30.py -i ./tem/ibdiagnet2 -a -n 20 -o  C:\\Python39\\study\\save_backdata.xlsx \n"
command5 = "  #python check_ib_link_status_v30.py -i ./tem/ibdiagnet2 -a -n 20 -s -o C:\\Python39\\study\\save_backdata.xlsx \n"
command6 = "  #python check_ib_link_status_v30.py -i ./tem/ibdiagnet2 -a -n 20 -c -s -o C:\\Python39\\study\\save_backdata.xlsx \n"
parser.usage = usage.rstrip() + command1 + command2 + command3 + command4 + command5 + command6
args = parser.parse_args()

warn_return = []
temp_invalid_checking = True
if args.skip_lid_checking:
    temp_invalid_checking = False

ibdiagnet_cable_file_exist = True

if args.skip_cable_checking:
    ibdiagnet_cable_file_exist = False

Temperature_info_exist = False

###########################################################################################################################################################
########################## This is to check invalid LID number ############################################################################################

def check_Invalid_lid (ibdiagnet_discover) : 

    global warn_return                
        
    for i in ibdiagnet_discover :
        hi = i.split(" ")
        hi = [x for x in hi if x != '']
        i = i.replace("\n", "")
        for d, key in enumerate (hi):
            if key == 'lid':
        
                if  'DR' in hi[d+1] or 'lmc' in hi[d+1]  :
                    warn_return.append(i)
                    continue
                    
                try :        
                    temp_int = int(hi[d+1])
                except: 
                    warn_return.append(i)  
                    temp_int = 2   
                    pass
                                        
                if (temp_int < 1)  or (temp_int >= 65535) : 
                    warn_return.append(i)

                                        
                if  (temp_int > 49151) and (temp_int < 65535) :
                    warn_return.append(i)
              
######################################### End of the function #############################################################################################


###########################################################################################################################################################
########################## This is to extract cable link status ############################################################################################

def cable_tbl_extr(ibdiagnet_cable):

    """
    Extract all active links from ibdiagnet2.cables
    """

    cable_blk_regex = re.compile(
        r"Port=(\d+) Lid=\w+ GUID=(\w+) Port Name=.{1,255}\n"   # GRP 1: sw name  
        r"-{1,255}\n"      
        r"((.*\w+.*\n)+)"                           # GRP 2: link table
        r"^$\n",                                    # blank line
        re.MULTILINE,
    )

    cable_blocks = re.findall(cable_blk_regex, ibdiagnet_cable)
    df_cable_tbl = pd.DataFrame()
            
    for i in cable_blocks:
           
            # Load cable table

            df_cable_blk = pd.read_csv(io.StringIO(i[2]), sep=":", engine="python", dtype=str, names=["a","b"])


        #   df_cable_blk.columns = df_cable_blk.columns.str.strip()
            
            df_cable_blk.columns = df_cable_blk.columns.str.strip()    
            df_cable_blk = df_cable_blk.apply(
                lambda x: x.str.strip() if x.dtype == "object" else x
            )
    
            df_cable_blk.loc[65] = ['Cable_Portnum', i[0]]
            df_cable_blk.loc[66] = ['DeviceGuid', i[1]]

                    
            df_cable_blk=df_cable_blk.transpose()
        
            df_cable_blk.rename(columns=df_cable_blk.iloc[0],inplace=True)
            df_cable_blk = df_cable_blk.drop(df_cable_blk.index[0])
        
            df_cable_tbl = pd.concat([df_cable_tbl, df_cable_blk], ignore_index=True )


    df_cable_tbl.reset_index(drop=True, inplace=True)
    df_cable_tbl["Temperature"] = df_cable_tbl["Temperature"].str.replace("C","")       
   # df_cable_tbl["Temperature"].replace("N/A","0", inplace=True)
    df_cable_tbl["Temperature"] = df_cable_tbl["Temperature"].replace("N/A","0")
    
    df_cable_tbl["Temperature" ]=  pd.to_numeric(df_cable_tbl["Temperature" ])
        
    return df_cable_tbl


###########################################################################################################################################################
########################## This is to Load ibdiagnet.cables file ###########################################################################################

ibdgnt_cable = args.ibdiagnet_folder + "/ibdiagnet2.cables"


if os.path.isfile(ibdgnt_cable):
        with open(ibdgnt_cable, "r", encoding="utf-8", errors="ignore") as ibdiagnet_cable_file:
            ibdiagnet_cable = ibdiagnet_cable_file.read()

        df_ibdgnt_cable_tbl = cable_tbl_extr(ibdiagnet_cable)
    
else:     
    print("\nCouldn't find ibdiagnet2.cables file. Skiping cable status checking ...")
    ibdiagnet_cable_file_exist = False
                

###########################################################################################################################################################
########################## This is to extract ibdiagnet.net_dump###########################################################################################

def lnk_tbl_extr(ibdgnt_net_file):

    """
    Extract all active links from ibdiagnet2.net_dump
    """

    #+ =  one more
    # \w =  one word
    # \d = any number = [0-9]
    # * = repeat
    # re.MULTILINE =  all line by line matching
    # findall = return as a list which matches all with regular expression.
    #
    # Block starting line:
    # "MF0;<SW Name >:MQM8700/U1", Mellanox, 0xb8cef603001bf9de, LID 1

    ibdgnt_net_file_appending_new_line_character = re.sub(r"((\"(.{1,255})\", \w+, (\w+), LID \d+))", r"\n\1", ibdgnt_net_file)
  
    sw_blk_regex = re.compile(
        r"^\"(.{1,255})\", \w+, (\w+), LID \d+\n"   # GRP 1: sw name  
        r"((.*\w+.*\n)+)"                           # GRP 2: link table
        r"^$\n",                                    # blank line
        re.MULTILINE,
    )

    sw_blcks = re.findall(sw_blk_regex, ibdgnt_net_file_appending_new_line_character)  



    df_lnk_tbl = pd.DataFrame()

    # 1. Interate and concatenate swich blocks

    for i in sw_blcks:

        # Load link table

        df_sw_blk = pd.read_csv(io.StringIO(i[2]), sep=" :", engine="python", dtype=str)       
        df_sw_blk["SrcDevice"] = i[0]
        df_sw_blk["SrcGUID"] = i[1]

        # Clean up each switch block
        #str.strip()  # to remove empty space front and back
 
        df_sw_blk.columns = df_sw_blk.columns.str.strip()    
        df_sw_blk = df_sw_blk.apply(
            lambda x: x.str.strip() if x.dtype == "object" else x
        )     
        df_lnk_tbl = pd.concat([df_lnk_tbl, df_sw_blk])
   
    # 2. Remove down links

    df_lnk_tbl = df_lnk_tbl[df_lnk_tbl["Neighbor Description"].notnull()]

    df_lnk_tbl["Neighbor Description"] = (
        df_lnk_tbl["Neighbor Description"].str.replace("\"", "")
    )


    # 3. Remove SHARP AN

    SHARP_AN = "Mellanox Technologies Aggregation Node"

    df_lnk_tbl = df_lnk_tbl[
        df_lnk_tbl["Neighbor Description"] != SHARP_AN
    ]

    # 4 To replace Neighbor port number string ex "B141D0F0/0/0" , "B148D0F0" to all "1"
    df_lnk_tbl["N#"] = df_lnk_tbl["N#"].map(lambda x: 1 if 'B' in x else x) 

    # 5. Finalize link table DF

    df_lnk_tbl.rename(
        columns={
            "IB#": "SrcPort",
            "Neighbor Description": "DstDevice",
            "N#": "DstPort",
            "Neighbor Guid": "DstGUID",
        },
        inplace=True,
    )

    df_lnk_tbl = df_lnk_tbl[
        ["SrcDevice", "SrcPort", "SrcGUID", "LWA","LSA","DstDevice", "DstPort", "DstGUID"]
    ]

    df_dup_lnks = pd.DataFrame()

    df_dup_lnks[
        ["SrcDevice", "SrcPort", "SrcGUID", "LWA","LSA", "DstDevice", "DstPort", "DstGUID"]
    ] = df_lnk_tbl[
        ["DstDevice", "DstPort", "DstGUID","LWA","LSA", "SrcDevice", "SrcPort", "SrcGUID"]
    ]

    df_full_lnk_tbl = pd.concat([df_lnk_tbl, df_dup_lnks])
 
 
    df_full_lnk_tbl.drop_duplicates(
        subset=["SrcGUID", "SrcPort"],
        inplace=True,
    )

    # 6. Add leading 0 if GUID length < 16 hex numbers

    df_full_lnk_tbl["SrcGUID"] = df_full_lnk_tbl["SrcGUID"].apply(lambda x: "0x" + x.lstrip("0x").zfill(16))
    df_full_lnk_tbl["DstGUID"] = df_full_lnk_tbl["DstGUID"].apply(lambda x: "0x" + x.lstrip("0x").zfill(16))
    df_full_lnk_tbl["LWA"] = df_full_lnk_tbl["LWA"].apply(lambda x: x.rstrip("x"))

    df_full_lnk_tbl.reset_index(drop=True, inplace=True)
    return df_full_lnk_tbl


###########################################################################################################################################################
########################## This is to Load ibdiagnet2.net_dump                                   ##########################################################

ibdgnt_net = args.ibdiagnet_folder + "/ibdiagnet2.net_dump"

if os.path.isfile(ibdgnt_net):

    with open(ibdgnt_net, "r", encoding="utf-8", errors="ignore") as net_file:
        net_dump = net_file.read()

    df_ibdgnt_lnk_tbl = lnk_tbl_extr(net_dump)


else:
    print("\nCouldn't find ibdiagnet2.net_dump. Existing ...")
    exit()


###########################################################################################################################################################
########################## This is to extract ibdiagnet.db_csv ############################################################################################

def db_csv_extr(separator, ibdgnt_db_csv_file):

    """
    Extract each csv table within ibdiagnet2.db_csv
    """

    # search csv tables

    regexp = re.compile(
        r"^START_" + separator + r"$\n"         # starting separator
        r"((.*\n)+)"                            # csv table
        r"^END_" + separator + r"$\n",          # ending separator
        re.MULTILINE                            # All line by line matching.
    )

    regexp_result = re.search(regexp, ibdgnt_db_csv_file)
    
    if regexp_result:
        return pd.read_csv(io.StringIO(regexp_result.group(1)), low_memory=False)
    else:
        return pd.DataFrame()


###########################################################################################################################################################
########################## This is to extract ibdiagnet.net_ext############################################################################################

def net_ext_extr(ibdgnt_net_ext_file):

    """
    Extract data from ibdiagnet2.net_dump_ext
    """

    regexp = re.compile(r"(Ty.*)", re.DOTALL)

    regexp_result = re.search(regexp, ibdgnt_net_ext_file)

    if regexp_result:

        df_net_dump = pd.read_csv(
            io.StringIO(regexp_result.group(1)),
            encoding="utf-8",
            sep=" :",
            engine="python",
            dtype=str,
        )

        df_net_dump.columns = df_net_dump.columns.str.strip()
        df_net_dump = df_net_dump.apply(
            lambda x: x.str.strip() if x.dtype == "object" else x
        )

        return df_net_dump

    else:
        return pd.DataFrame()

###########################################################################################################################################################
########################## This is to load ibdiagnet2.log###### ############################################################################################

ibdgnt_log = args.ibdiagnet_folder + "/ibdiagnet2.log"

if os.path.isfile(ibdgnt_log):

    with open(ibdgnt_log, "r", encoding="utf-8", errors="ignore") as log_file:

        while True:
            running_command_only = log_file.readline()
        
            if "Running command:"  in running_command_only : break
            if "Running:"  in running_command_only : break

        print('\n{} '.format(running_command_only) )
    


else:
    print("\nCouldn't find ibdiagnet2.log. Existing ...")
    exit()


###########################################################################################################################################################
########################## This is to load ibdiagnet2.ibnetdiscover                              ##########################################################
##########################"temp_invalid_checking = True" is important to run this feature or not ##########################################################

if temp_invalid_checking :
    ibdgnt_discover = args.ibdiagnet_folder + "/ibdiagnet2.ibnetdiscover"

    if os.path.isfile(ibdgnt_discover):
        with open(ibdgnt_discover, "r", encoding="utf-8", errors="ignore") as discover_file:
            discover_dump = discover_file.readlines()

            check_Invalid_lid(discover_dump)

    else:     
        print("\nCouldn't find ibdiagnet2.discover. Skiping Invalid LID checking ...")
        temp_invalid_checking = False


###########################################################################################################################################################
########################## This is to Load ibdiagnet2.db_csv                                     ##########################################################

ibdgnt_db = args.ibdiagnet_folder + "/ibdiagnet2.db_csv"

if os.path.isfile(ibdgnt_db):

    with open(ibdgnt_db, "r", encoding="utf-8", errors="ignore") as db_csv_file:
        db_csv = db_csv_file.read()

    # Extract PM CSV table from ibdiagnet2.db_csv

    df_pm = db_csv_extr("PM_INFO", db_csv)
    df_nodes_tbl = db_csv_extr("NODES", db_csv)
    df_power_supplies_tbl = db_csv_extr("POWER_SUPPLIES", db_csv)


    if not df_nodes_tbl.empty :
        df_nodes_tbl = df_nodes_tbl[["NodeGUID", "NodeDesc"]]        
        # 1.2 Extract NODES_INFO CSV table from ibdiagnet2.db_csv
    else:
        print(f"\nWARN: Couldn't find START_NODES info info in ibdiagnet2.db_csv.")
    
    
    if not df_power_supplies_tbl.empty :
        df_power_supplies_tbl = df_power_supplies_tbl[["NodeGuid","PSUIndex","IsPresent","IsFRU","ACInput","DCState","AlertState","FanState","TemperatureState","SerialNumber"]]
        
    else:
        print(f"\nWARN: Couldn't find START_POWER_SUPPLIES info in ibdiagnet2.db_csv.")
        
        
    df_nodes_info_tbl = db_csv_extr("NODES_INFO", db_csv)

    if not df_nodes_info_tbl.empty :
            df_nodes_info_tbl["FWInfo_Version"] = (
                df_nodes_info_tbl["FWInfo_Extended_Major"].apply(int, base=16).astype(str) + "."
                + df_nodes_info_tbl["FWInfo_Extended_Minor"].apply(int, base=16).astype(str) + "."
                + df_nodes_info_tbl["FWInfo_Extended_SubMinor"].apply(int, base=16).astype(str)
            )
            df_nodes_info_tbl = df_nodes_info_tbl[["NodeGUID", "FWInfo_PSID", "FWInfo_Version"]]

    else:
        print(f"\nWARN: Couldn't find START_NODE_INFO info info in ibdiagnet2.db_csv.")
    # 1.3 Extract SWITCHES CSV table from ibdiagnet2.db_csv

    df_sw_tbl = db_csv_extr("SWITCHES", db_csv)
    if not df_sw_tbl.empty : 
        df_sw_tbl = df_sw_tbl[["NodeGUID"]]

    # 1.4 Extract SYSTEM_GENERAL_INFORMATION CSV table from ibdiagnet2.db_csv
    else:
        print(f"\nWARN: Couldn't find START_SWITCHES info info in ibdiagnet2.db_csv.")


    df_sw_info_tbl = db_csv_extr("SYSTEM_GENERAL_INFORMATION", db_csv)
 

    # Extract Switch Asic temperature CSV table from ibdiagnet2.db_csv
    df_switch_asic_temperature = db_csv_extr("TEMPERATURE_SENSORS", db_csv)

    if not df_switch_asic_temperature.empty :
        df_switch_asic_temperature = df_switch_asic_temperature[["NodeGuid", "Temperature"]]
    else:
        print(f"\nWARN: Couldn't find START_TEMPERATURE_SENSORS info in ibdiagnet2.db_csv.")


    # Extract All IB device Temperature CSV table from ibdiagnet2.db_csv. This is not switch Asic Temperature
    df_ib_device_temperature = db_csv_extr("TEMP_SENSING", db_csv)

    if not df_ib_device_temperature.empty :
        df_ib_device_temperature = df_ib_device_temperature[["NodeGUID", "CurrentTemperature"]]

    else:
        print(f"\nWARN: Couldn't find START_TEMP_SENSING info in ibdiagnet2.db_csv.")
    
else:
    print("\nCouldn't find ibdiagnet2.db_csv. Existing ...")
    exit()

###########################################################################################################################################################
########################## This is to Load ibdiagnet2.net_dump_ext                                ##########################################################

ibdgnt_net_ext = args.ibdiagnet_folder + "/ibdiagnet2.net_dump_ext"

if os.path.isfile(ibdgnt_net_ext):

    with open(ibdgnt_net_ext, "r", encoding="utf-8", errors="ignore") as net_dump_file:
        net_dump = net_dump_file.read()

    df_ibdgnt_net_ext = net_ext_extr(net_dump)

else:
    print(f"\n\nCouldn't find ibdiagnet2.net_dump_ext. Existing ...")
    exit()


###########################################################################################################################################################
########################## This is to check IB inventory such as) switch/HCA fw version and Quantity.######################################################

#  1. Generate IB switch inventory table

#  1.1 Extract NodeDesc
if not df_nodes_info_tbl.empty and not df_sw_tbl.empty and not df_sw_info_tbl.empty: 

    df_sw_tbl = pd.merge(
        left=df_sw_tbl, right=df_nodes_tbl, on="NodeGUID"
    )

    #  Extract FWInfo_PSID & FWInfo_Version

    df_sw_tbl = pd.merge(
        left=df_sw_tbl, right=df_nodes_info_tbl, on="NodeGUID"
    )

# 1.2Extract PartNumber, Revision and SerialNumber if section SYSTEM_GENERAL_INFORMATION exists

if df_sw_info_tbl.empty:
    print(
        f"\nINFO: SYSTEM_GENERAL_INFORMATION section couldn't be found in ibdiagnet2.db_csv.",
        f"\nINFO: It's impossible to display detailed SW info, such as PN, SN and HW RN.",
    )

    if not df_nodes_info_tbl.empty and not df_sw_tbl.empty and not df_sw_info_tbl.empty: 
        df_sw_tbl = df_sw_tbl[["NodeDesc", "NodeGUID", "FWInfo_PSID", "FWInfo_Version"]]

else:

    if not df_nodes_info_tbl.empty and not df_sw_tbl.empty and not df_sw_info_tbl.empty: 

        df_sw_tbl = pd.merge(
            left=df_sw_tbl, right=df_sw_info_tbl,
            left_on="NodeGUID", right_on="NodeGuid",
            how="left",
        )

        df_sw_tbl = df_sw_tbl[
            [
                "NodeDesc",
                "NodeGUID",
                "FWInfo_PSID",
                "FWInfo_Version",
                "PartNumber",
                "Revision",
                "SerialNumber",
            ]
        ]

        df_sw_tbl.sort_values(by="NodeDesc", inplace=True)

  #  2. Generate SW pivot table

        df_ib_sw_pivot = pd.pivot_table(
            df_sw_tbl, index="FWInfo_PSID", columns="FWInfo_Version", aggfunc="size"
        )

#  3. Generate HCA inventory table

# 3.1 Extract NodeDesc
if not df_nodes_info_tbl.empty and not df_sw_tbl.empty and not df_sw_info_tbl.empty: 
    df_hca_tbl = pd.merge(
        left=df_nodes_info_tbl, right=df_nodes_tbl,
        left_on="NodeGUID", right_on="NodeGUID"
    )

    # 3.2 Remove SHArP AN from df_hca_tbl

    SHARP_AN = "Mellanox Technologies Aggregation Node"
    df_hca_tbl = df_hca_tbl[df_hca_tbl["NodeDesc"] != SHARP_AN]

    # 3.3 Remove IB switches from df_hca_tbl

    if not df_sw_tbl.empty:
        df_hca_tbl = df_hca_tbl[~df_hca_tbl["NodeGUID"].isin(df_sw_tbl["NodeGUID"])]

    # 3.4 Split NodeDesc into host and port names, then sort by them


    df_hca_tbl[["HostName", "PortNum"]] = df_hca_tbl["NodeDesc"].str.rsplit(
        " ", n=1, expand=True
    )
    df_hca_tbl = df_hca_tbl[
           [
            "HostName",
            "PortNum",
            "NodeGUID",
            "FWInfo_PSID",
            "FWInfo_Version",
           ]
        ]
    df_hca_tbl.sort_values(by=["HostName", "PortNum"], inplace=True)

        # 3.5 Generate HCA pivot table

    df_hca_pivot = pd.pivot_table(
        df_hca_tbl, index="FWInfo_PSID", columns="FWInfo_Version", aggfunc="size"
    )


###########################################################################################################################################################
########################## This is to create Data Frame for Asic temperature and IB device temperature#####################################################

#  1. Generate IB switch inventory table

#  1.1 Extract NodeDesc
if not df_nodes_tbl.empty and not df_ib_device_temperature.empty and not df_switch_asic_temperature.empty: 

    df_nodes_temperature = pd.merge(
        left=df_nodes_tbl, right=df_ib_device_temperature, on="NodeGUID" , how="left"
    )


    df_switch_asic_temperature.rename(
        columns={
                "NodeGuid": "NodeGUID",
                    },
                inplace=True,
            )

    df_nodes_temperature = pd.merge(
        left=df_nodes_temperature, right=df_switch_asic_temperature, on="NodeGUID", how="left"
    )

    # Remove Aggregation Node temperature

    df_nodes_temperature.rename(
        columns={
                "CurrentTemperature": "IbDeviceTemperature",
                "Temperature": "SwitchAsicTemperature"
                    },
                inplace=True,
            )
    
    df_nodes_temperature = df_nodes_temperature[
        df_nodes_temperature["NodeDesc"] != "Mellanox Technologies Aggregation Node"
    ]

    if not df_nodes_temperature.empty: 
     Temperature_info_exist = True

###########################################################################################################################################################

"""
    # Step 6. Check PM counters
"""

if not df_pm.empty:

    df_pm.rename(
        columns={
            " max_retransmission_rate": "max_retransmission_rate",
        },
        inplace=True,
    )

    df_pm["max_retransmission_rate"] = df_pm["max_retransmission_rate"].astype(str)  #sometimes, when ibdiagnet has all "-1" of max_retransmission_rate', it returns an error due to astype at the code 
                                                                                     # "df_pm["max_retransmission_rate"] = df_pm["max_retransmission_rate"].apply(int, base=16)" So, This is to avoid dtype issue

    df_pm["PortNumber"] = df_pm["PortNumber"].astype(str)
    df_ibdgnt_lnk_tbl["SrcPort"] = df_ibdgnt_lnk_tbl["SrcPort"].astype(str)
 
    df_pm = pd.merge(
        left=df_pm,
        right=df_ibdgnt_lnk_tbl,
        left_on=["NodeGUID", "PortNumber"],
        right_on=["SrcGUID", "SrcPort"],
        how="left",
    )

    if ibdiagnet_cable_file_exist :   #If ibdiagnet2.cables file exists
  
    #    df_ibdgnt_lnk_tbl["Cableportnum"] = df_ibdgnt_lnk_tbl["Cableportnum"].astype(str)
   
        df_pm = pd.merge(
            left=df_pm,
            right=df_ibdgnt_cable_tbl,
            left_on=["NodeGUID", "PortNumber"],
            right_on=["DeviceGuid", "Cable_Portnum"],
            how="left",
        )
                           
        df_cable_all = df_pm.copy()
        cable_cols = [
            "SrcDevice",
            "SrcPort",
            "SrcGUID",
            "Vendor",
            "PN",
            "SN",
            "Temperature",
            "DstDevice",
            "DstPort",
            "DstGUID",
        ]
        df_cable_all = df_cable_all[cable_cols]
        df_cable_all.dropna(subset=["SrcDevice"], inplace=True)

    # 5.1 LinkDownedCounter

    df_pm = df_pm[df_pm["LWA"] != ""]
    df_pm = df_pm[df_pm["LSA"] != ""]


    if "--extended_speeds all" in running_command_only :    
        pm_cols = [
            "SrcDevice",
            "SrcPort",
            "SrcGUID",
            "DstDevice",
            "DstPort",
            "DstGUID",
            "LinkDownedCounter",
            "PortXmitDiscards",
            "PortXmitWait",
            "PortXmitWaitExt",
            "PortXmitPktsExtended",
            "ExcessiveBufferOverrunErrors",
            "PortFECUncorrectableBlockCounter",
            "max_retransmission_rate",
            "PortRcvData",
            "PortXmitData",
            "PortRcvDataExtended",
            "PortXmitDataExtended",
            "LWA",
            "LSA",
        ]


    else :  
        pm_cols = [
            "SrcDevice",
            "SrcPort",
            "SrcGUID",
            "DstDevice",
            "DstPort",
            "DstGUID",
            "LinkDownedCounter",
            "PortXmitDiscards",
            "PortXmitWait",
            "PortXmitWaitExt",
            "PortXmitPktsExtended",
            "ExcessiveBufferOverrunErrors",
            "max_retransmission_rate",
            "PortRcvData",
            "PortXmitData",
            "PortRcvDataExtended",  
            "PortXmitDataExtended",
            "LWA",
            "LSA",
        ]



    df_pm = df_pm[pm_cols]



    df_lnk_dn = df_pm[df_pm["LinkDownedCounter"] > 0]
    df_lnk_dn = df_lnk_dn[
        ["SrcDevice", "SrcPort", "SrcGUID", "LinkDownedCounter", "DstDevice", "DstPort", "DstGUID"]
    ]
    df_lnk_dn = df_lnk_dn.sort_values(by="LinkDownedCounter", ascending=False)

    # 5.2 PortXmitDiscards

    df_xmit_drp = df_pm[df_pm["PortXmitDiscards"] > 0]
    df_xmit_drp = df_xmit_drp[
        ["SrcDevice", "SrcPort", "SrcGUID", "PortXmitDiscards", "DstDevice", "DstPort","DstGUID"]
    ]
    df_xmit_drp = df_xmit_drp.sort_values(by="PortXmitDiscards", ascending=False)

    # 5.3 PortFECUncorrectableBlockCounter
 

    if "extended_speeds" in running_command_only :
        df_fec_uncorrectable = df_pm[df_pm["PortFECUncorrectableBlockCounter"] > 0]
        df_fec_uncorrectable = df_fec_uncorrectable[
            ["SrcDevice", "SrcPort", "SrcGUID", "PortFECUncorrectableBlockCounter", "DstDevice","DstPort","DstGUID"]
        ]
        df_fec_uncorrectable = df_fec_uncorrectable.sort_values(
            by="PortFECUncorrectableBlockCounter", ascending=False
        )

    # 5.4 ExcessiveBufferOverrunErrors

    df_buf_overrun = df_pm[df_pm["ExcessiveBufferOverrunErrors"] != 0]
    df_buf_overrun = df_buf_overrun[
        ["SrcDevice", "SrcPort", "SrcGUID", "ExcessiveBufferOverrunErrors", "DstDevice", "DstGUID", "DstPort"]
    ]
    df_buf_overrun = df_buf_overrun.sort_values(
        by="ExcessiveBufferOverrunErrors", ascending=False
    )
     
    """
     Old FDR or SX6710 does not support PortXmitWaitExt. so writes unrealistic value '0xfffffffffffffffe' to ibdiagnet2.db_csv
    ("unsupported extended counters (in older FDR device and old SX6710 GW device))
    So for that, below code needed.
     
    """  
  #  df_pm["PortXmitWaitExt"].replace('0xfffffffffffffffe', '0x0000000000000000', inplace=True) 
    
    df_pm["PortXmitWaitExt"] = df_pm["PortXmitWaitExt"].replace('0xfffffffffffffffe', '0x0000000000000000')  
    
    if (not is_integer_dtype(df_pm["PortXmitWaitExt"])) : 



        df_pm["PortXmitWaitExt"] = df_pm["PortXmitWaitExt"].apply(int, base=16)
        df_pm["PortXmitPktsExtended"] = df_pm["PortXmitPktsExtended"].apply(int, base=16)


  
        """
        df=pd.DataFrame({ 'a':[52894036999, 78893201999, 45790373999] })
        df['b'] = df['a'].apply( hex )
        df['c'] = df['b'].apply( int, base=0 )
        Results:

                    a             b            c
        0  52894036999   0xc50baf407  52894036999
        1  78893201999  0x125e66ba4f  78893201999
        2  45790373999   0xaa951a86f  45790373999
    
        """
  
  
    # 5.5 CongestionIndex
    try:
        # In the Ibdiagnet "2.8.1", ibdiagnet2_db.csv files , data written like "-1". Which triggers an exception such as) "PortXmitWaitExt = -1"

        df_pm["CongestionIndexExt"] = (
         df_pm["PortXmitWaitExt"] / df_pm["PortXmitPktsExtended"]
        )
    
    except ZeroDivisionError:
        df_pm["CongestionIndexExt"] = 0


    df_pm["CongestionIndexExt"] = df_pm["CongestionIndexExt"].round(2)
    df_congestion_ext = df_pm[df_pm["CongestionIndexExt"] >= 10]

    df_congestion_ext = df_congestion_ext[
        ["SrcDevice", "SrcPort", "SrcGUID", "PortXmitWaitExt", "PortXmitPktsExtended", "CongestionIndexExt", "DstDevice","DstPort", "DstGUID"]
    ]
    df_congestion_ext = df_congestion_ext.sort_values(
        by="CongestionIndexExt", ascending=False
    )

    # 5.6 max_retransmission_rate (threshold 500)
    
    df_pm["max_retransmission_rate"] = df_pm["max_retransmission_rate"].apply(int, base=16)      #to convert hex 16 digits (0x0000) to int   
    df_max_retrans = df_pm[df_pm["max_retransmission_rate"] > 500]
    df_max_retrans = df_max_retrans[
        ["SrcDevice", "SrcPort", "SrcGUID", "max_retransmission_rate", "DstDevice", "DstGUID", "DstPort"]
    ]
    df_max_retrans = df_max_retrans.sort_values(
        by="max_retransmission_rate", ascending=False
    )   

    if "--pm_pause_time" in running_command_only :
            pm_pause_time = running_command_only.split()

            index = pm_pause_time.index("--pm_pause_time")
            pm_pause_time_value = int(pm_pause_time[index + 1])
    
    # 5.7 Lost BandWidth

            df_pm["Lost_Bandwidth(Gbps)"] = ( 
                df_pm["PortXmitWaitExt"] * 64 / (pm_pause_time_value * 1000000000)
            )

            df_pm["Lost_Bandwidth(Gbps)"] = df_pm["Lost_Bandwidth(Gbps)"].round(2)   

            df_pm = df_pm.dropna(how='any')
            df_pm = df_pm.astype({'LWA':'float', 'LSA':'float'})        

            df_pm.replace({'LSA': {'FDR10':'14'}},  inplace = True)
            
    ###Congestion BW percentage.
            """
             Below for new feature "Congestion BW percentage." in the feature. But in current version this feature is not implemented. 
             just logic added. and the logic works. but not displays.
     
            """  
    
            df_pm["Link_active_speed"] = ( 
                df_pm["LWA"] * df_pm["LSA"] 
            )
     
            df_pm["Congestion_BW_Percentage"] =  ( 
                (df_pm["Lost_Bandwidth(Gbps)"] * 100) / 64 * df_pm["LWA"] * df_pm["LSA"]
            )
     
    ###Recevie & Transmit Bandwidth
    
            df_pm["PortRcvData"] = df_pm["PortRcvData"].apply(lambda x : format(x,"#018x"))
            df_pm["PortRcvData"] = df_pm["PortRcvData"].astype('object')
      

            df_pm["PortXmitData"] = df_pm["PortXmitData"].apply(lambda x : format(x,"#018x"))
            df_pm["PortXmitData"] = df_pm["PortXmitData"].astype('object')
                                       
            if (not is_integer_dtype(df_pm["PortRcvDataExtended"])) : 
                                
                mask = df_pm["PortRcvDataExtended"] == '0xfffffffffffffffe'
                df_pm.loc[mask, 'PortRcvDataExtended'] = df_pm.loc[mask, 'PortRcvData'] 
                
                df_pm["PortRcvDataExtended"] = df_pm["PortRcvDataExtended"].apply(int, base=16)

            if (not is_integer_dtype(df_pm["PortXmitDataExtended"])) : 
                
                mask = df_pm["PortXmitDataExtended"] == '0xfffffffffffffffe'
                df_pm.loc[mask, 'PortXmitDataExtended'] = df_pm.loc[mask, 'PortXmitData'] 
 
                df_pm["PortXmitDataExtended"] = df_pm["PortXmitDataExtended"].apply(int, base=16)

            df_pm["PortRcvDataExtended(Gbps)"] = ( 
                df_pm["PortRcvDataExtended"] * 32 / (pm_pause_time_value * 1000000000)
            )

            df_pm["PortXmitDataExtended(Gbps)"] = ( 
                df_pm["PortXmitDataExtended"] * 32 / (pm_pause_time_value * 1000000000)
            )

            df_pm["PortRcvDataExtended(Gbps)"]  = df_pm["PortRcvDataExtended(Gbps)"] .round(2)
            df_pm["PortXmitDataExtended(Gbps)"]  = df_pm["PortXmitDataExtended(Gbps)"] .round(2)

            df_all_port_TX_RX_Bandwidth = df_pm.copy()
    
           
            df_Server_Rx_Bandwidth = df_pm[(df_pm["PortRcvDataExtended(Gbps)"] > 0) & (df_pm["SrcDevice"].str.contains("HCA|mlx|Connect",case=False)) ] 
            df_Server_Tx_Bandwidth = df_pm[(df_pm["PortXmitDataExtended(Gbps)"] > 0) & (df_pm["SrcDevice"].str.contains("HCA|mlx|Connect",case=False)) ]

            
            df_Switch_Rx_Bandwidth = df_pm[(df_pm["PortRcvDataExtended(Gbps)"] > 0) & (df_pm["SrcDevice"].str.contains("HCA|mlx|Connect",case=False)==0)& (df_pm["DstDevice"].str.contains("HCA|mlx|Connect",case=False)==0) ] 
            df_Switch_Tx_Bandwidth = df_pm[(df_pm["PortXmitDataExtended(Gbps)"] > 0) & (df_pm["SrcDevice"].str.contains("HCA|mlx|Connect",case=False)==0)& (df_pm["DstDevice"].str.contains("HCA|mlx|Connect",case=False)==0) ]



        #5.8 (Tier1 & Tier4) Switch -> Servers By RX Bandwidth (Gbps)
            df_Server_Rx_Bandwidth = df_Server_Rx_Bandwidth[
            ["DstDevice", "DstPort", "DstGUID", "PortRcvDataExtended(Gbps)","Lost_Bandwidth(Gbps)", "SrcDevice", "SrcPort", "SrcGUID"]
            ]      

            df_Server_Rx_Bandwidth.rename(
                columns={
                    "DstDevice": "SrcSwitch",
                    "DstGUID": "SrcGUID",
                    "DstPort": "SrcPort",
                    "SrcDevice": "DstServer",
                    "SrcPort": "DstPort",
                    "SrcGUID": "DstGUID",
                    "PortRcvDataExtended(Gbps)":"RX_BW(Gbps)",
                    "Lost_Bandwidth(Gbps)":"Lost_BW(Gbps)",
                    },
                inplace=True,
            )
       

            df_Server_Rx_Bandwidth = df_Server_Rx_Bandwidth.sort_values(by="Lost_BW(Gbps)", ascending=False)
       
   
        #5.9 (Tier1 & Tier4) Servers -> Switch By TX Bandwidth (Gbps)
            df_Server_Tx_Bandwidth = df_Server_Tx_Bandwidth[
            ["SrcDevice", "SrcPort", "SrcGUID", "PortXmitDataExtended(Gbps)","Lost_Bandwidth(Gbps)" , "DstDevice", "DstPort", "DstGUID" ]
            ]      
        
            df_Server_Tx_Bandwidth.rename(
                columns={
                    "DstDevice": "DstSwitch",
                    "SrcDevice": "SrcServer",
                    "PortXmitDataExtended(Gbps)":"TX_BW(Gbps)",
                    "Lost_Bandwidth(Gbps)":"Lost_BW(Gbps)",
                    },
                inplace=True,
            )

            df_Server_Tx_Bandwidth = df_Server_Tx_Bandwidth.sort_values(by="Lost_BW(Gbps)", ascending=False)

 

        #5.10 (Tier2 & Tier3) Switch <-> Switch By RX Bandwidth (Gbps)
            df_Switch_Rx_Bandwidth = df_Switch_Rx_Bandwidth[
            [ "SrcDevice", "SrcPort", "SrcGUID","PortRcvDataExtended(Gbps)","Lost_Bandwidth(Gbps)" , "DstDevice", "DstPort", "DstGUID",]
            ]      

            df_Switch_Rx_Bandwidth.rename(
                columns={
                    "DstDevice": "DstSwitch",
                    "SrcDevice": "SrcSwitch",
                    "PortRcvDataExtended(Gbps)":"RX_BW(Gbps)",
                    "Lost_Bandwidth(Gbps)":"Lost_BW(Gbps)",
                    },
                inplace=True,
            )

            df_Switch_Rx_Bandwidth = df_Switch_Rx_Bandwidth.sort_values(by="Lost_BW(Gbps)", ascending=False)
       
        #5.11 (Tier2 & Tier3) Switch <-> Switch By TX Bandwidth (Gbps)
            df_Switch_Tx_Bandwidth = df_Switch_Tx_Bandwidth[
            [ "SrcDevice", "SrcPort", "SrcGUID","PortXmitDataExtended(Gbps)","Lost_Bandwidth(Gbps)" , "DstDevice", "DstPort", "DstGUID",]
            ]      

            df_Switch_Tx_Bandwidth.rename(
                columns={
                    "DstDevice": "DstSwitch",
                    "SrcDevice": "SrcSwitch",
                    "PortXmitDataExtended(Gbps)":"TX_BW(Gbps)",
                    "Lost_Bandwidth(Gbps)":"Lost_BW(Gbps)",
                    },
                inplace=True,
            )

            df_Switch_Tx_Bandwidth = df_Switch_Tx_Bandwidth.sort_values(by="Lost_BW(Gbps)", ascending=False)
       
     
         ### "5.7 Lost BandWidth" logic implemented here
  
            df_Lost_Bandwidth = df_pm[df_pm["Lost_Bandwidth(Gbps)"] > 0].copy()
 
            df_Lost_Bandwidth["Current_TX_BW(Gbps)"] =  df_Lost_Bandwidth["PortXmitDataExtended(Gbps)"]
            df_Lost_Bandwidth["Current_RX_BW(Gbps)"] =  df_Lost_Bandwidth["PortRcvDataExtended(Gbps)"]
                        
            
            df_Lost_Bandwidth = df_Lost_Bandwidth[
            ["SrcDevice", "SrcPort", "SrcGUID", "PortXmitWaitExt", "Lost_Bandwidth(Gbps)","Current_TX_BW(Gbps)","Current_RX_BW(Gbps)", "DstDevice", "DstPort", "DstGUID"]
       
            ]
                        
            df_Lost_Bandwidth = df_Lost_Bandwidth.sort_values(by="Lost_Bandwidth(Gbps)", ascending=False)


        #5.12 all ports TX RX Bandwidth
                  

            df_all_port_TX_RX_Bandwidth = df_all_port_TX_RX_Bandwidth.astype({'SrcPort':'int'})  
            df_all_port_TX_RX_Bandwidth = df_all_port_TX_RX_Bandwidth[
            [ "SrcDevice", "SrcPort", "SrcGUID","PortXmitDataExtended(Gbps)","PortRcvDataExtended(Gbps)" ,"Lost_Bandwidth(Gbps)", "DstDevice", "DstPort", "DstGUID",]
            ]      

            df_all_port_TX_RX_Bandwidth.rename(
                columns={
                    "PortXmitDataExtended(Gbps)":"TX_BW(Gbps)",
                    "PortRcvDataExtended(Gbps)":"RX_BW(Gbps)",
                    },
                inplace=True,
            )
            

                            
            df_all_port_TX_RX_Bandwidth = df_all_port_TX_RX_Bandwidth.sort_values(by=["SrcDevice", "SrcPort"], ascending=[True,True])             
                

else:
    print(f"\nWARN: Couldn't find START_PM_INFO in ibdiagnet2.db_csv.")


"""
    # Step 6. Check link BER
"""

if not df_ibdgnt_net_ext.empty:

    df_ibdgnt_net_ext = pd.merge(
        left=df_ibdgnt_net_ext,
        right=df_ibdgnt_lnk_tbl,
        left_on=["GUID", "#IB"],
        right_on=["SrcGUID", "SrcPort"],
        how="left",
    )

    if "Symbol BER" in df_ibdgnt_net_ext:
        df_ibdgnt_net_ext.rename(
            columns={
                "Effective BER": "EffectiveBER",
                "Symbol BER": "SymbolBER",
                "Raw BER": "RawBER",
            },
            inplace=True,
        )

        # 6.1 filter out links with effective BER > 1e-13

        df_eff_ber = df_ibdgnt_net_ext[df_ibdgnt_net_ext["EffectiveBER"] != ""].copy()
        df_eff_ber["EffectiveBER"] = df_eff_ber["EffectiveBER"].astype(float)

        df_eff_ber = df_eff_ber[df_eff_ber["EffectiveBER"] > 1e-13]

        df_eff_ber = df_eff_ber[
            ["SrcDevice", "SrcPort", "SrcGUID", "EffectiveBER", "DstDevice","DstPort", "DstGUID"]
        ]
        df_eff_ber = df_eff_ber.sort_values(by="EffectiveBER", ascending=False)

        # 6.2 filter out links with Symbol BER > 1e-13

        df_symbol_ber = df_ibdgnt_net_ext[
            (df_ibdgnt_net_ext["SymbolBER"] != "") & (df_ibdgnt_net_ext["SymbolBER"] != "N/A")
        ].copy()
        df_symbol_ber["SymbolBER"] = df_symbol_ber["SymbolBER"].astype(float)

        df_symbol_ber = df_symbol_ber[df_symbol_ber["SymbolBER"] > 1e-13]

        df_symbol_ber = df_symbol_ber[
            ["SrcDevice", "SrcPort", "SrcGUID",  "SymbolBER", "DstDevice", "DstPort", "DstGUID"]
        ]
        df_symbol_ber = df_symbol_ber.sort_values(by="SymbolBER", ascending=False)

        # 6.3 Raw BER

   
        df_Raw_ber = df_ibdgnt_net_ext[df_ibdgnt_net_ext["RawBER"] != ""].copy()    
        df_Raw_ber["RawBER"] = df_Raw_ber["RawBER"].astype(float)
        df_Raw_ber = df_Raw_ber[df_Raw_ber["RawBER"] > 1e-5]

        df_Raw_ber = df_Raw_ber[
            ["SrcDevice", "SrcPort", "SrcGUID",  "RawBER", "DstDevice", "DstPort", "DstGUID"]
        ]
        df_Raw_ber = df_Raw_ber.sort_values(by="RawBER", ascending=False)

    else : 

        df_ibdgnt_net_ext.rename(
            columns={
                "Effective BER": "EffectiveBER",
                "Symbol Err": "SymbolErr",
                "Raw BER": "RawBER",
            },
            inplace=True,
        )

        # 6.1 filter out links with effective BER > 1e-13

        df_eff_ber = df_ibdgnt_net_ext[df_ibdgnt_net_ext["EffectiveBER"] != ""].copy()
        df_eff_ber["EffectiveBER"] = df_eff_ber["EffectiveBER"].astype(float)

        df_eff_ber = df_eff_ber[df_eff_ber["EffectiveBER"] > 1e-13]

        df_eff_ber = df_eff_ber[
            ["SrcDevice", "SrcPort", "SrcGUID", "EffectiveBER", "DstDevice", "DstPort", "DstGUID"]
        ]
        df_eff_ber = df_eff_ber.sort_values(by="EffectiveBER", ascending=False)

        # 6.2 filter out links with Symbol BER > 1e-13

        df_symbol_ber = df_ibdgnt_net_ext[
            (df_ibdgnt_net_ext["SymbolErr"] != "") & (df_ibdgnt_net_ext["SymbolErr"] != "N/A")
        ].copy()
        df_symbol_ber["SymbolErr"] = df_symbol_ber["SymbolErr"].astype(float)

        df_symbol_ber = df_symbol_ber[df_symbol_ber["SymbolErr"] > 0]

        df_symbol_ber = df_symbol_ber[
            ["SrcDevice", "SrcPort", "SrcGUID",  "SymbolErr", "DstDevice", "DstPort", "DstGUID"]
        ]
        df_symbol_ber = df_symbol_ber.sort_values(by="SymbolErr", ascending=False)

        # 6.3 Raw BER

        df_Raw_ber = df_ibdgnt_net_ext[df_ibdgnt_net_ext["RawBER"] != ""].copy()

        df_Raw_ber["RawBER"] = df_Raw_ber["RawBER"].astype(float)

        df_Raw_ber = df_Raw_ber[df_Raw_ber["RawBER"] > 2e-5]

        df_Raw_ber = df_Raw_ber[
            ["SrcDevice", "SrcPort", "SrcGUID",  "RawBER", "DstDevice", "DstPort", "DstGUID"]
        ]
        df_Raw_ber = df_Raw_ber.sort_values(by="RawBER", ascending=False)


else:
    print(f"\nWARN: Couldn't find BER info in ibdiagnet2.net_dump_ext.")



"""
    # Step 7. Print results
"""
if args.top_n == 10:
    print(
        f"\nINFO: The --top-n option is not set, only the first 10 records will be listed here."
        f"\n"
    )

"""
    # Step 7.1 Print IB Inventory lists (Switch & HCA FW info and quantity)
"""


if not df_nodes_info_tbl.empty and not df_sw_tbl.empty and not df_sw_info_tbl.empty : 
    print(f"\n\nIB Switch Inventory Summary:")
    print(f"Total IB SW/ASIC: {len(df_sw_tbl)}")
    print(f"##################################################")
    for i in range(df_ib_sw_pivot.index.size):
        print("--------------------------------------------------")
        print(f"PSID: {df_ib_sw_pivot.index[i]}")
        print("--------------------------------------------------")
        for j in range(df_ib_sw_pivot.columns.size):
            if pd.notnull(df_ib_sw_pivot.iat[i, j]):
                print(
                    f"FW Ver.: {df_ib_sw_pivot.columns[j]:>16}\t"
                    f"Qty.: {df_ib_sw_pivot.iat[i, j]:>6.0f}"
                )
    print("--------------------------------------------------")

    
# 4.2 Print HCA inventory summary
if not df_nodes_info_tbl.empty and not df_sw_tbl.empty and not df_sw_info_tbl.empty : 
    print(f"\n\nHCA Inventory Summary:")
    print(f"Total HCA Ports: {len(df_hca_tbl)}")
    print(f"##################################################")
    for i in range(df_hca_pivot.index.size):
        print("--------------------------------------------------")
        print(f"PSID: {df_hca_pivot.index[i]}")
        print("--------------------------------------------------")
        for j in range(df_hca_pivot.columns.size):
            if pd.notnull(df_hca_pivot.iat[i, j]):
                print(
                    f"FW Ver.: {df_hca_pivot.columns[j]:>16}\t"
                    f"Qty.: {df_hca_pivot.iat[i, j]:>6.0f}"
                )
    print("--------------------------------------------------")
    print("")

if  df_nodes_info_tbl.empty or  df_sw_tbl.empty or  df_sw_info_tbl.empty: 
    
    print(f"\n\nIB Switch Inventory Summary:")
    print(f"##################################################")
    print("--------------------------------------------------")
    print(f"There is no Switch inventory info in ibdiagnet.db_csv, please check items in ibdiagnet.db_csv")
    print("--------------------------------------------------")

    print(f"\n\nHCA Inventory Summary:")
    print(f"##################################################")
    print("--------------------------------------------------")
    print(f"There is no HCA inventory info in ibdiagnet.db_csv, please check items in ibdiagnet.db_csv")
    print("--------------------------------------------------")

    
    
"""
    # Step 7.2 Print results BER
"""



if "--extended_speeds all" not in running_command_only :
    print(
        f"\nINFO: To get the FEC Uncorrectable counters, please add --extended_speeds parameters in the commands",    
    )

if temp_invalid_checking :
        Invalid_lid_mcast = pd.DataFrame({'Invalid LID number or Mcast LID' : warn_return })
                
        if len(warn_return) >0  :
                print(
                    f"\n\nInvalid LID number or Mcast LID found (to skip this, please re-run with -s )",
                    f"\n##############################################################################################",
                )      
                for i in warn_return :
                            print(i)
       

        else:
                print(
                    f"\n\nNo Invalid LID & Mcast LID found",
                    f"\n##################################",
                )

if not df_pm.empty:
            
    if not df_lnk_dn.empty:
        print(
            f"\n\nLinkDowned Counters > 0 (Qt :{len(df_lnk_dn.index)}):",
            f"\n##################################################",
            f"\n{df_lnk_dn.head(args.top_n).to_string(index=False)}",
        )
    else:
        print(
            f"\n\nLinkDowned Counters > 0 (Qt : 0):",
            f"\n##################################################",
        )


    if not df_xmit_drp.empty:
        print(
            f"\n\nXmitDidscard Counters > 0 (Qt :{len(df_xmit_drp.index)})",
            f"\n##################################################",
            f"\n{df_xmit_drp.head(args.top_n).to_string(index=False)}",
        )
    else:
        print(
            f"\n\nXmitDidscard Counters > 0 (Qt : 0):",
            f"\n##################################################",
        )

 
    if "--extended_speeds" in running_command_only :
     
        if not df_fec_uncorrectable.empty:
            print(
                f"\n\nPort FEC Uncorrectable Counters (Qt :{len(df_fec_uncorrectable.index)}) ",
                f"\n##################################################",
                f"\n{df_fec_uncorrectable.head(args.top_n).to_string(index=False)}",
            )
        else:
            print(
                f"\n\nPort FEC Uncorrectable Counters (Qt : 0):",
                f"\n##################################################",
            )

    if not df_buf_overrun.empty:
        print(
            f"\n\nBuffer overrun Counters > 0 (Qt :{len(df_buf_overrun.index)})",
            f"\n##################################################",
            f"\n{df_buf_overrun.head(args.top_n).to_string(index=False)}",
        )
    else:
        print(
            f"\n\nBuffer overrun Counters > 0 (Qt : 0):",
            f"\n##################################################",
        )


    if not df_max_retrans.empty:
        print(
            f"\nMax Retransmission_rate : > 500 (Qt :{len(df_max_retrans.index)}) :",
            f"\n##################################################",
            f"\n{df_max_retrans.head(args.top_n).to_string(index=False)}",
        )
    else:
        print(
            f"\nMax Retransmission_rate : > 500 (Qt : 0):",
            f"\n##################################################",
        )

if not df_ibdgnt_net_ext.empty:

    if not df_Raw_ber.empty:

        if "RawBER" in df_Raw_ber:
            print(
                f"\n\nRaw BER Counters > 1e-5 (Qt :{len(df_Raw_ber.index)}) ",
                f"\n##################################################",
                f"\n{df_Raw_ber.head(args.top_n).to_string(index=False)}",
            )

    else : 
        print(
            f"\n\nRaw BER Counters > 1e-5 (Qt : 0):",
            f"\n##################################################",
            )       

    if not df_eff_ber.empty:
        print(
            f"\n\nEffective BER Counters > 1e-13 (Qt :{len(df_eff_ber.index)})",
            f"\n##################################################",
            f"\n{df_eff_ber.head(args.top_n).to_string(index=False)}",
        )
    else:
        print(
            f"\n\nEffective BER Counters > 1e-13 (Qt : 0):",
            f"\n##################################################",
        )

    if not df_symbol_ber.empty:

        if "SymbolBER" in df_symbol_ber:
            print(
                f"\n\nSymbol BER Counters > 1e-13, or Err > 0 (Qt :{len(df_symbol_ber.index)})",
                f"\n##################################################",
                f"\n{df_symbol_ber.head(args.top_n).to_string(index=False)}",
            )

        else : 
            print(
                f"\n\nSymbol Err counters > 0 (Qt : 0)",
                f"\n##################################################",
                f"\n{df_symbol_ber.head(args.top_n).to_string(index=False)}",
            )       

    else:
        print(
            f"\n\nSymbol BER Counters > 1e-13, or Err > 0 (Qt : 0):",
            f"\n##################################################",
        )

    if not df_pm.empty:
        if not df_congestion_ext.empty:
            print(
                f"\n\nCongestion Indexes > 10 (will be deprecated):",
                f"\n##################################################",
                f"\n{df_congestion_ext.head(args.top_n).to_string(index=False)}",
            )
        else:
            print(
                f"\n\nCongestion Indexes > 10 (will be deprecated):",
                f"\n##################################################",
                f"\n\nCongestion Indexes : < 10 on all links:",
            )

        if "--pm_pause_time" in running_command_only :
                    
            if not df_Lost_Bandwidth.empty:
                print(
                    f"\n\nLost Bandwidth Summary (Qt :{len(df_Lost_Bandwidth.index)})",
                    f"\n##################################################",
                    f"\n{df_Lost_Bandwidth.head(args.top_n).to_string(index=False)}",
                )

            else:
                print(
                f"\n\nLost Bandwidth Summary ",
                f"\n##################################################",
                f"\n\nLost BandWidth 0 on all links :",
            )

            if args.all:
                
                print(
                        f"\n\n###########################################################################################################################################################################",
                        f"\n##########################################################       Fabric link Rate in details + Lost Bandwidth       #######################################################",
                        f"\n###########################################################################################################################################################################",   
                    )
    
                print(
                        f"\n\n(Tier1 & Tier4) Switch -> Servers By RX Bandwidth     ",
                        f"\n#######################################################################################",

                        )                          
                                
                if not df_Server_Rx_Bandwidth.empty:
                    print(
                        f"\n Sorted by Lost Bandwitdh ",
                        f"\n----------------------------------------",
                        f"\n{df_Server_Rx_Bandwidth.head(args.top_n).to_string(index=False)}",
                    )

                    df_Server_Rx_Bandwidth = df_Server_Rx_Bandwidth.sort_values(by="RX_BW(Gbps)", ascending=False)
                    print(
                        f"\n Sorted by RX Bandwidth ",
                        f"\n------------------------------------------",
                        f"\n{df_Server_Rx_Bandwidth.head(args.top_n).to_string(index=False)}",
                    )
                    
                else:
                    print(
                    f"\n\n(Tier1 & Tier4) Rx BandWidth 0 on all links :",
                    )

                if not df_Server_Tx_Bandwidth.empty:

                    print(
                        f"\n\n (Tier1 & Tier4) Servers -> Switch By TX Bandwidth   ",
                        f"\n#######################################################################################",

                        )
                    
                    
                    print(
                        f"\n Sorted by Lost Bandwitdh ",
                        f"\n----------------------------------------",
                        f"\n{df_Server_Tx_Bandwidth.head(args.top_n).to_string(index=False)}",
                    )
                    
                    df_Server_Tx_Bandwidth = df_Server_Tx_Bandwidth.sort_values(by="TX_BW(Gbps)", ascending=False)
                    print(
                        f"\n Sorted by Tx BandWidth ",
                        f"\n------------------------------------------",
                        f"\n{df_Server_Tx_Bandwidth.head(args.top_n).to_string(index=False)}",
                    )


                else:
                    print(
                    f"\n\n(Tier2 & Tier3) Tx BandWidth 0 on all links :",
                    )

                if not df_Switch_Rx_Bandwidth.empty:
                    
                    print(
                        f"\n\n (Tier2 & Tier3) Switch <-> Switch By RX Bandwidth   ",     
                        f"\n#######################################################################################",                    
                
                        )
                    
                    print(
                        f"\n Sorted by Lost Bandwitdh ",
                        f"\n--------------------------------------",
                        f"\n{df_Switch_Rx_Bandwidth.head(args.top_n).to_string(index=False)}",
                        )
                
                    df_Switch_Rx_Bandwidth = df_Switch_Rx_Bandwidth.sort_values(by="RX_BW(Gbps)", ascending=False)          
                    print(
                        f"\n Sorted by Rx BandWidth  ",
                        f"\n-----------------------------------------",
                        f"\n{df_Switch_Rx_Bandwidth.head(args.top_n).to_string(index=False)}",
                        )


                else:
                    print(
                    f"\n\nRx BandWidth 0 on all links :",
                    )

                if not df_Switch_Tx_Bandwidth.empty:
                    print(
                        f"\n\n (Tier2 & Tier3) Switch <-> Switch By TX Bandwidth    ",
                        f"\n#######################################################################################",                    

                        )
                        
                    print(
                        f"\n Sorted by Lost Bandwitdh ",
                        f"\n-----------------------------------------",
                        f"\n{df_Switch_Tx_Bandwidth.head(args.top_n).to_string(index=False)}",
                        )

                    df_Switch_Tx_Bandwidth = df_Switch_Tx_Bandwidth.sort_values(by="TX_BW(Gbps)", ascending=False)            
                    print(
                        f"\n Sorted by Tx BandWidth ",
                        f"\n------------------------------------------",
                        f"\n{df_Switch_Tx_Bandwidth.head(args.top_n).to_string(index=False)}",
                        )
                    
                else:
                    print(
                        f"\n\n (Tier2 & Tier3) Tx BandWidth 0 on all links :",
                        )
        
        
            
        
                if not df_all_port_TX_RX_Bandwidth.empty:
                    print(
                        f"\n\n All_port_TX_RX_Bandwidth Bandwidth    ",
                        f"\n#######################################################################################",                    

                        )
                        
                    print(
                        f"\n Sorted by Src device & port number ",
                        f"\n-----------------------------------------",
                        f"\n{df_all_port_TX_RX_Bandwidth.head(args.top_n).to_string(index=False)}",
                        )

                    
                else:
                    print(
                        f"\n\n No data for all ports bandwidth links:",
                        )
                                                                       
if Temperature_info_exist : 

    df_nodes_temperature = df_nodes_temperature[(df_nodes_temperature["IbDeviceTemperature"] > 69) | (df_nodes_temperature["SwitchAsicTemperature"] > 69)]

    df_nodes_temperature = df_nodes_temperature.sort_values(by="SwitchAsicTemperature", ascending=False)


    if not df_nodes_temperature.empty:
        print(
            f"\n\nIB Device temperature > 70c or IB Switch Asic temperature > 70c (Qt : {len(df_nodes_temperature.index)})",
            f"\n##################################################",
            f"\n{df_nodes_temperature.head(args.top_n).to_string(index=False)}",
        )
    else:
        print(
            f"\n\nIB Device temperature > 70c or IB Switch Asic temperature > 70c: (Qt :0 )",
            f"\n##################################################",
        )

if ibdiagnet_cable_file_exist : 
             
    df_cable_3rd_party = df_cable_all[(df_cable_all["Vendor"] != "Mellanox") & (df_cable_all["Vendor"] != "NVIDIA")]
           
    df_cable_3rd_party = df_cable_3rd_party [
    ["SrcDevice", "SrcPort", "SrcGUID", "Vendor", "PN","SN", "DstDevice", "DstPort", "DstGUID"]
     ]
                       
    df_cable_3rd_party = df_cable_3rd_party.sort_values(by="Vendor", ascending=False)

             
    if not df_cable_3rd_party.empty:
        print(
            f"\n\n3rd Party Cable used  (Qt : {len(df_cable_3rd_party.index)})",
            f"\n##################################################",
            f"\n{df_cable_3rd_party.head(args.top_n).to_string(index=False)}",
        )
    else:
        print(
            f"\n\n3rd Party Cable found: (Qt :0 )",
            f"\n##################################################",
        )
        

    df_cable_temperature = df_cable_all[df_cable_all["Temperature"] > 70]    
    df_cable_temperature = df_cable_temperature [
    ["SrcDevice", "SrcPort", "SrcGUID", "Temperature", "DstDevice", "DstPort", "DstGUID"]
     ]
    df_cable_temperature = df_cable_temperature.sort_values(by="Temperature", ascending=False)
    
         
    if not df_cable_temperature.empty:
        print(
            f"\n\nCable Temperature > 70c: (Qt : {len(df_cable_temperature.index)} ) ",
            f"\n##################################################",
            f"\n{df_cable_temperature.head(args.top_n).to_string(index=False)}",
            )
    else:
        print(
            f"\n\nCable Temperature > 70c: (Qt :0 )",
            f"\n##################################################",
        )


###########################################################################################################################################################
########################## This is to check for Power Supply (PSU) H/W failure.############################################################################

   # df_power_supplies_tbl = df_power_supplies_tbl[["NodeGuid","PSUIndex","IsPresent","IsFRU","ACInput","DCState","AlertState","FanState","TemperatureState","SerialNumber"]]

if not df_power_supplies_tbl.empty:
    
    df_power_supplies_tbl = df_power_supplies_tbl[ (df_power_supplies_tbl['IsPresent'] != 'Yes') | (df_power_supplies_tbl['IsFRU'] != 'Yes') |  (df_power_supplies_tbl['DCState'] == 'Error') | (df_power_supplies_tbl['AlertState'] == 'Yes')]

    if not df_power_supplies_tbl.empty:
        print(
            f"\n\nPSU problem regarding (IsPresent, IsFRU, DCState, AlertState ) (Qt : {len(df_power_supplies_tbl.index)} ) ",
            f"\n##################################################",
            f"\n{df_power_supplies_tbl.to_string(index=False)}",
            )
                
    else:
        print(
            f"\n\nNo PSU problem regarding (IsPresent, IsFRU, DCState, AlertState )",
            f"\n##################################################",
            )

else:
    print(
        f"\n\nNo PSU problem regarding (IsPresent, IsFRU, DCState, AlertState )",
        f"\n##################################################",
        )

###########################################################################################################################################################
########################## Save all outputs to excel file  ################################################################################################
          
if args.output_file:

    print(
        f"\n\nSaving to Excel file:",
        f"\n##################################################",
        f"\n\n",
    )

    # Create a Pandas Excel writer

    writer = pd.ExcelWriter(args.output_file, engine="openpyxl")


    # 8.1 Writing IB inventory lists

    if not df_nodes_info_tbl.empty and not df_sw_tbl.empty and not df_sw_info_tbl.empty and not df_sw_tbl.empty:
        df_ib_sw_pivot.to_excel(writer, sheet_name="IB_Switch_Summary")

    if not df_nodes_info_tbl.empty and not df_sw_tbl.empty and not df_sw_info_tbl.empty and not df_hca_tbl.empty:
        df_hca_pivot.to_excel(writer, sheet_name="HCA_Inventory_Summary")     
        
    # 8.2 Writing IB BER

    if temp_invalid_checking :
        if not Invalid_lid_mcast.empty:           
            Invalid_lid_mcast.to_excel(writer, sheet_name="Invalid LID & Mcast checking", index=False)

    if not df_pm.empty:
        if not df_lnk_dn.empty:
            df_lnk_dn.to_excel(writer, sheet_name="Flapping_Links", index=False)

        if not df_xmit_drp.empty:
            df_xmit_drp.to_excel(writer, sheet_name="Output_Didscard_Links", index=False)

        if "--extended_speeds" in running_command_only :
            if not df_fec_uncorrectable.empty:
                df_fec_uncorrectable.to_excel(writer, sheet_name="FEC_Uncorrectable_Links", index=False)

        if not df_buf_overrun.empty:
            df_buf_overrun.to_excel(writer, sheet_name="Buf_Overrun_Links", index=False)

        if not df_congestion_ext.empty:
            df_congestion_ext.to_excel(writer, sheet_name="Congested_Links", index=False)

        if not df_max_retrans.empty:
            df_max_retrans.to_excel(writer, sheet_name="Max_Retransmission_rate", index=False)

    if not df_ibdgnt_net_ext.empty:
        if not df_eff_ber.empty:
            df_eff_ber.to_excel(writer, sheet_name="Effective_BER_Links", index=False)

        if not df_symbol_ber.empty:
            df_symbol_ber.to_excel(writer, sheet_name="Symbol_BER_Links", index=False)

        if not df_Raw_ber.empty:
            df_Raw_ber.to_excel(writer, sheet_name="Raw_BER_Links", index=False)

      
        if "--pm_pause_time" in running_command_only :
            if not df_Lost_Bandwidth.empty:
                df_Lost_Bandwidth.to_excel(writer, sheet_name="Lost_Bandwidth", index=False)

            if args.all:
                if not df_Server_Tx_Bandwidth.empty:
                   df_Server_Tx_Bandwidth.to_excel(writer, sheet_name="Server_Tx_Bandwidth", index=False)
                    
                if not df_Server_Rx_Bandwidth.empty:
                    df_Server_Rx_Bandwidth.to_excel(writer, sheet_name="Server_Rx_Bandwidth", index=False)

                if not df_Switch_Tx_Bandwidth.empty:
                    df_Switch_Tx_Bandwidth.to_excel(writer, sheet_name="Switch_Tx_Bandwidth", index=False)

                if not df_Switch_Rx_Bandwidth.empty:
                    df_Switch_Rx_Bandwidth.to_excel(writer, sheet_name="Switch_Rx_Bandwidth", index=False)
            
            
                if not df_all_port_TX_RX_Bandwidth.empty:
                    df_all_port_TX_RX_Bandwidth.to_excel(writer, sheet_name="All_port_TX_RX_Bandwidth", index=False)        
            

    if Temperature_info_exist :
        if not df_nodes_temperature.empty:
                df_nodes_temperature.to_excel(writer, sheet_name="IB device and Asic temperature", index=False)

    if ibdiagnet_cable_file_exist :               
        if not df_cable_3rd_party.empty:
                df_cable_3rd_party.to_excel(writer, sheet_name="3rd party cables", index=False)
            
        if not df_cable_temperature.empty:
                df_cable_temperature.to_excel(writer, sheet_name="Cable Temperature >70c", index=False)


    if not df_power_supplies_tbl.empty:
        
        df_power_supplies_tbl.to_excel(writer, sheet_name="PSU problem regarding", index=False)
                        
        
    writer.close()
    print(f"Data is written successfully to Excel File: {args.output_file}")