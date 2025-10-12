#!/usr/bin/env python3
"""
Convert WAV files to MP3 for web delivery.
Reduces file sizes by ~10x for faster loading.
"""

import subprocess
from pathlib import Path
import json
import argparse


def convert_to_mp3(wav_path, mp3_path, bitrate="128k"):
    """Convert WAV to MP3 using ffmpeg."""
    try:
        subprocess.run(
            [
                "ffmpeg",
                "-i",
                str(wav_path),
                "-codec:a",
                "libmp3lame",
                "-b:a",
                bitrate,
                "-y",  # Overwrite output file
                str(mp3_path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error converting {wav_path.name}: {e.stderr}")
        return False
    except FileNotFoundError:
        print("❌ ffmpeg not found. Install with: brew install ffmpeg")
        return False


def main():
    parser = argparse.ArgumentParser(description="Convert showcase WAV files to MP3")
    parser.add_argument(
        "--showcase-dir", default="site/showcase", help="Showcase directory"
    )
    parser.add_argument("--bitrate", default="128k", help="MP3 bitrate (default: 128k)")

    args = parser.parse_args()

    showcase_dir = Path(args.showcase_dir)
    audio_dir = showcase_dir / "audio"

    if not audio_dir.exists():
        print(f"❌ Audio directory not found: {audio_dir}")
        return

    # Get all WAV files
    wav_files = sorted(audio_dir.glob("*.wav"))

    if not wav_files:
        print(f"❌ No WAV files found in {audio_dir}")
        return

    print(f"🎵 Found {len(wav_files)} WAV files")
    print(f"🔄 Converting to MP3 at {args.bitrate}...\n")

    converted = 0
    total_wav_size = 0
    total_mp3_size = 0

    for wav_file in wav_files:
        mp3_file = wav_file.with_suffix(".mp3")

        wav_size = wav_file.stat().st_size
        total_wav_size += wav_size

        print(f"Converting: {wav_file.name}... ", end="", flush=True)

        if convert_to_mp3(wav_file, mp3_file, args.bitrate):
            mp3_size = mp3_file.stat().st_size
            total_mp3_size += mp3_size

            compression = ((wav_size - mp3_size) / wav_size) * 100
            print(
                f"✅ {wav_size // 1024 // 1024}MB → {mp3_size // 1024 // 1024}MB ({compression:.0f}% smaller)"
            )
            converted += 1
        else:
            print("❌ Failed")

    # Update showcase_data.json to reference MP3 files
    data_file = showcase_dir / "showcase_data.json"
    if data_file.exists():
        print(f"\n📝 Updating {data_file}...")
        with open(data_file, "r") as f:
            data = json.load(f)

        for file_info in data["files"]:
            # Change .wav to .mp3
            file_info["audio_raw"] = file_info["audio_raw"].replace(".wav", ".mp3")
            file_info["audio_denoised"] = file_info["audio_denoised"].replace(
                ".wav", ".mp3"
            )

        with open(data_file, "w") as f:
            json.dump(data, f, indent=2)

        print("✅ Updated showcase_data.json")

    print(f"\n{'='*60}")
    print(f"✅ Converted {converted}/{len(wav_files)} files")
    print(f"💾 Total WAV size: {total_wav_size // 1024 // 1024} MB")
    print(f"💾 Total MP3 size: {total_mp3_size // 1024 // 1024} MB")
    print(
        f"🎉 Saved {(total_wav_size - total_mp3_size) // 1024 // 1024} MB ({((total_wav_size - total_mp3_size) / total_wav_size * 100):.0f}% reduction)"
    )
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
