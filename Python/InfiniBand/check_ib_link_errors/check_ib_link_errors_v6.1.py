# =============================================================================
# File name: check_ib_link_errors_v5.py
# Description: check common errors and congestion indexes on all IB links
# Author: <.....> , HyungKwang Choi
# Software: Python 3.8+, Pandas and OpenPyXL Libraries
# Revision:
# v1  : 7/29/2021  modified by  <....>
# v2  : 3/15/2022  modified by HyungKwang Choi (Fixed script bug (FEC Uncorrectable))
# v3  : 4/14/2022  modified by HyungKwang Choi (Fixed script bug (Symbol BER/Err))
# v4  : 4/30/2022  modified by HyungKwang Choi (Modifying BER threshold from ‘1e-12’ to ‘1e-13’)
# v5  : 5/1/2022   modified by HyungKwang Choi  (Added "Max Retransmission_rate")
# v5.1: 5/11/2022  modified by HyungKwang Choi  (modifed "Running command" parsing code)
# v6.1: 5/13/2022  modified by HyungKwang Choi & Sam (In the Ibdiagnet "2.8.1", ibdiagnet2_db.csv files , data written like "-1". Which triggers an exception such as) "PortXmitWaitExt = -1")
#==================================================================================

##############Troubleshoot syntax###########################
#  df_pm.to_csv("before") 
# =============================================================================

import argparse
import io
import os
import re
import pandas as pd

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
    "-v", "--version", action="version", version="%(prog)s 5.0",
    help="print current script version",
)
args = parser.parse_args()


def db_csv_extr(separator, ibdgnt_db_csv_file):

    """
    Extract each csv table within ibdiagnet2.db_csv
    """

    # search csv tables

    regexp = re.compile(
        r"^START_" + separator + r"$\n"         # starting separator
        r"((.*\n)+)"                            # csv table
        r"^END_" + separator + r"$\n",          # ending separator
        re.MULTILINE
    )

    regexp_result = re.search(regexp, ibdgnt_db_csv_file)
    
    #print(regexp_result)
    #print(pd.read_csv(io.StringIO(regexp_result.group(1))))

    if regexp_result:
        return pd.read_csv(io.StringIO(regexp_result.group(1)), low_memory=False)
    else:
        return pd.DataFrame()


def net_ext_extr(ibdgnt_net_ext_file):

    """
    Extract data from ibdiagnet2.net_dump_ext
    """

    # Skip commented lines

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


def lnk_tbl_extr(ibdgnt_net_file):

    """
    Extract all active links from ibdiagnet2.net_dump
    """

    # Block starting line:
    # "MF0;<SW Name >:MQM8700/U1", Mellanox, 0xb8cef603001bf9de, LID 1
    sw_blk_regex = re.compile(
        r"^\"(.{1,255})\", \w+, (\w+), LID \d+\n"   # GRP 1: sw name
        r"((.*\w+.*\n)+)"                           # GRP 2: link table
        r"^$\n",                                    # blank line
        re.MULTILINE,
    )

    sw_blcks = re.findall(sw_blk_regex, ibdgnt_net_file)

    df_lnk_tbl = pd.DataFrame()

    # 1. Interate and concatenate swich blocks

    for i in sw_blcks:

        # Load link table

        df_sw_blk = pd.read_csv(io.StringIO(i[2]), sep=" :", engine="python", dtype=str)

        df_sw_blk["SrcDevice"] = i[0]
        df_sw_blk["SrcGUID"] = i[1]

        # Clean up each switch block

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

    # 4. Finalize link table DF

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
        ["SrcDevice", "SrcPort", "SrcGUID", "DstDevice", "DstPort", "DstGUID"]
    ]

    df_dup_lnks = pd.DataFrame()

    df_dup_lnks[
        ["SrcDevice", "SrcPort", "SrcGUID", "DstDevice", "DstPort", "DstGUID"]
    ] = df_lnk_tbl[
        ["DstDevice", "DstPort", "DstGUID", "SrcDevice", "SrcPort", "SrcGUID"]
    ]

    df_full_lnk_tbl = pd.concat([df_lnk_tbl, df_dup_lnks])

    df_full_lnk_tbl.drop_duplicates(
        subset=["SrcGUID", "SrcPort"],
        inplace=True,
    )

    # Add leading 0 if GUID length < 16 hex numbers

    df_full_lnk_tbl["SrcGUID"] = df_full_lnk_tbl["SrcGUID"].apply(lambda x: "0x" + x.lstrip("0x").zfill(16))
    df_full_lnk_tbl["DstGUID"] = df_full_lnk_tbl["DstGUID"].apply(lambda x: "0x" + x.lstrip("0x").zfill(16))

    df_full_lnk_tbl.reset_index(drop=True, inplace=True)

    return df_full_lnk_tbl


