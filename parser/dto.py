from dataclasses import dataclass
from typing import Literal


@dataclass
class Image:
    source: str
    hash: str = None


@dataclass
class Examination:
    id: str
    images: list[Image] = None


@dataclass
class Case:
    id: str
    type: Literal['old', 'new']
    examinations: list[Examination] = None
