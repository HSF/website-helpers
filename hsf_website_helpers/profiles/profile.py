# std
from typing import Optional, Dict, Any
from pathlib import Path

# 3rd
import oyaml as yaml  # same as normal yaml, only it keeps order of keys


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
        self.path: Optional[Path] = None
        self.content = ""
        self.header: Dict[str, Any] = {}

    def check(self):
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
        lines = path.read_text().split("\n")
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
            if "" != self.header.get(key, "") == other.header.get(key, ""):
                return True
        return False

    def to_file(self, path: Path) -> None:
        new_file_content = "---\n"
        new_file_content += yaml.dump(self.header)
        new_file_content += "---\n"
        new_file_content += self.content
        path.write_text(new_file_content)

    def update(self, newer: "Profile"):
        for key in self.merge_update:
            self.header[key] = sorted(
                set(self.header.get(key, []) + newer.header.get(key, []))
            )
        for key in self.easy_update:
            if newer.header.get(key, "").strip() != "":
                self.header[key] = newer.header[key]