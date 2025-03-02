from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class ExamContent(models.Model):
    """Stores typing test passages for multiple exams."""
    
    exam_types = models.ManyToManyField('ExamType', related_name="exam_contents")  # ✅ Many-to-Many Relationship
    # passage = models.TextField(help_text="Typing passage for the test", blank=True)
    passage_english = models.TextField(blank=True, null=True)  # English passage (CPCT)
    passage_hindi = models.TextField(blank=True, null=True)
    passage_german = models.TextField(blank=True, null=True)  # For German
    passage_french = models.TextField(blank=True, null=True)  # For French
    duration = models.IntegerField(default=15, help_text="Duration in minutes")  # ✅ Custom duration
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Passage for {', '.join([exam.name for exam in self.exam_types.all()])}"
    
    
    
class ExamType(models.Model):
    """Stores different exam types dynamically along with instructions."""
    name = models.CharField(max_length=50, unique=True)  # ✅ Now dynamically adding exams
    instructions = models.TextField(
        help_text="Instructions for this exam type",
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        """Ensure every exam type has default instructions if not provided."""
        if not self.instructions:
            self.instructions = "Please write instructions for this exam"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name  # ✅ Display exam name directly


# class TestResult(models.Model):
#     """Stores typing test results (No login required for now)."""
#     exam_content = models.ForeignKey(ExamContent, on_delete=models.CASCADE, null=True, blank=True)  # Temporarily allow null
#     session_id = models.CharField(max_length=50, help_text="Unique session identifier")
#     wpm = models.FloatField(default=0.0)
#     accuracy = models.FloatField(default=0.0)
#     errors = models.PositiveIntegerField(default=0)
#     backspaces = models.PositiveIntegerField(default=0) 
#     spaces = models.PositiveIntegerField(default=0)
#     test_date = models.DateTimeField(auto_now_add=True)
#     full_mistakes = models.PositiveIntegerField(default=0)  # Count of full mistakes (e.g., omissions, substitutions)
#     half_mistakes = models.PositiveIntegerField(default=0)
#     time_taken = models.FloatField(default=0.0)
#     total_errors = models.PositiveIntegerField(default=0)
#     omissions = models.PositiveIntegerField(default=0)  # Omission errors (full mistakes)
#     substitutions = models.PositiveIntegerField(default=0)  # Substitution errors (full mistakes)
#     spelling_errors = models.PositiveIntegerField(default=0)  # Spelling errors (full mistakes)
#     repetitions = models.PositiveIntegerField(default=0)  # Repetition errors (full mistakes)
#     incomplete_words = models.PositiveIntegerField(default=0)  # Incomplete words (full mistakes)
#     additions = models.PositiveIntegerField(default=0)
#     spacing = models.PositiveIntegerField(default=0)  # Spacing errors (half mistakes)
#     capitalization = models.PositiveIntegerField(default=0)  # Capitalization errors (half mistakes)
#     punctuation = models.PositiveIntegerField(default=0)
#     total_words_typed = models.PositiveIntegerField(default=0)  # Total words typed
#     actual_key_depressions = models.PositiveIntegerField(default=0)

#     def __str__(self):
#         return f"Test Result for {self.exam_content.exam_types if self.exam_content else 'Unknown'}"

#     def calculate_total_errors(self):
#         self.total_errors = self.full_mistakes + self.half_mistakes
#         self.save()

class AdPlacement(models.Model):
    """Allows management of ad placement in templates."""
    name = models.CharField(max_length=100, help_text="E.g., Sidebar Top, Below Passage")
    code = models.TextField(help_text="Google AdSense or other ad code")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Ad - {self.name} ({'Active' if self.active else 'Inactive'})"


class Feedback(models.Model):
    """Stores user feedback and suggestions."""
    email = models.EmailField(help_text="User's email address")
    suggestion = models.TextField(help_text="User's feedback or suggestion")
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.email} - {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"

class TypingGameResult(models.Model):
    """Stores user typing results for different typing games."""
    GAME_CHOICES = [
        ("speed_typing", "Speed Typing Challenge"),
        ("key_hit_trainer", "Key Hit Trainer"),
        ("missing_word", "Type the Missing Word"),
    ]

    session_id = models.CharField(max_length=50, help_text="Unique session identifier")
    game_name = models.CharField(max_length=50, choices=GAME_CHOICES)
    passage = models.TextField(blank=True, null=True)  # Not needed for Key Hit Trainer
    correct_hits = models.PositiveIntegerField(default=0)
    incorrect_hits = models.PositiveIntegerField(default=0)
    wpm = models.FloatField(default=0.0)
    accuracy = models.FloatField(default=0.0)
    errors = models.PositiveIntegerField(default=0)
    time_taken = models.IntegerField(default=60)  # Time limit (30s, 60s, 120s)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_game_name_display()} | WPM: {self.wpm} | Acc: {self.accuracy}%"





class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=255, blank=True)
    keywords = models.CharField(max_length=750, blank=True)
    featured_image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    ads_code = models.TextField(blank=True, null=True)  # Store ad code if needed for monetization
    is_published = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=255) 

    def save(self, *args, **kwargs):
        # Automatically generate the slug from the title if it's empty
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']


