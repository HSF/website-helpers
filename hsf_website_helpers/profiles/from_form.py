from typing import Iterable

import pandas as pd

from hsf_website_helpers.profiles.profile import Profile


header_mapping = {
    "Your name": "title",
    "Years active in training": "training_years",
    "Training roles you have already taken": "training_roles",
    "gravatar": "gravatar",
    "github": "github",
    "gitlab": "gitlab",
    "bitbucket": "bitbucket",
    "homepage": "homepage",
    "twitter": "twitter",
    "orcid": "orcid",
    "linkedin": "linkedin",
    "email": "email",
    "Write about yourself": "content",
}

available_roles = ["mentor", "instructor", "facilitator"]


def profiles_from_google_form(df: pd.DataFrame) -> Iterable[Profile]:
    """Yields profiles from rows of a dataframe (usually the dataframe that is
    loaded from the google spreadsheet results of a google form)
    """
    df = df.astype("str")
    df = df.rename(columns=header_mapping)
    for row in df.iterrows():
        p = Profile()
        for k in header_mapping.values():
            value = row[1][k].replace("nan", "")
            if k == "content":
                p.content = value
            elif k == "training_years":
                p.header["training_years"] = sorted(map(int, value.split(",")))
            elif k == "training_roles":
                p.header["training_roles"] = [
                    role for role in available_roles if role in value.lower()
                ]
            else:
                if value == "":
                    value = None
                p.header[k] = value
        p.header["layout"] = "educator"
        yield p
