import argparse
from pathlib import Path, PurePath
from typing import Union

from hsf_website_helpers.util.repo import is_website_folder
from hsf_website_helpers.util.log import logger


def verified_path(path: Union[str, PurePath]) -> Path:
    path = Path(path)
    if not path.is_dir():
        msg = f"Expected existing directory, got {path}"
        logger.error(msg)
        raise ValueError(msg)
    if not is_website_folder(path):
        msg = (
            f"The directory {path} doesn't look like the hsf.github.io "
            f"repository. You might need to either supply the path to the "
            f"correct directory or change your working directory to there."
        )
        logger.error(msg)
        raise ValueError(msg)
    return path


def add_website_home_option(parser: argparse.ArgumentParser):
    parser.add_argument("--home", type=verified_path, default=str(Path.cwd()))
