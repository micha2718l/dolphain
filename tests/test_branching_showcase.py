#!/usr/bin/env python3
"""Tests for the branching showcase helper utilities."""

from __future__ import annotations

from pathlib import Path
import sys

import pytest  # type: ignore

# Ensure local imports resolve when tests are executed directly
sys.path.insert(0, str(Path(__file__).parent.parent))

import dolphain


def _make_record(rank: int, wpm: float, freq_range: float, coverage: float) -> dict:
    return {
        "rank": rank,
        "filename": f"sample_{rank:02d}.200",
        "audio_raw": f"audio/sample_{rank:02d}_raw.mp3",
        "audio_denoised": f"audio/sample_{rank:02d}_denoised.mp3",
        "spectrogram": f"images/sample_{rank:02d}_spectrogram.png",
        "waveform": f"images/sample_{rank:02d}_waveform.png",
        "stats": {
            "whistles_per_minute": wpm,
            "coverage": coverage,
            "freq_range_khz": freq_range,
            "whistle_count": int(wpm / 2),
            "duration": 21.33,
        },
        "metadata": {
            "time_start": "2017-07-01 00:00:00",
            "duration": 21.33,
        },
        "score": int(wpm),
    }


def test_bucket_classification_boundaries():
    assert dolphain.categorize_energy(180).name == "Hyperspeed Superpod"
    assert dolphain.categorize_energy(150).name == "Chorus Cascade"
    assert dolphain.categorize_energy(125).name == "Lively Drift"
    assert dolphain.categorize_energy(80).name == "Moonlight Echo"

    assert dolphain.categorize_frequency_span(1.2).name == "Tight Harmonics"
    assert dolphain.categorize_frequency_span(1.5).name == "Dynamic Duets"
    assert dolphain.categorize_frequency_span(2.0).name == "Wild Improvisations"

    assert dolphain.categorize_coverage(97).name == "Wall-to-Wall Whistles"
    assert dolphain.categorize_coverage(90).name == "Rolling Conversations"
    assert dolphain.categorize_coverage(70).name == "Open Water Echoes"


def test_build_branch_tree_structure():
    records = [
        _make_record(1, wpm=175, freq_range=1.3, coverage=96),
        _make_record(2, wpm=160, freq_range=1.6, coverage=92),
        _make_record(3, wpm=100, freq_range=1.9, coverage=80),
    ]

    tree = dolphain.build_branch_tree(records)

    assert tree["type"] == "root"
    assert tree["name"] == "Dolphin Branch Explorer"
    assert tree["meta"]["count"] == 3

    # Ensure we created at least two distinct energy branches
    energy_names = {child["name"] for child in tree["children"]}
    assert any("Hyperspeed Superpod" in name for name in energy_names)
    assert any("Moonlight Echo" in name for name in energy_names)

    # Ensure leaves include audio metadata and stats
    leaf = None
    for energy_branch in tree["children"]:
        for freq_branch in energy_branch["children"]:
            for coverage_branch in freq_branch["children"]:
                if coverage_branch["children"]:
                    leaf = coverage_branch["children"][0]
                    break
            if leaf:
                break
        if leaf:
            break

    assert leaf is not None
    assert leaf["type"] == "record"
    assert leaf["media"]["audio_raw"].endswith(".mp3")
    assert leaf["stats"]["whistles_per_minute"] is not None


@pytest.mark.parametrize(
    "wpm,expected",
    [
        (200, "Hyperspeed Superpod"),
        (145, "Chorus Cascade"),
        (135, "Lively Drift"),
        (0, "Moonlight Echo"),
    ],
)
def test_energy_bucket_parametrized(wpm, expected):
    assert dolphain.categorize_energy(wpm).name == expected
