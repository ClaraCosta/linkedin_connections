from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RunStats:
    clicked: int = 0
    skipped: int = 0
    scrolls_without_click: int = 0


@dataclass
class PersonInfo:
    name: str
    description: str
    profile_url: str
