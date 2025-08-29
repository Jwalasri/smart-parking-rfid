"""Utility functions for managing an RFID tag registry."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import List, Dict

import numpy as np


def generate_registry(num_tags: int, seed: int | None = None) -> List[Dict[str, any]]:
    """Generate a synthetic registry mapping tag IDs to vehicle identifiers.

    Parameters
    ----------
    num_tags:
        Number of unique tags to generate.
    seed:
        Optional random seed for reproducibility.

    Returns
    -------
    list of dict
        Each dict contains ``tag_id`` and ``vehicle_id``.
    """
    rng = np.random.default_rng(seed)
    registry = []
    for i in range(num_tags):
        tag_id = f"TAG{i:05d}"
        vehicle_id = f"VEH{rng.integers(0, 99999):05d}"
        registry.append({"tag_id": tag_id, "vehicle_id": vehicle_id})
    return registry


def write_registry(registry: List[Dict[str, any]], path: Path) -> None:
    """Write the tag registry to a CSV file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["tag_id", "vehicle_id"])
        writer.writeheader()
        writer.writerows(registry)