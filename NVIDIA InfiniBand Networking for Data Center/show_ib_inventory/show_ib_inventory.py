# =============================================================================
# File name: show_ib_inventory.py
# Description: extract IB SW and HCA info from ibdiagnet2.db_csv
# Author: Jie Wu
# Date created: 4/12/2021
# Date last modified: 8/2/2021
# Software: python 3.8+, Pandas and OpenPyXL libraries
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
    help="write IB SW and HCA inventory info to xlsx file"
)
parser.add_argument(
    "-f", "--show-ib-hosts", action="store_true",
    help="print detailed HCA inventory info"
)
parser.add_argument(
    "-s", "--show-ib-switches", action="store_true",
    help="print detailed IB switch inventory info"
)
parser.add_argument(
    "-v", "--version", action="version", version="%(prog)s 1.2",
    help="print current script version"
)
args = parser.parse_args()


def csv_extractor(separator, file):

    regexp = re.compile(
        r"^START_" + separator + r"$\n"         # starting separator
        r"((.*\n)+)"                            # csv table
        r"^END_" + separator + r"$\n",          # ending separator
        re.MULTILINE
    )

    regexp_result = re.search(regexp, file)

    if regexp_result:
        return pd.read_csv(io.StringIO(regexp_result.group(1)))
    else:
        return pd.DataFrame()


# Step 1. Load ibdiagnet2.db_csv file

print("\nStart to parse ibdiagnet2.db_csv ...")

ibdgnt_db = args.ibdiagnet_folder + "/ibdiagnet2.db_csv"

if os.path.isfile(ibdgnt_db):

    with open(ibdgnt_db, "r", encoding="utf-8", errors="ignore") as db_csv_file:
        db_csv = db_csv_file.read()

    # 1.1 Extract NODES CSV table from ibdiagnet2.db_csv

    df_nodes_tbl = csv_extractor("NODES", db_csv)

    df_nodes_tbl = df_nodes_tbl[["NodeGUID", "NodeDesc"]]

    # 1.2 Extract NODES_INFO CSV table from ibdiagnet2.db_csv

    df_nodes_info_tbl = csv_extractor("NODES_INFO", db_csv)

    df_nodes_info_tbl["FWInfo_Version"] = (
        df_nodes_info_tbl["FWInfo_Extended_Major"].apply(int, base=16).astype(str) + "."
        + df_nodes_info_tbl["FWInfo_Extended_Minor"].apply(int, base=16).astype(str) + "."
        + df_nodes_info_tbl["FWInfo_Extended_SubMinor"].apply(int, base=16).astype(str)
    )
    df_nodes_info_tbl = df_nodes_info_tbl[["NodeGUID", "FWInfo_PSID", "FWInfo_Version"]]

    # 1.3 Extract SWITCHES CSV table from ibdiagnet2.db_csv

    df_sw_tbl = csv_extractor("SWITCHES", db_csv)

    df_sw_tbl = df_sw_tbl[["NodeGUID"]]

    # 1.4 Extract SYSTEM_GENERAL_INFORMATION CSV table from ibdiagnet2.db_csv

    df_sw_info_tbl = csv_extractor("SYSTEM_GENERAL_INFORMATION", db_csv)

else:
     print("\nCouldn't find ibdiagnet2.db_csv. Existing ...")
     exit()

# Step 2. Generate IB switch inventory table

# 2.1 Extract NodeDesc

df_sw_tbl = pd.merge(
    left=df_sw_tbl, right=df_nodes_tbl, on="NodeGUID"
)

# 2.2 Extract FWInfo_PSID & FWInfo_Version

df_sw_tbl = pd.merge(
    left=df_sw_tbl, right=df_nodes_info_tbl, on="NodeGUID"
)

# 2.3 Extract PartNumber, Revision and SerialNumber if section SYSTEM_GENERAL_INFORMATION exists

if df_sw_info_tbl.empty:
    print(
        f"\nINFO: SYSTEM_GENERAL_INFORMATION section couldn't be found in ibdiagnet2.db_csv.",
        f"\nINFO: It's impossible to display detailed SW info, such as PN, SN and HW RN.",
    )

    df_sw_tbl = df_sw_tbl[["NodeDesc", "NodeGUID", "FWInfo_PSID", "FWInfo_Version"]]

else:

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

# 2.4 Generate SW pivot table

df_ib_sw_pivot = pd.pivot_table(
    df_sw_tbl, index="FWInfo_PSID", columns="FWInfo_Version", aggfunc="size"
)

# Step 3. Generate HCA inventory table

# 3.1 Extract NodeDesc

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

# Step 4. Print out the results

# 4.1 Print IB swtich inventory summary

if not df_sw_tbl.empty:
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

if not df_hca_tbl.empty:
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

# 4.3 Print detailed IB switch inventory info

if args.show_ib_switches and (not df_sw_tbl.empty):
    print(
        f"\n\nIB Switch Inventory Details:",
        f"\n##################################################",
        f"\n{df_sw_tbl.to_string(index=False)}",
    )

# 4.4 Print detailed HCA inventory info

if args.show_ib_hosts and (not df_hca_tbl.empty):
    print(
        f"\n\nHCA Inventory Details:",
        f"\n##################################################",
        f"\n{df_hca_tbl.to_string(index=False)}",
    )

# Step 5: Save all outputs to excel file

if args.output_file:
    print(
        f"\n\nSaving to Excel file:",
        f"\n##################################################",
    )

    # 5.1 Create a Pandas Excel writer

    writer = pd.ExcelWriter(args.output_file, engine="openpyxl")

    # 5.2 Write each DataFrame to a specific sheet

    if not df_sw_tbl.empty:
        df_ib_sw_pivot.to_excel(writer, sheet_name="IB_Switch_Summary")
        df_sw_tbl.to_excel(writer, sheet_name="IB_Switch_Details", index=False)

    if not df_hca_tbl.empty:
        df_hca_pivot.to_excel(writer, sheet_name="HCA_Inventory_Summary")
        df_hca_tbl.to_excel(writer, sheet_name="HCA_Inventory_Details", index=False)

    # 5.3 Close the Pandas Excel writer

    writer.save()
    print(f"Data is written successfully to Excel File: {args.output_file}")