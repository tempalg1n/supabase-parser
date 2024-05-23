from dataclasses import dataclass


@dataclass
class Image:
    id: str
    source: str


@dataclass
class Examination:
    id: str
    images: list[Image]


@dataclass
class Case:
    id: str
    examinations: list[Examination]
