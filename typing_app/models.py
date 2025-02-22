from django.db import models


class ExamContent(models.Model):
    """Stores typing test passages and instructions for multiple exams."""
    
    EXAM_CHOICES = [
        ('CHSL', 'CHSL Exam'),
        ('CGL', 'CGL Exam'),
        ('NTPC', 'NTPC Exam'),
        ('CPCT', 'CPCT Exam'),
        ('PRACTISE', 'PRACTISE'),
    ]
    
    exam_types = models.ManyToManyField('ExamType', related_name="exam_contents")  # ✅ Many-to-Many Relationship
    instructions = models.TextField(help_text="Detailed instructions for the typing test")
    passage = models.TextField(help_text="Typing passage for the test",blank=True)
    passage_english = models.TextField(blank=True, null=True)  # English passage (CPCT)
    passage_hindi = models.TextField(blank=True, null=True)
    duration = models.IntegerField(default=10, help_text="Duration in minutes")  # ✅ Custom duration

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Passage for {', '.join([exam.name for exam in self.exam_types.all()])}"

class ExamType(models.Model):
    """Stores different exam types (CHSL, CGL, NTPC)."""
    name = models.CharField(max_length=10, choices=[
        ('CHSL', 'CHSL Exam'),
        ('CGL', 'CGL Exam'),
        ('NTPC', 'NTPC Exam'),
        ('CPCT', 'CPCT Exam'),
        ('PRACTISE', 'PRACTISE'),
        
        
    ], unique=True)

    def __str__(self):
        return self.get_name_display()


class TestResult(models.Model):
    """Stores typing test results (No login required for now)."""
    exam_content = models.ForeignKey(ExamContent, on_delete=models.CASCADE, null=True, blank=True)  # Temporarily allow null
    session_id = models.CharField(max_length=50, help_text="Unique session identifier")
    wpm = models.FloatField(default=0.0)
    accuracy = models.FloatField(default=0.0)
    errors = models.PositiveIntegerField(default=0)
    backspaces = models.PositiveIntegerField(default=0) 
    spaces = models.PositiveIntegerField(default=0)
    test_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Test: {self.exam_content.exam_type if self.exam_content else 'Unknown'} | WPM: {self.wpm} | Acc: {self.accuracy}%"



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
