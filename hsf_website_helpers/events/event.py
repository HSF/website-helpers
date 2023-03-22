import datetime
from pathlib import Path
from typing import List, Optional, Union

import yaml

from hsf_website_helpers.util.log import logger


class Event:
    default_false = ["url_proof_ignore"]
    hsf_tag = "HSF"
    known_tags = {hsf_tag}

    def __init__(
        self,
        title: str,
        date: Union[str, datetime.date],
        end_date: Union[str, datetime.date],
        source: str,
        author: str,
        deadline: Union[str, datetime.date] = "",
        url_proof_ignore=False,
        tags=None,
    ):
        self.title = title
        self.date = self._interpret_date(date)
        self.end_date = self._interpret_date(end_date)
        self.deadline = self._interpret_date(deadline, empty_ok=True)
        self.source = source
        self.author = author
        self.url_proof_ignore = url_proof_ignore
        if tags is None:
            tags = []
        unknown_tags = set(tags) - self.known_tags
        if unknown_tags:
            logger.warning(f"Unknown tags: {unknown_tags}")
        self.tags = tags

        if not self.end_date >= self.date:
            raise ValueError(
                f"End date {self.end_date} is BEFORE the date {self.date} for "
                f"training event '{self.title}'."
            )
        if self.deadline:
            if not self.deadline <= self.date:
                raise ValueError(
                    f"Deadline {self.deadline} is after start date {self.date}"
                    f" for training event '{self.title}'."
                )
        assert self.title

    @staticmethod
    def _interpret_date(date: Union[datetime.date, str], empty_ok=False):
        if not date and empty_ok:
            return date
        elif isinstance(date, datetime.date):
            return date
        else:
            return datetime.datetime.strptime(date, "%Y-%m-%d").date()

    @classmethod
    def input(cls):
        tmp_event = Event(
            title=input("Event title ").strip(),
            date=input("Start date [YYYY-MM-DD] ").strip(),
            end_date=input("End date [YYYY-MM-DD] ").strip(),
            deadline=input("Deadline [YYYY-MM-DD or ''] ").strip(),
            source=input("Url ").strip(),
            author=input("Author ").strip(),
            tags=[
                t.strip()
                for t in input("Tags (comma separated)").split(",")
                if t.strip()
            ],
        )
        if cls.hsf_tag in tmp_event.tags:
            logger.warning(
                "Please make sure to also add the event to the IRIS-HEP "
                "website."
            )
        return tmp_event

    def to_dict(self):
        dct = self.__dict__.copy()
        for key in self.default_false:
            if not dct[key]:
                dct.pop(key)
        return dct


class EventDatabase:
    def __init__(self, events: Optional[List[Event]] = None):
        if events is not None:
            self.events = events
        else:
            self.events = []
        #: These lines get written to the top of the data file, e.g. comments
        #: for usage.
        self.prologue_lines = [
            "# Sorted by ascending date => New events go on top",
            "# You can use the scripts from https://github.com/HSF/website-helpers/",
            "# to update or reformat this file interactively.",
        ]

    @classmethod
    def from_file(cls, path: Path):
        with path.open() as stream:
            event_dict = yaml.safe_load(stream)
            if event_dict is None:
                return EventDatabase()
            else:
                return EventDatabase([Event(**dct) for dct in event_dict])

    def write(self, path: Path):
        def sort_key(event: Event):
            return event.date

        with path.open("w") as stream:
            stream.writelines("\n".join(self.prologue_lines) + "\n")
            yaml.dump(
                [
                    event.to_dict()
                    for event in sorted(self.events, key=sort_key, reverse=True)
                ],
                stream,
                default_flow_style=False,
            )

    def add_event(self, event: Event):
        self.events.append(event)
