from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data"
FIGURES_DIR = Path(__file__).resolve().parent / "correlate_figs"
EXCLUDED_EVENTS = {"333mbo", "magic", "mmagic", "333ft"}


def _latest_export_dir(prefix: str, required_files: tuple[str, ...]) -> Path:
    candidates = []
    for path in DATA_DIR.glob(f"{prefix}*"):
        if path.is_dir() and all((path / file_name).exists() for file_name in required_files):
            candidates.append(path)

    if not candidates:
        files = ", ".join(required_files)
        raise FileNotFoundError(f"No {prefix} export in {DATA_DIR} containing: {files}")

    return sorted(candidates, key=lambda path: path.name)[-1]


def latest_wca_export_dir() -> Path:
    return _latest_export_dir(
        "WCA_export",
        ("WCA_export_ranks_single.tsv",),
    )


def latest_cubingcontests_export_dir() -> Path:
    return _latest_export_dir(
        "CubingContests_export",
        ("export_results.csv", "export_persons.csv"),
    )


def load_wca_single_ranks(wca_export_dir: Path | None = None) -> list[dict[str, object]]:
    wca_export_dir = wca_export_dir or latest_wca_export_dir()
    rows = []
    with (wca_export_dir / "WCA_export_ranks_single.tsv").open(newline="") as file:
        reader = csv.DictReader(file, delimiter="\t")
        for row in reader:
            rows.append(
                {
                    "personId": row["person_id"],
                    "eventId": row["event_id"],
                    "worldRank": int(row["world_rank"]),
                }
            )
    return rows


def load_cubingcontests_fto_single_ranks(
    cubingcontests_export_dir: Path | None = None,
) -> list[dict[str, object]]:
    cubingcontests_export_dir = cubingcontests_export_dir or latest_cubingcontests_export_dir()

    cc_person_to_wca_id = {}
    with (cubingcontests_export_dir / "export_persons.csv").open(newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["wca_id"]:
                cc_person_to_wca_id[int(row["id"])] = row["wca_id"]

    best_by_person: dict[int, int] = {}
    with (cubingcontests_export_dir / "export_results.csv").open(newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["event_id"] != "fto" or row["approved"].upper() != "TRUE":
                continue

            best = int(row["best"] or 0)
            if best <= 0:
                continue

            person_ids = json.loads(row["person_ids"])
            if len(person_ids) != 1:
                continue

            cc_person_id = int(person_ids[0])
            if cc_person_id not in best_by_person or best < best_by_person[cc_person_id]:
                best_by_person[cc_person_id] = best

    ranks_by_person = _competition_ranks(best_by_person)
    return [
        {"personId": cc_person_to_wca_id[cc_person_id], "eventId": "fto", "worldRank": world_rank}
        for cc_person_id, world_rank in ranks_by_person.items()
        if cc_person_id in cc_person_to_wca_id
    ]


def _competition_ranks(values: dict[int, int]) -> dict[int, int]:
    sorted_items = sorted(values.items(), key=lambda item: item[1])
    ranks = {}
    index = 0
    while index < len(sorted_items):
        tie_end = index
        while tie_end < len(sorted_items) and sorted_items[tie_end][1] == sorted_items[index][1]:
            tie_end += 1

        rank = index + 1
        for person_id, _ in sorted_items[index:tie_end]:
            ranks[person_id] = rank
        index = tie_end

    return ranks


def _average_rank_positions(values: list[tuple[str, int]]) -> dict[str, float]:
    sorted_values = sorted(values, key=lambda item: item[1])
    ranks = {}
    index = 0
    while index < len(sorted_values):
        tie_end = index
        while tie_end < len(sorted_values) and sorted_values[tie_end][1] == sorted_values[index][1]:
            tie_end += 1

        average_rank = (index + 1 + tie_end) / 2
        for person_id, _ in sorted_values[index:tie_end]:
            ranks[person_id] = average_rank
        index = tie_end

    return ranks


def calculate_percentile_correlation(
    results: list[dict[str, object]],
) -> tuple[list[str], list[str], np.ndarray, np.ndarray]:
    deduped = {}
    for row in results:
        person_id = str(row["personId"])
        event_id = str(row["eventId"])
        if event_id in EXCLUDED_EVENTS:
            continue

        deduped.setdefault((person_id, event_id), int(row["worldRank"]))

    by_event = defaultdict(list)
    for (person_id, event_id), world_rank in deduped.items():
        by_event[event_id].append((person_id, world_rank))

    percentile_by_person_event = {}
    for event_id, event_values in by_event.items():
        n = len(event_values)
        average_ranks = _average_rank_positions(event_values)
        for person_id, average_rank in average_ranks.items():
            percentile_by_person_event[(person_id, event_id)] = 100 - average_rank / n * 100

    people = sorted({person_id for person_id, _ in percentile_by_person_event})
    events = sorted(by_event)
    participation = np.zeros((len(people), len(events)))
    person_index = {person_id: index for index, person_id in enumerate(people)}
    event_index = {event_id: index for index, event_id in enumerate(events)}

    for (person_id, event_id), percentile in percentile_by_person_event.items():
        participation[person_index[person_id], event_index[event_id]] = percentile

    corrmat = np.corrcoef(participation, rowvar=False)
    return events, people, corrmat, participation
