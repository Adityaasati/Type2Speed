from django.contrib import admin
from .models import *


@admin.register(ExamContent)
class ExamContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_exam_types', 'has_english', 'has_hindi', 'duration', 'created_at')  # ✅ Improved List Display
    search_fields = ('passage_english', 'passage_hindi')  # ✅ Enables search for passages
    list_filter = ('exam_types',)  # ✅ Adds filter for exam types
    ordering = ('-created_at',)  # ✅ Orders newest passages first
    list_per_page = 20  # ✅ Limits per page entries for better readability

    def get_exam_types(self, obj):
        """Display multiple exam types as a comma-separated list."""
        return ", ".join([exam.name for exam in obj.exam_types.all()])
    get_exam_types.short_description = "Exam Types"  # ✅ Fix field name in admin panel

    def has_english(self, obj):
        """Check if an English passage exists."""
        return bool(obj.passage_english)
    has_english.boolean = True
    has_english.short_description = "English Available"

    def has_hindi(self, obj):
        """Check if a Hindi passage exists."""
        return bool(obj.passage_hindi)
    has_hindi.boolean = True
    has_hindi.short_description = "Hindi Available"

@admin.register(ExamType)
class ExamTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # ✅ Show ID and Exam Type name
    search_fields = ('name',)  # ✅ Allow searching by exam name
    ordering = ('name',)  # ✅ Sort alphabetically

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('exam_content', 'wpm', 'accuracy', 'errors', 'test_date')
    search_fields = ('exam_content__exam_type', 'session_id')
    ordering = ('-test_date',)

@admin.register(AdPlacement)
class AdPlacementAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
    search_fields = ('name',)
    list_filter = ('active',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('email', 'suggestion','submitted_at')
    search_fields = ('email',)
    list_filter = ('suggestion',)