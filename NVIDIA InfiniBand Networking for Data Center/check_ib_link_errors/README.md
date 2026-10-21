# InfiniBand Fabric Status Checker

`check_ib_link_status_v49.py` provides a quick health overview of an NVIDIA InfiniBand fabric by analyzing an existing `ibdiagnet2` output directory. It reports inventory, link errors, congestion, BER, bandwidth loss, temperature, cable, PSU, topology, and other fabric warnings to the console and can optionally save findings to an Excel workbook.

The script does not run `ibdiagnet` itself. Collect the diagnostic files on the fabric management host first, copy or extract the resulting directory to the analysis system, and then pass that directory with `-i`.

## Highlights in v49

- Supports NVIDIA XDR multi-plane link mapping, where one logical link may contain four planes.
- Checks `VL15DroppedExt` first and falls back to `VL15Dropped` when the extended counter is unavailable.
- Treats PM checks independently. A missing optional counter skips only the affected check instead of stopping all analysis.
- Prints a final completion summary listing checks that were skipped, adjusted, or partially processed.
- Adds stage-aware fatal error reporting with the problem item, processing stage, reason, and traceback for unexpected errors.
- Avoids pandas DataFrame fragmentation warnings during lost-bandwidth and TX/RX calculations.
- Makes `-c` a true cable bypass: `ibdiagnet2.cables` is not opened or parsed.
- Handles cable values containing additional colons, such as `SN: MT24:4NT05981`.
- Skips only an invalid cable block and reports it at completion instead of terminating the script.
- Prevents accidental Excel overwrite by adding a numeric suffix such as `_1` or `_2` when the requested file already exists.

## Requirements

- Python 3.8 or newer
- pandas
- openpyxl
- Windows Command Prompt or PowerShell is the primary tested environment
- This script may not work in MAC & Linux Server. Because my labtop is Window, so i...If you want, you can develop it for Linux/Mac

Install the required Python packages & Check the installed versions

```powershell
python -m pip install pandas openpyxl
python --version
pip3 list
```

## Collecting ibdiagnet data. 2 methods

1. A basic collection suitable for inventory, PM counters, extended-speed counters, BER, and cable checks is:

```bash
ibdiagnet -r -P all=1 \
  --extended_speeds all \
  --pm_per_lane \
  --get_phy_info \
  --get_cable_info

tar -czf ibdiagnet2_A.tar.gz /var/tmp/ibdiagnet2/
```

2. For lost-bandwidth and TX/RX rate calculations, collect two PM samples with `--pm_pause_time`:

```bash
ibdiagnet -r \
  --pc \
  --reset_phy_info \
  --pm_pause_time 600 \
  -P all=1 \
  --extended_speeds all \
  --pm_per_lane \
  --get_phy_info \
  --get_cable_info

tar -czf ibdiagnet2_B.tar.gz /var/tmp/ibdiagnet2/
```

Collection options determine which checks are available. For example:

- `--pm_pause_time`: enables lost-bandwidth and TX/RX bandwidth calculations.
- `--extended_speeds all`: supplies extended speed and FEC counters when supported.
- `--pm_per_lane`: supplies per-lane PM data when supported.
- `--get_phy_info`: supplies BER and additional physical-layer information.
- `--get_cable_info`: creates cable data used by third-party and temperature checks.
- Routing and rail-validation options are required if those warnings should appear in the ibdiagnet log.

## Usage

```text
python check_ib_link_status_v49.py -i IBDIAGNET_FOLDER [options]
```

### Options

| Option | Description |
|---|---|
| `-i`, `--ibdiagnet-folder` | Required. Path to the extracted `ibdiagnet2` output directory. |
| `-o`, `--output-file` | Write non-empty findings to an `.xlsx` workbook. |
| `-n`, `--top-n` | Maximum console rows per result section. Default: `10`. |
| `-s`, `--skip-lid-checking` | Skip invalid LID and multicast LID validation. |
| `-c`, `--skip-cable-checking` | Do not read or parse `ibdiagnet2.cables`. Recommended for very large cable files when cable checks are unnecessary. |
| `-d`, `--debug` | Write the merged PM data to `For_debugging_data_all`. |
| `-a`, `--all` | Display detailed server/switch TX/RX bandwidth and lost-bandwidth tables. Requires `--pm_pause_time` in the original ibdiagnet command. |
| `-v`, `--version` | Print the script version string and exit. |

### Examples

Analyze a collection and print the first 10 rows in each section:

```powershell
python check_ib_link_status_v49.py -i .\ibdiagnet2
```

Print the first 20 rows:

```powershell
python check_ib_link_status_v49.py -i .\ibdiagnet2 -n 20
```

Skip cable parsing for a large fabric:

```powershell
python check_ib_link_status_v49.py -i .\ibdiagnet2 -c
```

Skip cable and LID checks:

```powershell
python check_ib_link_status_v49.py -i .\ibdiagnet2 -c -s
```

Command lists:

```powershell
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
```

