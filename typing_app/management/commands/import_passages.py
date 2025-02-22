import csv
from django.core.management.base import BaseCommand
from typing_app.models import ExamContent, ExamType

class Command(BaseCommand):
    help = "Bulk import passages from a CSV file."

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help="Path to the CSV file")

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                passage_text = row['passage']
                instructions = row['instructions']
                duration = int(row['duration'])
                exam_names = row['exam_types'].split(',')

                # Get or create ExamType instances
                exams = ExamType.objects.filter(name__in=exam_names)
                
                # Create ExamContent and link to exams
                exam_content = ExamContent.objects.create(
                    passage=passage_text,
                    instructions=instructions,
                    duration=duration
                )
                exam_content.exam_types.set(exams)

                self.stdout.write(self.style.SUCCESS(f"Added passage for {exam_names}"))
