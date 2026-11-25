"""Shared, safe file storage for iOrchid sensor readings and presets."""

from __future__ import annotations

import csv
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path


def zone_data_dir(zone: str) -> Path:
    return Path(zone) / "data_DO_NOT_MODIFY"


def atomic_write_text(path: Path, content: str) -> None:
    """Replace a file atomically so readers never see it half-written."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_name = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temp_file:
            temp_name = temp_file.name
            temp_file.write(content)
            temp_file.flush()
            os.fsync(temp_file.fileno())

        os.replace(temp_name, path)
    finally:
        if temp_name and os.path.exists(temp_name):
            os.unlink(temp_name)


def write_current_reading(zone: str, filename: str, value: int) -> None:
    atomic_write_text(zone_data_dir(zone) / filename, f"{int(value)}\n")


def read_integer(path: Path) -> int | None:
    try:
        raw = Path(path).read_text(encoding="utf-8").strip()
        return int(raw) if raw else None
    except (OSError, ValueError):
        return None


def save_preset(zone: str, sensor: str, minimum: int, maximum: int) -> None:
    if minimum > maximum:
        raise ValueError("Minimum value cannot be greater than maximum value.")

    path = zone_data_dir(zone) / "presets" / f"{sensor}.txt"
    atomic_write_text(path, f"{minimum}\n{maximum}\n")


def read_preset(zone: str, sensor: str) -> tuple[int, int] | None:
    path = zone_data_dir(zone) / "presets" / f"{sensor}.txt"
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
        if len(lines) < 2:
            return None

        minimum, maximum = int(lines[0].strip()), int(lines[1].strip())
        if minimum > maximum:
            return None
        return minimum, maximum
    except (OSError, ValueError):
        return None


def append_history(zone: str, sensor: str, value: int) -> None:
    """Append one timestamped sample to the sensor's CSV history."""
    history_dir = zone_data_dir(zone) / "history"
    history_dir.mkdir(parents=True, exist_ok=True)
    history_path = history_dir / f"{sensor}.csv"
    is_new = not history_path.exists()

    with history_path.open("a", newline="", encoding="utf-8") as history_file:
        writer = csv.writer(history_file)
        if is_new:
            writer.writerow(("timestamp", "value"))
        writer.writerow((datetime.now(timezone.utc).isoformat(), int(value)))


def read_history(zone: str, sensor: str) -> list[tuple[datetime, int]]:
    history_path = zone_data_dir(zone) / "history" / f"{sensor}.csv"
    samples: list[tuple[datetime, int]] = []

    try:
        with history_path.open("r", newline="", encoding="utf-8") as history_file:
            reader = csv.DictReader(history_file)
            for row in reader:
                try:
                    timestamp = datetime.fromisoformat(row["timestamp"])
                    value = int(row["value"])
                    samples.append((timestamp, value))
                except (KeyError, TypeError, ValueError):
                    # Ignore a malformed row rather than breaking the graph.
                    continue
    except OSError:
        return []

    return samples
