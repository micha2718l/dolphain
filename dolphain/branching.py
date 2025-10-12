"""Branching showcase utilities for dolphain.

This module generates a multi-level tree structure that groups showcase
recordings into an adventure-style branching experience.  The goal is to
provide a playful exploration path for hackathon demos and interactive
storytelling experiences.
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Any, Dict, Iterable, List, Optional

Number = Optional[float]


@dataclass(frozen=True)
class BranchBucket:
    """Represents a qualitative grouping for a metric."""

    name: str
    description: str
    emoji: str
    min_value: float
    max_value: float

    def matches(self, value: Number) -> bool:
        if value is None:
            return False
        return self.min_value <= value < self.max_value


ENERGY_BUCKETS: List[BranchBucket] = [
    BranchBucket(
        name="Hyperspeed Superpod",
        description="170+ whistles/min • maximum chaos and coordinated buzz",
        emoji="🚀",
        min_value=170.0,
        max_value=float("inf"),
    ),
    BranchBucket(
        name="Chorus Cascade",
        description="140-169 whistles/min • packed chatter and rising energy",
        emoji="🎶",
        min_value=140.0,
        max_value=170.0,
    ),
    BranchBucket(
        name="Lively Drift",
        description="110-139 whistles/min • balanced back-and-forth",
        emoji="🌊",
        min_value=110.0,
        max_value=140.0,
    ),
    BranchBucket(
        name="Moonlight Echo",
        description="<110 whistles/min • spacious, lingering calls",
        emoji="🌙",
        min_value=float("-inf"),
        max_value=110.0,
    ),
]

FREQ_BUCKETS: List[BranchBucket] = [
    BranchBucket(
        name="Tight Harmonics",
        description="range < 1.4 kHz • laser-focused melodies",
        emoji="🎯",
        min_value=float("-inf"),
        max_value=1.4,
    ),
    BranchBucket(
        name="Dynamic Duets",
        description="1.4-1.7 kHz • agile twists and conversational play",
        emoji="🌀",
        min_value=1.4,
        max_value=1.7,
    ),
    BranchBucket(
        name="Wild Improvisations",
        description=">= 1.7 kHz • soaring leaps and adventurous riffs",
        emoji="🎢",
        min_value=1.7,
        max_value=float("inf"),
    ),
]

COVERAGE_BUCKETS: List[BranchBucket] = [
    BranchBucket(
        name="Wall-to-Wall Whistles",
        description=">= 95% coverage • relentless sonic waterfall",
        emoji="🌊",
        min_value=95.0,
        max_value=float("inf"),
    ),
    BranchBucket(
        name="Rolling Conversations",
        description="85-94% coverage • rhythmic cadences",
        emoji="🔄",
        min_value=85.0,
        max_value=95.0,
    ),
    BranchBucket(
        name="Open Water Echoes",
        description="< 85% coverage • intentional pauses",
        emoji="💧",
        min_value=float("-inf"),
        max_value=85.0,
    ),
]


def _first_matching_bucket(value: Number, buckets: Iterable[BranchBucket]) -> BranchBucket:
    for bucket in buckets:
        if bucket.matches(value):
            return bucket
    raise ValueError(f"Unable to categorize value {value} into provided buckets")


def categorize_energy(whistles_per_minute: Number) -> BranchBucket:
    """Return the energy bucket for a whistles-per-minute score."""

    return _first_matching_bucket(whistles_per_minute, ENERGY_BUCKETS)


def categorize_frequency_span(freq_range_khz: Number) -> BranchBucket:
    """Return the frequency-range bucket for a clip."""

    return _first_matching_bucket(freq_range_khz, FREQ_BUCKETS)


def categorize_coverage(coverage_percent: Number) -> BranchBucket:
    """Return the coverage bucket for a clip."""

    return _first_matching_bucket(coverage_percent, COVERAGE_BUCKETS)


def _safe_mean(values: Iterable[Number]) -> Number:
    values_list = [v for v in values if v is not None]
    if not values_list:
        return None
    return mean(values_list)


def _summary_for_records(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    stats = [r.get("stats", {}) for r in records]

    def _extract(key: str) -> List[Number]:
        return [s.get(key) for s in stats]

    return {
        "count": len(records),
        "avg_whistles_per_minute": _round(_safe_mean(_extract("whistles_per_minute")), 1),
        "avg_coverage_percent": _round(_safe_mean(_extract("coverage")), 1),
        "avg_freq_span_khz": _round(_safe_mean(_extract("freq_range_khz")), 2),
        "avg_whistle_count": _round(_safe_mean(_extract("whistle_count")), 1),
    }


def _round(value: Number, decimals: int) -> Optional[float]:
    if value is None:
        return None
    return round(value, decimals)


def _build_leaf(record: Dict[str, Any]) -> Dict[str, Any]:
    stats = record.get("stats", {})
    metadata = record.get("metadata", {})

    audio_raw = record.get("audio_raw")
    audio_denoised = record.get("audio_denoised")

    return {
        "type": "record",
        "name": f"Rank {record.get('rank')} • {record.get('filename')}",
        "description": f"{stats.get('whistles_per_minute')} whistles/min, {stats.get('coverage')}% coverage",
        "stats": {
            "whistles_per_minute": stats.get("whistles_per_minute"),
            "coverage": stats.get("coverage"),
            "freq_range_khz": stats.get("freq_range_khz"),
            "whistle_count": stats.get("whistle_count"),
            "duration_s": stats.get("duration"),
        },
        "media": {
            "audio_raw": f"../showcase/{audio_raw}" if audio_raw else None,
            "audio_denoised": f"../showcase/{audio_denoised}" if audio_denoised else None,
            "spectrogram": f"../showcase/{record.get('spectrogram')}"
            if record.get("spectrogram")
            else None,
            "waveform": f"../showcase/{record.get('waveform')}"
            if record.get("waveform")
            else None,
        },
        "metadata": {
            "score": record.get("score"),
            "time_start": metadata.get("time_start"),
            "duration": metadata.get("duration"),
            "original_path": record.get("original_path"),
        },
    }


def build_branch_tree(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a hierarchical branching structure from showcase records."""

    root_children: Dict[str, Dict[str, Dict[str, List[Dict[str, Any]]]]] = {}

    for record in records:
        stats = record.get("stats", {})
        energy_bucket = categorize_energy(stats.get("whistles_per_minute"))
        freq_bucket = categorize_frequency_span(stats.get("freq_range_khz"))
        coverage_bucket = categorize_coverage(stats.get("coverage"))

        leaf = _build_leaf(record)

        energy_dict = root_children.setdefault(energy_bucket.name, {})
        freq_dict = energy_dict.setdefault(freq_bucket.name, {})
        coverage_list = freq_dict.setdefault(coverage_bucket.name, [])
        coverage_list.append(leaf)

    def _bucket_meta(bucket: BranchBucket) -> Dict[str, Any]:
        return {
            "label": bucket.name,
            "emoji": bucket.emoji,
            "description": bucket.description,
        }

    root: Dict[str, Any] = {
        "type": "root",
        "name": "Dolphin Branch Explorer",
        "description": "Choose a branch to follow pods by energy, harmony, and flow.",
        "meta": _summary_for_records(records),
        "children": [],
    }

    for energy_bucket in ENERGY_BUCKETS:
        energy_records_nested = root_children.get(energy_bucket.name)
        if not energy_records_nested:
            continue

        energy_children = []
        energy_records_flat: List[Dict[str, Any]] = []

        for freq_bucket in FREQ_BUCKETS:
            freq_records_nested = energy_records_nested.get(freq_bucket.name)
            if not freq_records_nested:
                continue

            freq_children = []
            freq_records_flat: List[Dict[str, Any]] = []

            for coverage_bucket in COVERAGE_BUCKETS:
                coverage_records = freq_records_nested.get(coverage_bucket.name)
                if not coverage_records:
                    continue

                freq_records_flat.extend(coverage_records)

                freq_children.append(
                    {
                        "type": "coverage",
                        "name": f"{coverage_bucket.emoji} {coverage_bucket.name}",
                        "meta": {
                            **_bucket_meta(coverage_bucket),
                            **_summary_for_records(coverage_records),
                        },
                        "children": coverage_records,
                    }
                )

            if not freq_children:
                continue

            energy_records_flat.extend(freq_records_flat)

            freq_children.sort(key=lambda node: node["meta"].get("avg_whistles_per_minute") or 0, reverse=True)

            energy_children.append(
                {
                    "type": "frequency",
                    "name": f"{freq_bucket.emoji} {freq_bucket.name}",
                    "meta": {
                        **_bucket_meta(freq_bucket),
                        **_summary_for_records(freq_records_flat),
                    },
                    "children": freq_children,
                }
            )

        if not energy_children:
            continue

        energy_children.sort(key=lambda node: node["meta"].get("avg_freq_span_khz") or 0, reverse=True)

        root["children"].append(
            {
                "type": "energy",
                "name": f"{energy_bucket.emoji} {energy_bucket.name}",
                "meta": {
                    **_bucket_meta(energy_bucket),
                    **_summary_for_records(energy_records_flat),
                },
                "children": energy_children,
            }
        )

    root["children"].sort(
        key=lambda node: node["meta"].get("avg_whistles_per_minute") or 0,
        reverse=True,
    )

    return root


__all__ = [
    "BranchBucket",
    "build_branch_tree",
    "categorize_energy",
    "categorize_frequency_span",
    "categorize_coverage",
]
