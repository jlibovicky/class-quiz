#!/usr/bin/env python3
"""Generate new one-time attendance keys and append them to the key file.

The same can be done from the teacher interface at <root>/attendance_keys,
which also prints the slips and invalidates keys.
"""

import argparse
import datetime

from attendance import KeyStore


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "count", type=int, help="How many keys to generate.")
    parser.add_argument(
        "--batch", default=None,
        help="Name of the batch, by default the current date and time.")
    parser.add_argument(
        "--keys-file", default="attendance_keys.txt",
        help="File with the one-time attendance keys.")
    args = parser.parse_args()

    batch = args.batch or datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    key_store = KeyStore(args.keys_file)
    new_entries = key_store.generate(args.count, batch)

    print(f"Added {len(new_entries)} keys in batch '{batch}' to "
          f"{args.keys_file} ({len(key_store.entries)} valid in total).")


if __name__ == "__main__":
    main()
