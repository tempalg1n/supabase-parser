import hashlib
from postgrest import APIResponse
from storage3.utils import StorageException

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

    def get_case_examinations(self, case_id: str) -> list[dict[str, str]]:
        response: APIResponse = self.client.table('casesExaminations').select('examinationId').eq('caseId', case_id).execute()
        return response.data

    def get_case_random_examination(self, case_id: str) -> dict[str, str]:
        try:
            response: APIResponse = self.client.table('casesExaminations').select('examinationId').eq('caseId', case_id).execute()
            return choice(response.data)
        except IndexError:
            print(f'No examinations in case {case_id}')

    def get_examination_random_image(self, examination_id: str) -> dict[str, str]:
        try:
            response: APIResponse = self.client.table('images').select('source').eq('examinationId', examination_id).execute()
            return choice(response.data)
        except IndexError:
            print(f'No images in examination {examination_id}')

    def get_all_exam_images(self, examination_id: str) -> list[dict[str, str]]:
        response: APIResponse = self.client.table('images').select('source').eq('examinationId', examination_id).execute()
        return response.data

    def get_image_hash(self, source: str):
        try:
            image_bytes: bytes = self.client.storage.from_(self.bucket).download(f'/{source}')
            str_hash: str = hashlib.md5(image_bytes).hexdigest()
            return str_hash
        except StorageException as e:
            print(f"Can't find source: {e}")