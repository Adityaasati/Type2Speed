import csv
from django.core.management.base import BaseCommand
from typing_app.models import ExamType, ExamContent
from datetime import datetime

class Command(BaseCommand):
    help = 'Import passages (English and Hindi) and duration into ExamContent'

    def handle(self, *args, **kwargs):
        # Path to your CSV file
        file_path = "passages.csv"  # Replace with the actual file path

        # Open and read the CSV file
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                exam_type_names = row['exam_type_name'].split(",")  # Split if multiple exam types are given
                passage_english = row['passage_english']
                passage_hindi = row['passage_hindi']
                duration_str = row['duration']

                # Remove unwanted triple quotes (""" ) and extra quotes from passages
                if passage_english:
                    # Strip triple quotes and handle internal line breaks
                    passage_english = passage_english.strip('"""').replace('"""', '').replace('"', '').strip()

                if passage_hindi:
                    # Strip triple quotes and handle internal line breaks
                    passage_hindi = passage_hindi.strip('"""').replace('"""', '').replace('"', '').strip()

                # Validate the duration field
                try:
                    # Convert the duration to an integer, if possible
                    duration = int(duration_str)
                except ValueError:
                    # If it's not a valid number, skip this row or set a default value
                    self.stdout.write(self.style.ERROR(f"Invalid duration value for {exam_type_names}, skipping..."))
                    continue  # Skip the row if duration is invalid

                # Get or create ExamType(s)
                exam_types = []
                for exam_type_name in exam_type_names:
                    exam_type_name = exam_type_name.strip()
                    exam_type, created = ExamType.objects.get_or_create(name=exam_type_name)
                    exam_types.append(exam_type)

                # Create ExamContent with the English and Hindi passages and duration
                exam_content = ExamContent.objects.create(
                    passage_english=passage_english if passage_english else None,
                    passage_hindi=passage_hindi if passage_hindi else None,
                    duration=duration,
                )

                # Add exam_types (ManyToMany relationship)
                exam_content.exam_types.set(exam_types)  # Associate exam types with this content
                exam_content.save()

                # Output to indicate the process is running
                self.stdout.write(self.style.SUCCESS(f"Successfully imported passage number {reader.line_num} for {', '.join(exam_type_names)}"))
