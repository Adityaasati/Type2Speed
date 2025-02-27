import csv
from django.core.management.base import BaseCommand
from typing_app.models import ExamContent, ExamType

class Command(BaseCommand):
    help = "Import passages from passages.csv into the database"

    def handle(self, *args, **kwargs):
        file_path = "passages.csv"  # Ensure file is in project root or provide full path

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            passages_to_create = []  # For bulk creation

            for row in reader:
                exam_names = [name.strip() for name in row["exam_types"].split(",")]  # ✅ Handle multiple exams
                duration = int(row.get("duration", 15))  # Default to 15 min if missing

                # ✅ Ensure all ExamType records exist
                exam_objs = []
                for exam_name in exam_names:
                    exam_obj, created = ExamType.objects.get_or_create(name=exam_name)
                    exam_objs.append(exam_obj)

                # ✅ Create the passage with empty `passage` field
                passage_obj = ExamContent(
                    passage="",  # ✅ Keep passage empty as requested
                    passage_english=row.get("passage_english", ""),
                    passage_hindi=row.get("passage_hindi", ""),
                    duration=duration,
                )
                passage_obj.save()  # Save first to get an ID before adding ManyToMany

                # ✅ Attach the ExamType(s)
                passage_obj.exam_types.set(exam_objs)
                passage_obj.save()

                passages_to_create.append(passage_obj)

        self.stdout.write(self.style.SUCCESS(f"✅ Successfully imported {len(passages_to_create)} passages!"))