# Step 0. Display Runnig command

ibdgnt_log = args.ibdiagnet_folder + "/ibdiagnet2.log"

if os.path.isfile(ibdgnt_log):

    with open(ibdgnt_log, "r", encoding="utf-8", errors="ignore") as log_file:

        while True:
            running_command_only = log_file.readline()
        
            if "Running command:"  in running_command_only : break
            if "Running:"  in running_command_only : break

    #    running_command = log_file.readlines()
    #    print(running_command)
    #    running_command_only = running_command[0]

        print('\n{} '.format(running_command_only) )
    

else:
    print("\nCouldn't find ibdiagnet2.log. Existing ...")
    exit()

# Step 1. Load ibdiagnet2.net_dump

#print("\nStart to parse ibdiagnet2.net_dump ...")

ibdgnt_net = args.ibdiagnet_folder + "/ibdiagnet2.net_dump"

if os.path.isfile(ibdgnt_net):

    with open(ibdgnt_net, "r", encoding="utf-8", errors="ignore") as net_file:
        net_dump = net_file.read()

    df_ibdgnt_lnk_tbl = lnk_tbl_extr(net_dump)

else:
    print("\nCouldn't find ibdiagnet2.net_dump. Existing ...")
    exit()

# Step 2. Load ibdiagnet2.db_csv

#print("\nStart to parse ibdiagnet2.db_csv ...")

ibdgnt_db = args.ibdiagnet_folder + "/ibdiagnet2.db_csv"

if os.path.isfile(ibdgnt_db):

    with open(ibdgnt_db, "r", encoding="utf-8", errors="ignore") as db_csv_file:
        db_csv = db_csv_file.read()

    # Extract PM CSV table from ibdiagnet2.db_csv

    df_pm = db_csv_extr("PM_INFO", db_csv)
    #print(df_pm.iloc[:,[43]])

else:
    print("\nCouldn't find ibdiagnet2.db_csv. Existing ...")
    exit()

# Step 3. Load ibdiagnet2.net_dump_ext

#print(f"\nStart to parse ibdiagnet2.net_dump_ext ...")

ibdgnt_net_ext = args.ibdiagnet_folder + "/ibdiagnet2.net_dump_ext"

if os.path.isfile(ibdgnt_net_ext):

    with open(ibdgnt_net_ext, "r", encoding="utf-8", errors="ignore") as net_dump_file:
        net_dump = net_dump_file.read()

    df_ibdgnt_net_ext = net_ext_extr(net_dump)

else:
    print(f"\n\nCouldn't find ibdiagnet2.net_dump_ext. Existing ...")
    exit()

# Step 4. Check PM counters

