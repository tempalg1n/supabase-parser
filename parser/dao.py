from postgrest import APIResponse

from config import config, Bucket
from supabase import Client
from random import choice


class Supabase:
    """
    Data access object for storages.
    """

    def __init__(
            self,
            client: Client,
            bucket: Bucket = Bucket.JPG
    ):
        self.client: Client = client
        self.bucket: Bucket = bucket

    def get_cases_examinations(self, cases_ids: list[str]) -> list[dict]:
        response: APIResponse = self.client.table('casesExaminations').select('examinationId').in_('caseId', cases_ids).execute()
        return response.data

    def get_examination_random_image(self, examination_id: str) -> str:
        response: APIResponse = self.client.table('images').select('source').is_('examinationId', examination_id).execute()
        return choice(response.data)
