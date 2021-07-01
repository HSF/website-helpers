from pathlib import Path


def is_website_folder(path: Path):
    """Checks if path likely points at the hsf.github.io repository"""
    existing_subfolders = [".git", "_profiles", "_data"]
    for es in existing_subfolders:
        if not (path / es).is_dir():
            print(path, es)
            return False
    return True