if not df_pm.empty:

    df_pm.rename(
        columns={
            " max_retransmission_rate": "max_retransmission_rate",
        },
        inplace=True,
    )

    df_pm["PortNumber"] = df_pm["PortNumber"].astype(str)

    df_pm = pd.merge(
        left=df_pm,
        right=df_ibdgnt_lnk_tbl,
        left_on=["NodeGUID", "PortNumber"],
        right_on=["SrcGUID", "SrcPort"],
        how="left",
    )
  #  df_pm.to_csv("before") 


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
            "PortXmitWaitExt",
            "PortXmitPktsExtended",
            "ExcessiveBufferOverrunErrors",
            "PortFECUncorrectableBlockCounter",
            "max_retransmission_rate",
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
            "PortXmitWaitExt",
            "PortXmitPktsExtended",
            "ExcessiveBufferOverrunErrors",
            "max_retransmission_rate",
        ]



    df_pm = df_pm[pm_cols]
    #df_pm.to_csv("final") 
    # 4.1 LinkDownedCounter

    df_lnk_dn = df_pm[df_pm["LinkDownedCounter"] > 0]
    df_lnk_dn = df_lnk_dn[
        ["SrcDevice", "SrcPort", "SrcGUID", "LinkDownedCounter", "DstDevice", "DstGUID", "DstPort"]
    ]
    df_lnk_dn = df_lnk_dn.sort_values(by="LinkDownedCounter", ascending=False)

    # 4.2 PortXmitDiscards

    df_xmit_drp = df_pm[df_pm["PortXmitDiscards"] > 0]
    df_xmit_drp = df_xmit_drp[
        ["SrcDevice", "SrcPort", "SrcGUID", "PortXmitDiscards", "DstDevice", "DstGUID", "DstPort"]
    ]
    df_xmit_drp = df_xmit_drp.sort_values(by="PortXmitDiscards", ascending=False)

    # 4.3 PortFECUncorrectableBlockCounter
 

    if "extended_speeds" in running_command_only :
        df_fec_uncorrectable = df_pm[df_pm["PortFECUncorrectableBlockCounter"] > 0]
        df_fec_uncorrectable = df_fec_uncorrectable[
            ["SrcDevice", "SrcPort", "SrcGUID", "PortFECUncorrectableBlockCounter", "DstDevice", "DstGUID", "DstPort"]
        ]
        df_fec_uncorrectable = df_fec_uncorrectable.sort_values(
            by="PortFECUncorrectableBlockCounter", ascending=False
        )

    # 4.4 ExcessiveBufferOverrunErrors

    df_buf_overrun = df_pm[df_pm["ExcessiveBufferOverrunErrors"] != 0]
    df_buf_overrun = df_buf_overrun[
        ["SrcDevice", "SrcPort", "SrcGUID", "ExcessiveBufferOverrunErrors", "DstDevice", "DstGUID", "DstPort"]
    ]
    df_buf_overrun = df_buf_overrun.sort_values(
        by="ExcessiveBufferOverrunErrors", ascending=False
    )

    # 4.5 CongestionIndex

    df_pm["PortXmitWaitExt"] = df_pm["PortXmitWaitExt"].apply(int, base=16)
    df_pm["PortXmitPktsExtended"] = df_pm["PortXmitPktsExtended"].apply(int, base=16)

    #df_pm.to_csv("Congested_Links")
  

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
        ["SrcDevice", "SrcPort", "SrcGUID", "PortXmitWaitExt", "PortXmitPktsExtended", "CongestionIndexExt", "DstDevice", "DstGUID", "DstPort"]
    ]
    df_congestion_ext = df_congestion_ext.sort_values(
        by="CongestionIndexExt", ascending=False
    )

    # 4.6 max_retransmission_rate (threshold 500)
    df_pm["max_retransmission_rate"] = df_pm["max_retransmission_rate"].apply(int, base=16) #to convert hex (0x0000) to int    

    df_max_retrans = df_pm[df_pm["max_retransmission_rate"] > 500]
    df_max_retrans = df_max_retrans[
        ["SrcDevice", "SrcPort", "SrcGUID", "max_retransmission_rate", "DstDevice", "DstGUID", "DstPort"]
    ]
    df_max_retrans = df_max_retrans.sort_values(
        by="max_retransmission_rate", ascending=False
    )   

else:
    print(f"\nWARN: Couldn't find PM info in ibdiagnet2.db_csv.")

# Step 5. Check link BER