If `ib_fabric_status.xlsx` already exists, the script uses `ib_fabric_status_1.xlsx`, then `_2`, and so on. Existing workbooks are not overwritten.

## Input files

The following files are read from the directory supplied with `-i`:

| File | Status | Used for |
|---|---|---|
| `ibdiagnet2.log` | Required | Original ibdiagnet command, APort symmetry, speed/width, rail topology, and PCI degradation warnings. |
| `ibdiagnet2.net_dump` | Required | Active link mapping, source/destination devices, GUIDs, ports, width, and speed. |
| `ibdiagnet2.db_csv` | Required | PM counters, switch/HCA/GPU inventory, temperature, PSU, and other database sections. |
| `ibdiagnet2.net_dump_ext` | Optional | Raw, effective, and symbol BER information. Missing data skips BER checks. |
| `ibdiagnet2.ibnetdiscover` | Optional | Invalid LID/multicast LID and remote-peer-not-responding checks. |
| `ibdiagnet2.cables` | Optional | Cable vendor, part number, serial number, and temperature. Not read when `-c` is used. |

The input folder, `ibdiagnet2.log`, `ibdiagnet2.net_dump`, and `ibdiagnet2.db_csv` are fundamental inputs. If one of these is unavailable or cannot be used, the script stops with a stage-aware fatal error.

## Checks and thresholds

### Inventory

- IB switch/ASIC quantity, PSID/model mapping, and firmware versions
- HCA quantity, PSID/model mapping, and firmware versions
- GPU inventory when matching GPU node records are available

### PM and link counters

| Check | Threshold or behavior |
|---|---|
| Link down | `LinkDownedCounter > 0` |
| Transmit discard | `PortXmitDiscards > 0` |
| FEC uncorrectable | `PortFECUncorrectableBlockCounter > 0` when extended-speed data is available |
| Buffer overrun | `ExcessiveBufferOverrunErrors != 0` |
| VL15 drop | Prefer `VL15DroppedExt`; fall back to `VL15Dropped`; report values `> 10` |
| Maximum retransmission rate | `max_retransmission_rate > 500` |
| Congestion index | `PortXmitWaitExt / PortXmitPktsExtended >= 10` |

Each counter is evaluated independently. For example, if `PortXmitWaitExt` is absent, the congestion and dependent bandwidth checks can be skipped while link-down, discard, buffer-overrun, VL15, and other available checks continue.

### BER

- Effective BER: `> 1e-13`
- Symbol BER: `> 1e-13`
- Legacy symbol error count: `> 0`
- Raw BER: `> 1e-5` for Symbol BER format, or `> 2e-5` for the legacy Symbol Err format

### Bandwidth

When the original collection command contains `--pm_pause_time`, the script calculates:

- Lost bandwidth in Gbps
- Current TX and RX bandwidth in Gbps
- Server-to-switch and switch-to-server bandwidth
- Switch-to-switch TX/RX bandwidth
- All-port TX/RX bandwidth when `-a` is selected

### Hardware and fabric validation

- IB device or switch ASIC temperature at 70°C or higher
- Third-party cable vendor detection
- Cable temperature above 70°C
- PSU problems: missing/non-FRU PSU, DC error, or active alert
- Invalid LID and multicast LID values
- APort symmetry errors
- Link speed/width errors
- Rail-optimized topology warnings
- PCI degradation warnings
- Ports that are UP while the remote peer is not responding

## Excel output

Use `-o` to create an Excel workbook. Sheets are created only when the corresponding result contains data.

Possible sheets include:

- `IB_Switch_Summary`
- `HCA_Inventory_Summary`
- `GPU_Inventory_Summary`
- `Invalid LID & Mcast checking`
- `Flapping_Links`
- `Output_Didscard_Links`
- `FEC_Uncorrectable_Links`
- `Buf_Overrun_Links`
- `VL15_Drop`
- `Congested_Links`
- `Max_Retransmission_rate`
- `Effective_BER_Links`
- `Symbol_BER_Links`
- `Raw_BER_Links`
- `Lost_Bandwidth`
- `Server_Tx_Bandwidth`
- `Server_Rx_Bandwidth`
- `Switch_Tx_Bandwidth`
- `Switch_Rx_Bandwidth`
- `All_port_TX_RX_Bandwidth`
- `IB device and Asic temperature`
- `3rd party cables`
- `Cable Temperature >70c`
- `PSU problem regarding`
- `APort_Symmetry_Errors`
- `Links_Speed_Width_Errors`
- `PCI_degradation_warnings`
- `Rail_topology_warnings`
- `Remote_peer_not_responding`

## Large-fabric recommendations

- Use `-c` if `ibdiagnet2.cables` is very large and cable analysis is not required. In v49 the file is completely bypassed.
- Use `-s` if LID validation is not needed.


## Screenshot

<img width="1060" height="1870" alt="Example script output" src="https://github.com/user-attachments/assets/520bab03-0f91-4566-871e-0d5c59c6dbf6" />

