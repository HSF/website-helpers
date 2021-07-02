# std
from typing import Optional, Dict, Any
from pathlib import Path

# 3rd
import oyaml as yaml  # same as normal yaml, only it keeps order of keys

from hsf_website_helpers.util.log import logger


class Profile:
    match_keys = [
        "title",
        "github",
        "gravatar",
        "twitter",
        "gitlab",
        "bitbucket",
        "orcide",
        "linkedin",
        "email",
    ]

    merge_update = ["training_roles", "training_years"]

    easy_update = [
        "country",
        "github",
        "homepage",
        "gravatar",
        "twitter",
        "gitlab",
        "bitbucket",
        "orcide",
        "linkedin",
        "email",
    ]

    def __init__(self):
        #: The path from which we loaded this data (if we loaded form a file)
        self.path: Optional[Path] = None
        #: The "about me" content, i.e. the content of the profile page
        self.content = ""
        #: The yaml frontmatter / key value pairs of the profile
        self.header: Dict[str, Any] = {}

    def check(self):
        """Sanity checks of the data"""
        assert self.header.get("title", "") != ""

    def get_new_path(self, basepath: Optional[Path]) -> Path:
        """Format path based on title"""
        if self.header.get("title", "") == "":
            raise ValueError("Couldn't get title.")
        title = self.header["title"]
        # Remove (she/her) things
        title = title.split("(")[0]
        title = title.lower().strip()
        title = title.replace(" ", "_")
        title += ".md"
        if basepath is None:
            basepath = Path.cwd()
        return basepath / title

    @classmethod
    def from_file(cls, path: Path) -> "Profile":
        """Load Profile from markdown file"""
        logger.debug(f"Reading {path}")
        lines = path.read_text(encoding="utf-8").split("\n")
        header_lines = []
        content_lines = []
        is_content = False
        for i_line, line in enumerate(lines):
            line = line.strip()
            if i_line == 0:
                assert line == "---", lines
                continue
            if line == "---":
                is_content = True
                continue
            if is_content:
                content_lines.append(line)
            else:
                header_lines.append(line)
        p = cls()
        p.header = yaml.safe_load("\n".join(header_lines))
        p.content = "\n".join(content_lines)
        p.path = path
        p.check()
        return p

    def same_person(self, other: "Profile") -> bool:
        """Determine if the other profile corresponds to the same person"""
        if (
            self.path is not None
            and other.path is not None
            and self.path.name == other.path.name != ""
        ):
            return True
        for key in self.match_keys:
            value = self.header.get(key, "")
            if value and value == other.header.get(key, ""):
                return True
        return False

    def to_file(self, path: Optional[Path] = None) -> Path:
        """Write profile to Jekyll style markdown file"""
        if path is None:
            if self.path:
                path = self.path
            else:
                raise ValueError("Either supply path as argument or attribute.")
        new_file_content = "---\n"
        new_file_content += yaml.dump(self.header)
        new_file_content += "---\n"
        new_file_content += self.content
        path.write_text(new_file_content)
        return path

    def update(self, newer: "Profile"):
        """Update this profile with data from a newer profile of the same
        person.
        """
        for key in self.merge_update:
            self.header[key] = sorted(
                set(self.header.get(key, []) + newer.header.get(key, []))
            )
        for key in self.easy_update:
            value = newer.header.get(key, "")
            if value is None or value.strip() != "":
                self.header[key] = newer.header.get(key, None)
