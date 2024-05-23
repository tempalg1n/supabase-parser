import logging
from supabase import Client, create_client
from tqdm import tqdm

from config import config
from dao import Supabase
from parser.dto import Case, Image, Examination
from sources.source_parser import get_sources, FILE_PATH, CASES_BORDER

logger = logging.getLogger(__name__)


def main():
    supabase_client: Client = create_client(config.supabase.url, config.supabase.key)
    supabase: Supabase = Supabase(supabase_client)
    old_cases, new_cases = get_sources(
        file_path=FILE_PATH,
        cases_border=CASES_BORDER
    )
    old_cases_dto: list[Case] = []
    with tqdm(total=len(old_cases)) as progress_bar:
        progress_bar.set_description("Getting info about old cases")
        for old_case in old_cases:
            old_case_examination: dict[str, str] = supabase.get_case_random_examination(old_case)
            if old_case_examination:
                random_image: dict[str, str] = supabase.get_examination_random_image(old_case_examination['examinationId'])
                if random_image:
                    image_hash: str = supabase.get_image_hash(random_image['source'])
                    image: Image = Image(source=random_image['source'], hash=image_hash)
                    exam: Examination = Examination(id=old_case_examination['examinationId'], images=[image])
                else:
                    exam: Examination = Examination(id=old_case_examination['examinationId'])
                old_cases_dto.append(Case(id=old_case, type='old', examinations=[exam]))
            else:
                old_cases_dto.append(Case(id=old_case, type='old'))
            progress_bar.update()

    new_cases_dto: list[Case] = []
    with tqdm(total=len(new_cases)) as progress_bar:
        progress_bar.set_description("Getting info about new cases")
        for new_case in new_cases:
            new_case_examinations: list[dict] = supabase.get_case_examinations(new_case)
            if new_case_examinations:
                case_exams_dto: list[Examination] = []
                for new_case_exam in new_case_examinations:
                    exam_images: list[dict[str, str]] = supabase.get_all_exam_images(new_case_exam['examinationId'])
                    if exam_images:
                        images: list[Image] = []
                        for img in exam_images:
                            image_hash: str = supabase.get_image_hash(img['source'])
                            image: Image = Image(source=img['source'], hash=image_hash)
                            images.append(image)
                        exam: Examination = Examination(id=new_case_exam['examinationId'], images=images)
                    else:
                        exam: Examination = Examination(id=new_case_exam['examinationId'])
                    case_exams_dto.append(exam)
                new_cases_dto.append(Case(id=new_case, type='new', examinations=case_exams_dto))
            else:
                new_cases_dto.append(Case(id=new_case, type='new'))
            progress_bar.update()

    for new_case in new_cases_dto:
        for old_case in old_cases_dto:
            if new_case.examinations:
                for examination in new_case.examinations:
                    if examination.images:
                        for image in examination.images:
                            if old_case.examinations:
                                for old_exam in old_case.examinations:
                                    if old_exam.images:
                                        if image.hash and old_exam.images[0].hash:
                                            if image.hash == old_exam.images[0].hash:
                                                print(f'Same case found: {new_case.id} is {old_case.id}')

    # new_examinations: list[dict] = supabase.get_case_examinations(new_cases)


if __name__ == '__main__':
    main()
