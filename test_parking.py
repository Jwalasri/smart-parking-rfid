"""Unit tests for the smart parking RFID project."""

from pathlib import Path

import pandas as pd

from src.registry import generate_registry
from src.simulate_gate import simulate_events
from src.pipeline import run_pipeline


def test_generate_registry() -> None:
    registry = generate_registry(10, seed=0)
    assert len(registry) == 10
    for entry in registry:
        assert entry["tag_id"].startswith("TAG")
        assert entry["vehicle_id"].startswith("VEH")


def test_simulate_events_order() -> None:
    events = simulate_events(num_tags=5, duration_minutes=10, seed=1)
    # Events should be sorted by timestamp
    timestamps = [event["timestamp"] for event in events]
    assert timestamps == sorted(timestamps)
    # Event count should be even (entry/exit pairs)
    assert len(events) % 2 == 0


def test_pipeline(tmp_path: Path) -> None:
    # Create simple registry and events
    registry = generate_registry(2, seed=2)
    registry_path = tmp_path / "registry.csv"
    # Write registry
    import csv
    with registry_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["tag_id", "vehicle_id"])
        writer.writeheader()
        writer.writerows(registry)
    # Generate events for tags
    events = simulate_events(num_tags=2, duration_minutes=1, seed=3)
    events_path = tmp_path / "events.csv"
    with events_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "tag_id", "event"])
        writer.writeheader()
        writer.writerows(events)
    # Run pipeline
    output_path = tmp_path / "occupancy.csv"
    run_pipeline(registry_path, events_path, output_path)
    df = pd.read_csv(output_path)
    assert "occupancy" in df.columns
    # Occupancy should never be negative
    assert (df["occupancy"] >= 0).all()