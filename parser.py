import logging
from supabase import Client, create_client

from config import config
from dao import Supabase

logger = logging.getLogger(__name__)


def main():
    supabase_client: Client = create_client(config.supabase.url, config.supabase.key)
    supabase: Supabase = Supabase(supabase_client)
