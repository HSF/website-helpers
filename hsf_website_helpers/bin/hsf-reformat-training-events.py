#!/usr/bin/env python3

"""
Quick script to read all training schools from data file and write them out
again to e.g. update the formatting.
"""

import argparse

from hsf_website_helpers.events.event import EventDatabase
from hsf_website_helpers.util.cli import add_website_home_option


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__file__.__doc__)
    add_website_home_option(parser)
    args = parser.parse_args()
    path = args.home / "_data" / "training-schools.yml"
    if path.is_file():
        edb = EventDatabase.from_file(path)
        print(f"Loaded {len(edb.events)} events from database.")
    else:
        print(f"Did not find database at {path}. Initializing empty one.")
        edb = EventDatabase()
    edb.write(path)
    print(
        "Reformated database. Please commit and submit a PR to add it to "
        "the webpage."
    )
