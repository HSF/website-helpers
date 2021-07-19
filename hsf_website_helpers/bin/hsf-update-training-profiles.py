#!/usr/bin/env python3

"""Reading from a csv dump of a google spreadsheet of google form answers,
update all profiles accordingly.
New profiles will also be added.
"""

from pathlib import Path
import argparse
import pandas as pd

from hsf_website_helpers.profiles.profile import Profile
from hsf_website_helpers.profiles.updater import (
    merge_profiles,
    write_profiles,
)
from hsf_website_helpers.profiles.from_form import profiles_from_google_form
from hsf_website_helpers.util.cli import add_website_home_option
from hsf_website_helpers.util.log import logger


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__file__.__doc__)
    parser.add_argument("--csv", type=Path, required=True)
    add_website_home_option(parser)
    args = parser.parse_args()
    data_dir = args.home / "_profiles"
    logger.info(f"Reading profiles from {data_dir}")

    # We first load all already existing profiles, then all profiles from the
    # google spreadsheet and then merge them iteratively until we only have
    # one profile per person.

    profiles = [
        Profile.from_file(p)
        for p in data_dir.iterdir()
        if p.name not in ["000_template.md", "readme.md"]
        and not p.name.startswith(".")
    ]
    logger.debug(f"Reading csv from {args.csv}")
    df = pd.read_csv(args.csv)
    new_profiles = list(profiles_from_google_form(df))
    write_profiles(merge_profiles(new_profiles + profiles), basepath=data_dir)
