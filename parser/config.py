from dataclasses import dataclass, field
from enum import StrEnum
from environs import Env


class Bucket(StrEnum):
    JPG = "jpg"
    STATIC = "static"
    CERTIFICATES = "certificates"
    HISTOLOGY = "histology"


@dataclass
class SupabaseConfig:
    url: str
    key: str
    bucket: Bucket = Bucket


@dataclass
class Config:
    supabase: SupabaseConfig
    tables: list[str] = field(default_factory=lambda: [
        'cases', 'casesAnswers', 'examinations', 'images', 'casesExaminations'
    ])


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        supabase=SupabaseConfig(
            url=env.str("SUPABASE_URL"),
            key=env.str("SUPABASE_KEY")
        ),
    )


config: Config = load_config()
