#!/usr/bin/env python3
"""
NVLSM mapping visualizer: GPU ALID / PLID (NVLID) and NVSwitch ASIC LID (planes).

Reads nvlsm dump files (same layout as nvidia nvlsm):
  - guid2alid   : GPU base GUID -> Application LID (ALID)
  - guid2nvlid  : per-plane GPU GUID -> NVLink LID (PLID in fabric terms)
  - guid2lid    : NVSwitch GUID -> Local ID (LID)
  - guid2planes : NVSwitch GUID -> plane index (1..18 typical for NVL72)
  - neighbors   : endpoint:port pairs linking GPU plane GUIDs to switch GUIDs

GPU "planes" are separate GUIDs sharing the first 13 hex digits (last 3 hex digits vary),
each with its own PLID in guid2nvlid.

Usage:
  python nvlsm_mapping_visualizer.py --nvlsm-dir "path/to/nvlsm" --out diagram.png
  python nvlsm_mapping_visualizer.py --nvlsm-dir "path/to/nvlsm" --mode heatmap --out heatmap.png
  python nvlsm_mapping_visualizer.py --nvlsm-dir "path/to/nvlsm" --gpu-index 0 --out gpu0.png
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple

# -----------------------------------------------------------------------------
# Parsing
# -----------------------------------------------------------------------------


def _norm_guid(g: str) -> str:
    g = g.strip().lower()
    if g.startswith("0x"):
        g = g[2:]
    return g


def parse_guid2alid(path: Path) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        guid = _norm_guid(parts[0])
        alid = int(parts[1], 16)
        out[guid] = alid
    return out


def parse_guid_hex_map(path: Path) -> Dict[str, int]:
    """guid2lid style: guid val1 val2 (use first value)."""
    out: Dict[str, int] = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        guid = _norm_guid(parts[0])
        val = int(parts[1], 16)
        out[guid] = val
    return out


def parse_guid2planes(path: Path) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        guid = _norm_guid(parts[0])
        out[guid] = int(parts[1], 10)
    return out


def parse_guid2nvlid(path: Path) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        guid = _norm_guid(parts[0])
        plid = int(parts[1], 16)
        out[guid] = plid
    return out


def parse_neighbors(path: Path) -> List[Tuple[str, int, str, int]]:
    rows: List[Tuple[str, int, str, int]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        a, b = parts[0], parts[1]
        ga, pa = a.split(":", 1)
        gb, pb = b.split(":", 1)
        rows.append((_norm_guid(ga), int(pa, 10), _norm_guid(gb), int(pb, 10)))
    return rows


def guid_prefix13(guid: str) -> str:
    """Group GPU plane GUIDs: first 13 hex chars; last 3 hex digits vary per plane."""
    if len(guid) < 13:
        return guid
    return guid[:13]


# -----------------------------------------------------------------------------
# Topology model
# -----------------------------------------------------------------------------


@dataclass
class SwitchInfo:
    guid: str
    lid: int
    plane: int


@dataclass
class GpuPlaneLink:
    gpu_sub_guid: str
    plid: int
    switch_guid: str
    switch_lid: int
    plane: int


@dataclass
class GpuInfo:
    base_guid: str
    alid: int
    plane_links: List[GpuPlaneLink] = field(default_factory=list)


def build_topology(nvlsm_dir: Path) -> Tuple[Dict[str, SwitchInfo], List[GpuInfo], Dict[str, str]]:
    d = nvlsm_dir
    guid2alid = parse_guid2alid(d / "guid2alid")
    guid2nvlid = parse_guid2nvlid(d / "guid2nvlid")
    guid2lid_sw = parse_guid_hex_map(d / "guid2lid")
    guid2planes = parse_guid2planes(d / "guid2planes")
    neighbors = parse_neighbors(d / "neighbors")

    switch_by_guid: Dict[str, SwitchInfo] = {}
    for sg, lid in guid2lid_sw.items():
        plane = guid2planes.get(sg, -1)
        switch_by_guid[sg] = SwitchInfo(guid=sg, lid=lid, plane=plane)

    # GPU sub-guid -> switch guid (from neighbors)
    gpu_side: Dict[str, str] = {}
    for ga, _pa, gb, _pb in neighbors:
        a_sw = ga in guid2lid_sw
        b_sw = gb in guid2lid_sw
        if a_sw and not b_sw:
            gpu_side[gb] = ga
        elif b_sw and not a_sw:
            gpu_side[ga] = gb

    # Base GPU GUIDs (have ALID)
    base_guids = sorted(guid2alid.keys(), key=lambda g: guid2alid[g])

    gpus: List[GpuInfo] = []
    for bg in base_guids:
        alid = guid2alid[bg]
        pfx = guid_prefix13(bg)
        sub_guids = sorted(
            [g for g in guid2nvlid if guid_prefix13(g) == pfx],
            key=lambda x: x,
        )
        gi = GpuInfo(base_guid=bg, alid=alid)
        for sg in sub_guids:
            plid = guid2nvlid[sg]
            sw = gpu_side.get(sg)
            if not sw:
                continue
            info = switch_by_guid.get(sw)
            if not info:
                continue
            gi.plane_links.append(
                GpuPlaneLink(
                    gpu_sub_guid=sg,
                    plid=plid,
                    switch_guid=sw,
                    switch_lid=info.lid,
                    plane=info.plane,
                )
            )
        gi.plane_links.sort(key=lambda lk: (lk.plane if lk.plane >= 0 else 999, lk.plid))
        gpus.append(gi)

    return switch_by_guid, gpus, gpu_side


def switches_sorted_by_plane(switch_by_guid: Dict[str, SwitchInfo]) -> List[SwitchInfo]:
    lst = list(switch_by_guid.values())
    lst.sort(key=lambda s: (s.plane if s.plane >= 0 else 999, s.lid))
    return lst


# -----------------------------------------------------------------------------
# Export CSV (optional)
# -----------------------------------------------------------------------------


def write_csv(out_path: Path, gpus: List[GpuInfo], switches: List[SwitchInfo]) -> None:
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["gpu_rank", "base_guid", "alid_dec", "alid_hex", "plane_idx", "plid_hex", "plid_dec", "switch_guid", "switch_lid_dec", "switch_lid_hex"])
        for rank, g in enumerate(gpus):
            if not g.plane_links:
                w.writerow([rank + 1, g.base_guid, g.alid, f"0x{g.alid:04x}", "", "", "", "", "", ""])
            for lk in g.plane_links:
                w.writerow(
                    [
                        rank + 1,
                        g.base_guid,
                        g.alid,
                        f"0x{g.alid:04x}",
                        lk.plane,
                        f"0x{lk.plid:04x}",
                        lk.plid,
                        lk.switch_guid,
                        lk.switch_lid,
                        f"0x{lk.switch_lid:04x}",
                    ]
                )


# -----------------------------------------------------------------------------
# Matplotlib diagrams
# -----------------------------------------------------------------------------


def draw_topology_diagram(
    switch_by_guid: Dict[str, SwitchInfo],
    gpu: GpuInfo,
    gpu_index: int,
    out_path: Path,
    dpi: int,
) -> None:
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch

    switches = switches_sorted_by_plane(switch_by_guid)
    n_sw = max(1, len(switches))
    fig_w = max(14, n_sw * 0.85)
    fig, ax = plt.subplots(figsize=(fig_w, 8), dpi=dpi)
    ax.set_xlim(0, n_sw)
    ax.set_ylim(0, 10)
    ax.axis("off")

    y_top = 8.0
    y_bot = 2.0
    # Top: switches
    for i, sw in enumerate(switches):
        x = i + 0.5
        w, h = 0.75, 0.9
        rect = FancyBboxPatch(
            (x - w / 2, y_top - h / 2),
            w,
            h,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            linewidth=1.2,
            edgecolor="#b22222",
            facecolor="#ffcccc",
        )
        ax.add_patch(rect)
        label = f"NVSwitch\nplane {sw.plane}\nLID {sw.lid}\n(0x{sw.lid:04x})"
        ax.text(x, y_top, label, ha="center", va="center", fontsize=7)

    # Bottom: one GPU with PLID chips
    gx = n_sw / 2
    gw = min(n_sw * 0.9, 18)
    gh = 1.4
    gpu_rect = FancyBboxPatch(
        (gx - gw / 2, y_bot - gh / 2),
        gw,
        gh,
        boxstyle="round,pad=0.03,rounding_size=0.12",
        linewidth=1.5,
        edgecolor="#228b22",
        facecolor="#ccffcc",
    )
    ax.add_patch(gpu_rect)
    title = f"GPU #{gpu_index + 1}  ALID {gpu.alid} (0x{gpu.alid:04x})\n{gpu.base_guid}"
    ax.text(gx, y_bot + 0.35, title, ha="center", va="center", fontsize=9, weight="bold")

    links = gpu.plane_links
    n_pl = len(links)
    if n_pl == 0:
        ax.text(gx, y_bot - 0.35, "No plane links parsed (check neighbors / nvlid)", ha="center", fontsize=9, color="red")
    else:
        inner_w = gw * 0.92
        slot = inner_w / n_pl
        x0 = gx - inner_w / 2 + slot / 2
        for j, lk in enumerate(links):
            px = x0 + j * slot
            pw = slot * 0.82
            ph = 0.55
            small = FancyBboxPatch(
                (px - pw / 2, y_bot - 0.55 - ph / 2),
                pw,
                ph,
                boxstyle="round,pad=0.01,rounding_size=0.04",
                linewidth=0.8,
                edgecolor="#1e6fa8",
                facecolor="#cceeff",
            )
            ax.add_patch(small)
            ax.text(px, y_bot - 0.55, f"PLID\n0x{lk.plid:04x}", ha="center", va="center", fontsize=5)
            # find switch x for this guid
            sw_x = None
            for i, sw in enumerate(switches):
                if sw.guid == lk.switch_guid:
                    sw_x = i + 0.5
                    break
            if sw_x is not None:
                ax.plot(
                    [px, sw_x],
                    [y_bot - 0.55 - ph / 2, y_top - 0.45],
                    color="black",
                    linewidth=0.6,
                    zorder=0,
                )

    ax.set_title("NVLSM: GPU ALID / PLID ↔ NVSwitch LID (planes)", fontsize=12)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)


def draw_heatmap(
    switch_by_guid: Dict[str, SwitchInfo],
    gpus: List[GpuInfo],
    out_path: Path,
    dpi: int,
) -> None:
    import matplotlib.pyplot as plt
    import numpy as np

    switches = switches_sorted_by_plane(switch_by_guid)
    plane_nums = [s.plane for s in switches if s.plane >= 0]
    max_plane = max(plane_nums) if plane_nums else 18
    n_cols = max_plane
    n_rows = len(gpus)
    mat = np.full((n_rows, n_cols), np.nan)
    for ri, g in enumerate(gpus):
        for lk in g.plane_links:
            if 1 <= lk.plane <= n_cols:
                mat[ri, lk.plane - 1] = float(lk.plid)

    fig, ax = plt.subplots(figsize=(min(20, n_cols * 0.45 + 4), max(6, n_rows * 0.22 + 2)), dpi=dpi)
    im = ax.imshow(mat, aspect="auto", cmap="viridis")
    ax.set_xlabel("Plane index (from guid2planes)")
    ax.set_ylabel("GPU (sorted by ALID)")
    ax.set_xticks(range(n_cols))
    ax.set_xticklabels([str(i + 1) for i in range(n_cols)], fontsize=7)
    ax.set_yticks(range(n_rows))
    ax.set_yticklabels([f"#{i+1} ALID {g.alid}" for i, g in enumerate(gpus)], fontsize=6)
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("PLID (decimal from NVLID)")
    ax.set_title("PLID per GPU row vs NVSwitch plane column (NVLSM)")
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)


def draw_compact_overview(
    switch_by_guid: Dict[str, SwitchInfo],
    gpus: List[GpuInfo],
    out_path: Path,
    dpi: int,
) -> None:
    """Small multiples: first N GPUs in a grid."""
    import matplotlib.pyplot as plt

    n = min(len(gpus), 12)
    cols = 4
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 3.2, rows * 2.2), dpi=dpi)
    axes_flat = axes.flatten() if n > 1 else [axes]

    switches = switches_sorted_by_plane(switch_by_guid)
    for idx in range(rows * cols):
        ax = axes_flat[idx]
        ax.axis("off")
        if idx >= n:
            continue
        g = gpus[idx]
        ax.set_title(f"GPU #{idx+1} ALID {g.alid}", fontsize=8)
        lines = [f"p{lk.plane}: PLID 0x{lk.plid:04x} → SW LID {lk.switch_lid}" for lk in g.plane_links[:24]]
        if len(g.plane_links) > 24:
            lines.append("…")
        ax.text(0.02, 0.98, "\n".join(lines) if lines else "(no links)", va="top", fontsize=6, family="monospace")

    fig.suptitle("GPU ↔ plane mapping (subset)", fontsize=11)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser(description="Visualize NVLSM ALID / PLID / Switch LID mapping.")
    ap.add_argument("--nvlsm-dir", type=Path, required=True, help="Directory containing nvlsm files")
    ap.add_argument("--out", type=Path, default=Path("nvlsm_mapping.png"), help="Output image path")
    ap.add_argument(
        "--mode",
        choices=("topology", "heatmap", "overview", "csv"),
        default="topology",
        help="topology: one GPU diagram; heatmap: all GPUs; overview: text grid; csv: table only",
    )
    ap.add_argument("--gpu-index", type=int, default=0, help="Which GPU (0-based, ALID order) for topology mode")
    ap.add_argument("--dpi", type=int, default=150)
    args = ap.parse_args()

    nvdir = args.nvlsm_dir
    for name in ("guid2alid", "guid2nvlid", "guid2lid", "guid2planes", "neighbors"):
        p = nvdir / name
        if not p.is_file():
            raise SystemExit(f"Missing required file: {p}")

    switch_by_guid, gpus, _gpu_side = build_topology(nvdir)
    switches = switches_sorted_by_plane(switch_by_guid)

    if args.mode == "csv":
        csv_path = args.out.with_suffix(".csv") if args.out.suffix.lower() not in (".csv",) else args.out
        write_csv(csv_path, gpus, switches)
        print(f"Wrote {csv_path}")
        return

    if args.mode == "heatmap":
        draw_heatmap(switch_by_guid, gpus, args.out, args.dpi)
    elif args.mode == "overview":
        draw_compact_overview(switch_by_guid, gpus, args.out, args.dpi)
    else:
        idx = max(0, min(args.gpu_index, len(gpus) - 1))
        draw_topology_diagram(switch_by_guid, gpus[idx], idx, args.out, args.dpi)

    print(f"Wrote {args.out} ({args.mode}, {len(gpus)} GPUs, {len(switches)} switches)")


if __name__ == "__main__":
    main()
