#!/usr/bin/env python

import argparse
import os
import sys

from ndspy import findInNamedList, indexInNamedList, setInNamedList
from ndspy.rom import NintendoDSRom
from ndspy.soundArchive import SDAT


# The key in this dictionary is the filename the track has in Phoenix Wright 1,
# the value is the track to be replaced in Phoenix Wright 2
#
# In the comment is roughly the name of the track in Phoenix Wright 1.
MUSIC_MAPPING = {
    "BGM005": "BGM071",  # Logic & Trick
    "BGM008": "BGM077",  # Defendant Lobby
    "BGM013": "BGM069",  # Court
    "BGM010": "BGM072",  # Cross-Examination Moderato
    "BGM011": "BGM073",  # Cross-Examination Allegro
    "BGM004": "BGM070",  # Objection
    "BGM002": "BGM074",  # Pursuit
    "BGM003": "BGM075",  # Pursuit variation
    "BGM016": "BGM080",  # Save prompt
}


def onify(pw1_rom_path: str, pw2_rom_path: str, output_path: str):
    if os.path.exists(output_path):
        raise RuntimeError(
            f"Output file ({output_path}) already exists. Not overwriting."
        )

    try:
        pw1_rom = NintendoDSRom.fromFile(pw1_rom_path)
        pw2_rom = NintendoDSRom.fromFile(pw2_rom_path)
    except OSError as e:
        raise RuntimeError(f"Could not open ROM: {e}")

    pw1_sound_data = pw1_rom.files[pw1_rom.filenames["sound_data.sdat"]]
    pw1_sdat = SDAT(pw1_sound_data)

    pw2_sound_data = pw2_rom.files[pw2_rom.filenames["sound_data.sdat"]]
    pw2_sdat = SDAT(pw2_sound_data)

    copy_sound_files(MUSIC_MAPPING, pw1_sdat, pw2_sdat)

    pw2_rom.files[pw2_rom.filenames["sound_data.sdat"]] = pw2_sdat.save()
    pw2_rom.saveToFile(output_path)

    print(f"Take that! Wrote modified ROM to {output_path}")


def copy_sound_files(mapping: dict, source_sdat: SDAT, destination_sdat: SDAT):
    """Copies the sound files from the source SDAT to the destination SDAT."""

    for from_name, to_name in mapping.items():
        wave = findInNamedList(source_sdat.waveArchives, f"WAVE_{from_name}")
        setInNamedList(destination_sdat.waveArchives, f"WAVE_{to_name}", wave)

        bank = findInNamedList(source_sdat.banks, f"BANK_{from_name}")
        # Point to the correct wave archive positions in the destination ROM
        bank.waveArchiveIDs = findInNamedList(
            destination_sdat.banks, f"BANK_{to_name}"
        ).waveArchiveIDs
        setInNamedList(destination_sdat.banks, f"BANK_{to_name}", bank)

        seq = findInNamedList(source_sdat.sequences, from_name)
        # Point to the correct bank position in the destination ROM
        seq.bankID = indexInNamedList(destination_sdat.banks, f"BANK_{to_name}")
        setInNamedList(destination_sdat.sequences, to_name, seq)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='"Phoenix Wright 2: Justice For All" Onifier',
        description="Improves a Phoenix Wright 2 ROM by copying the better music from a Phoenix Wright 1 ROM. Take that!",
    )
    parser.add_argument("pw1_path", help="Path to Phoenix Wright 1 ROM")
    parser.add_argument("pw2_path", help="Path to Phoenix Wright 2 ROM")
    parser.add_argument(
        "output_path",
        default="PW2-onified.nds",
        help="Where to write the modified Phoenix Wright 2 ROM to",
    )

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    try:
        onify(args.pw1_path, args.pw2_path, args.output_path)
    except RuntimeError as e:
        print("Hold it!", e, file=sys.stderr)
        sys.exit(1)