if not df_ibdgnt_net_ext.empty:

    # 5.1 extract remote end info

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
            },
            inplace=True,
        )

        # 5.2 filter out links with effective BER > 1e-13

        df_eff_ber = df_ibdgnt_net_ext[df_ibdgnt_net_ext["EffectiveBER"] != ""].copy()
        df_eff_ber["EffectiveBER"] = df_eff_ber["EffectiveBER"].astype(float)

        df_eff_ber = df_eff_ber[df_eff_ber["EffectiveBER"] > 1e-13]

        df_eff_ber = df_eff_ber[
            ["SrcDevice", "SrcPort", "SrcGUID", "EffectiveBER", "DstDevice", "DstGUID", "DstPort"]
        ]
        df_eff_ber = df_eff_ber.sort_values(by="EffectiveBER", ascending=False)

        # 2.3 filter out links with Symbol BER > 1e-13

        df_symbol_ber = df_ibdgnt_net_ext[
            (df_ibdgnt_net_ext["SymbolBER"] != "") & (df_ibdgnt_net_ext["SymbolBER"] != "N/A")
        ].copy()
        df_symbol_ber["SymbolBER"] = df_symbol_ber["SymbolBER"].astype(float)

        df_symbol_ber = df_symbol_ber[df_symbol_ber["SymbolBER"] > 1e-13]

        df_symbol_ber = df_symbol_ber[
            ["SrcDevice", "SrcPort", "SrcGUID",  "SymbolBER", "DstDevice", "DstGUID", "DstPort"]
        ]
        df_symbol_ber = df_symbol_ber.sort_values(by="SymbolBER", ascending=False)

    else : 

        df_ibdgnt_net_ext.rename(
            columns={
                "Effective BER": "EffectiveBER",
                "Symbol Err": "SymbolErr",
            },
            inplace=True,
        )

        # 5.2 filter out links with effective BER > 1e-13

        df_eff_ber = df_ibdgnt_net_ext[df_ibdgnt_net_ext["EffectiveBER"] != ""].copy()
        df_eff_ber["EffectiveBER"] = df_eff_ber["EffectiveBER"].astype(float)

        df_eff_ber = df_eff_ber[df_eff_ber["EffectiveBER"] > 1e-13]

        df_eff_ber = df_eff_ber[
            ["SrcDevice", "SrcPort", "SrcGUID", "EffectiveBER", "DstDevice", "DstGUID", "DstPort"]
        ]
        df_eff_ber = df_eff_ber.sort_values(by="EffectiveBER", ascending=False)

        # 2.3 filter out links with Symbol BER > 1e-13

        df_symbol_ber = df_ibdgnt_net_ext[
            (df_ibdgnt_net_ext["SymbolErr"] != "") & (df_ibdgnt_net_ext["SymbolErr"] != "N/A")
        ].copy()
        df_symbol_ber["SymbolErr"] = df_symbol_ber["SymbolErr"].astype(float)

        df_symbol_ber = df_symbol_ber[df_symbol_ber["SymbolErr"] > 0]

        df_symbol_ber = df_symbol_ber[
            ["SrcDevice", "SrcPort", "SrcGUID",  "SymbolErr", "DstDevice", "DstGUID", "DstPort"]
        ]
        df_symbol_ber = df_symbol_ber.sort_values(by="SymbolErr", ascending=False)


else:
    print(f"\nWARN: Couldn't find BER info in ibdiagnet2.net_dump_ext.")

# Step 6. Print results

if args.top_n == 10:
    print(
        f"\nINFO: The --top-n option is not set, only the first 10 records will be listed here."
    )

if "--extended_speeds all" not in running_command_only :
    print(
        f"\nINFO: To get the FEC Uncorrectable counters, please add --extended_speeds all option",    
    )

