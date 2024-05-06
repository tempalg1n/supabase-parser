import logging
from supabase import Client, create_client

from config import config
from dao import Supabase
from sources.source_parser import get_sources, FILE_PATH, CASES_BORDER

logger = logging.getLogger(__name__)


def main():
    supabase_client: Client = create_client(config.supabase.url, config.supabase.key)
    supabase: Supabase = Supabase(supabase_client)
    old_cases, new_cases = get_sources(
        file_path=FILE_PATH,
        cases_border=CASES_BORDER
    )
    old_examinations: list[dict] = supabase.get_cases_examinations(old_cases)
    new_examinations: list[dict] = supabase.get_cases_examinations(new_cases)


if __name__ == '__main__':
    main()
