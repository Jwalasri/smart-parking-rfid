"""Merge RFID events with the tag registry and compute occupancy over time."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def run_pipeline(registry_path: Path, events_path: Path, output_path: Path) -> None:
    """Process gate events and compute occupancy.

    Parameters
    ----------
    registry_path:
        Path to the CSV file mapping tag IDs to vehicle IDs.
    events_path:
        Path to the CSV file of gate events.
    output_path:
        Path to write the output occupancy CSV.
    """
    registry = pd.read_csv(registry_path)
    events = pd.read_csv(events_path)
    # Merge events with registry to include vehicle_id; left join ensures unknown tags are kept
    merged = events.merge(registry, how="left", on="tag_id")
    # Sort by timestamp to process chronologically
    merged["timestamp"] = pd.to_datetime(merged["timestamp"], errors="coerce")
    merged = merged.sort_values("timestamp").reset_index(drop=True)
    occupancy = 0
    occupancy_list = []
    for _, row in merged.iterrows():
        event = row["event"]
        if event == "entry":
            occupancy += 1
        elif event == "exit":
            occupancy = max(0, occupancy - 1)
        occupancy_list.append(occupancy)
    merged["occupancy"] = occupancy_list
    output_path.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(output_path, index=False)
    print(f"Wrote occupancy data with {len(merged)} rows to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge RFID events with registry and compute occupancy.")
    parser.add_argument("--registry", type=str, required=True, help="Path to the registry CSV file.")
    parser.add_argument("--events", type=str, required=True, help="Path to the events CSV file.")
    parser.add_argument(
        "--output",
        type=str,
        default=str(Path(__file__).resolve().parents[1] / "data" / "occupancy.csv"),
        help="Path to write the output CSV.",
    )
    args = parser.parse_args()
    run_pipeline(Path(args.registry), Path(args.events), Path(args.output))


if __name__ == "__main__":
    main()