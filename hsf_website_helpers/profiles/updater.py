from pathlib import Path
from typing import List
import copy

from hsf_website_helpers.profiles.profile import Profile


def merge_profiles(profiles: List[Profile]) -> List[Profile]:
    merged_profiles: List[Profile] = []
    for profile in profiles:
        # check if we need to merge
        results = [p for p in merged_profiles if p.same_person(profile)]
        if not results:
            merged_profiles.append(copy.deepcopy(profile))
        elif len(results) == 1:
            results[0].update(profile)
        else:
            raise ValueError("More than one profile matches")
    return merged_profiles


def write_merged_profiles(profiles: List[Profile], basepath: Path) -> None:
    for profile in profiles:
        if not profile.path:
            profile.path = profile.get_new_path(basepath=basepath)
        profile.to_file()
