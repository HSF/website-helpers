from pathlib import Path
from typing import List
import copy

from hsf_website_helpers.profiles.profile import Profile
from hsf_website_helpers.util.log import logger


def merge_profiles(profiles: List[Profile]) -> List[Profile]:
    merged_profiles: List[Profile] = []
    for profile in profiles:
        results = [p for p in merged_profiles if p.same_person(profile)]
        if not results:
            if not profile.path:
                logger.debug(f"{profile.header['title']} is new")
            merged_profiles.append(copy.deepcopy(profile))
        elif len(results) == 1:
            logger.debug(f"{profile.header['title']} already had a profile")
            results[0].update(profile)
        else:
            raise ValueError("More than one profile matches")
    return merged_profiles


def write_merged_profiles(profiles: List[Profile], basepath: Path) -> None:
    for profile in profiles:
        if not profile.path:
            profile.path = profile.get_new_path(basepath=basepath)
        profile.to_file()