if not df_pm.empty:

    if not df_lnk_dn.empty:
        print(
            f"\n\nLinkDowned Counters:",
            f"\n##################################################",
            f"\n{df_lnk_dn.head(args.top_n).to_string(index=False)}",
        )
    else:
        print(
            f"\n\nLinkDowned Counters: 0 on all links.",
            #f"\n##################################################",
            #f"\nINFO: LinkDowned counters are 0 on all links.",
        )


    if not df_xmit_drp.empty:
        print(
            f"\n\nXmitDidscard Counters:",
            f"\n##################################################",
            f"\n{df_xmit_drp.head(args.top_n).to_string(index=False)}",
        )
    else:
        print(
            f"\n\nXmitDidscard Counters: 0 on all links",
          #  f"\n##################################################",
          #  f"\nINFO: XmitDidscard counters are 0 on all links.",
        )

 
    if "--extended_speeds" in running_command_only :
     
        if not df_fec_uncorrectable.empty:
            print(
                f"\n\nPort FEC Uncorrectable Counters:",
                f"\n##################################################",
                f"\n{df_fec_uncorrectable.head(args.top_n).to_string(index=False)}",
            )
        else:
            print(
                f"\n\nPort FEC Uncorrectable Counters: 0 on all links.",
               # f"\n##################################################",
               # f"\nINFO: FEC Uncorrectable counters are 0 on all links.",
            )

    if not df_buf_overrun.empty:
        print(
            f"\n\nBuffer overrun Counters:",
            f"\n##################################################",
            f"\n{df_buf_overrun.head(args.top_n).to_string(index=False)}",
        )
    else:
        print(
            f"\n\nBuffer overrun Counters: 0 on all links "
           # f"\n##################################################",
           # f"\nINFO: ExcessiveBufferOverrunErrors counters are 0 on all links.",
        )


    if not df_max_retrans.empty:
        print(
            f"\n\Max Retransmission_rate : > 500:",
            f"\n##################################################",
            f"\n{df_max_retrans.head(args.top_n).to_string(index=False)}",
        )
    else:
        print(
            f"\n\nMax Retransmission_rate Counters: 0 on all links "
           # f"\n##################################################",
           # f"\nINFO: ExcessiveBufferOverrunErrors counters are 0 on all links.",
        )



    if not df_congestion_ext.empty:
        print(
            f"\n\nCongestion Indexes > 10:",
            f"\n##################################################",
            f"\n{df_congestion_ext.head(args.top_n).to_string(index=False)}",
        )
    else:
        print(
            f"\n\nCongestion Indexes : < 10 on all links:",
         #   f"\n##################################################",
         #   f"\nINFO: Congestion Indexes < 10 on all links.",
        )


if not df_ibdgnt_net_ext.empty:

    if not df_eff_ber.empty:
        print(
            f"\n\nEffective BER Counters > 1e-13:",
            f"\n##################################################",
            f"\n{df_eff_ber.head(args.top_n).to_string(index=False)}",
        )
    else:

        print(
            f"\n\nEffective BER Counters : <= 1e-13:",
        #    f"\n##################################################",
        #    f"\nINFO: Effective BER Counters <= 1e-13.",
        )

    if not df_symbol_ber.empty:

        if "SymbolBER" in df_symbol_ber:
            print(
                f"\n\nSymbol BER Counters > 1e-13, or Err > 0 ",
                f"\n##################################################",
                f"\n{df_symbol_ber.head(args.top_n).to_string(index=False)}",
            )

        else : 

            print(
                f"\n\nSymbol Err counters > 0 ",
                f"\n##################################################",
                f"\n{df_symbol_ber.head(args.top_n).to_string(index=False)}",
            )       

    else:

        print(
            f"\n\nSymbol BER Counters <= 1e-13, or Err < 0 ",
          #  f"\n##################################################",
          #  f"\nINFO: Symbol BER Counters <= 1e-13.",
        )

# Step 7. Save all outputs to excel file

if args.output_file:

    print(
        f"\n\nSaving to Excel file:",
        f"\n##################################################",
    )

    # 7.1 Create a Pandas Excel writer

    writer = pd.ExcelWriter(args.output_file, engine="openpyxl")

    # 7.2 Write each DataFrame to a specific sheet

    if not df_pm.empty:
        if not df_lnk_dn.empty:
            df_lnk_dn.to_excel(writer, sheet_name="Flapping_Links", index=False)
        if not df_xmit_drp.empty:
            df_xmit_drp.to_excel(writer, sheet_name="Output_Didscard_Links", index=False)
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

    # 7.3 Close the Pandas Excel writer

    writer.save()
    print(f"Data is written successfully to Excel File: {args.output_file}")