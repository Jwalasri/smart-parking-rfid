"""Simulate RFID gate events for a parking facility.

This script generates a CSV file of entry and exit events for a set
of RFID tags over a specified duration.  Each tag may produce
multiple entry/exit pairs.  The resulting CSV has columns
``timestamp``, ``tag_id`` and ``event`` (either ``entry`` or ``exit``).
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict

import numpy as np

from .registry import generate_registry, write_registry


def simulate_events(num_tags: int, duration_minutes: int, seed: int | None = None) -> List[Dict[str, any]]:
    """Generate gate entry/exit events for a set of tags.

    Parameters
    ----------
    num_tags:
        Number of unique tags.
    duration_minutes:
        Duration of the simulation window in minutes.
    seed:
        Optional random seed.

    Returns
    -------
    list of dict
        Each dict has ``timestamp`` (ISO string), ``tag_id`` and ``event``.
    """
    rng = np.random.default_rng(seed)
    start_time = datetime.utcnow()
    events: List[Dict[str, any]] = []
    tag_ids = [f"TAG{i:05d}" for i in range(num_tags)]
    for tag in tag_ids:
        # Each tag may have between 0 and 2 visits
        num_visits = rng.integers(0, 3)
        for _ in range(num_visits):
            entry_offset = rng.uniform(0, duration_minutes * 60)
            entry_time = start_time + timedelta(seconds=entry_offset)
            # Stay between 5 and 30 minutes
            exit_offset = entry_offset + rng.uniform(300, 1800)
            if exit_offset > duration_minutes * 60:
                # If exit goes beyond simulation, clip to end and mark as exit
                exit_offset = duration_minutes * 60
            exit_time = start_time + timedelta(seconds=exit_offset)
            events.append({"timestamp": entry_time.isoformat(timespec="seconds") + "Z", "tag_id": tag, "event": "entry"})
            events.append({"timestamp": exit_time.isoformat(timespec="seconds") + "Z", "tag_id": tag, "event": "exit"})
    # Sort events by timestamp
    events.sort(key=lambda e: e["timestamp"])
    return events


def write_events(events: List[Dict[str, any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "tag_id", "event"])
        writer.writeheader()
        writer.writerows(events)


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulate RFID gate events.")
    parser.add_argument(
        "--duration",
        type=int,
        default=120,
        help="Simulation duration in minutes.",
    )
    parser.add_argument(
        "--tags",
        type=int,
        default=50,
        help="Number of unique tags to simulate.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=str(Path(__file__).resolve().parents[1] / "data" / "events.csv"),
        help="Path to write the events CSV.",
    )
    parser.add_argument(
        "--registry_output",
        type=str,
        default=str(Path(__file__).resolve().parents[1] / "data" / "registry.csv"),
        help="Path to write the registry CSV.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility.",
    )
    args = parser.parse_args()
    # Generate registry and save
    registry = generate_registry(args.tags, seed=args.seed)
    write_registry(registry, Path(args.registry_output))
    # Generate events
    events = simulate_events(args.tags, args.duration, seed=args.seed)
    write_events(events, Path(args.output))
    print(f"Generated registry with {len(registry)} tags and {len(events)} events.")


if __name__ == "__main__":
    main()