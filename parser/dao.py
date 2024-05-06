from postgrest import APIResponse

from config import config, Bucket
from supabase import Client


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

    def get_images(self, examination_ids: list[str]):
        pass
