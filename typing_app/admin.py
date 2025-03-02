from django.contrib import admin
from .models import *


@admin.register(ExamContent)
class ExamContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_exam_types', 'has_english', 'has_hindi','has_german', 'has_french', 'duration', 'created_at')  # ✅ Improved List Display
    search_fields = ('passage_english', 'passage_hindi', 'passage_german', 'passage_french')  # ✅ Enables search for passages
    list_filter = ('exam_types',)  # ✅ Adds filter for exam types
    ordering = ('-created_at',)  # ✅ Orders newest passages first
    list_per_page = 20  # ✅ Limits per page entries for better readability

    def get_exam_types(self, obj):
        """Display multiple exam types as a comma-separated list."""
        return ", ".join([exam.name for exam in obj.exam_types.all()])
    get_exam_types.short_description = "Exam Types"  # ✅ Fix field name in admin panel

    def has_english(self, obj):
        """Check if an English passage exists and prevent false positives."""
        if obj.passage_english is None or obj.passage_english.strip().lower() == "none" or obj.passage_english.strip() == "":
            return False
        return True

    has_english.boolean = True
    has_english.short_description = "English Available"

    def has_hindi(self, obj):
        """Check if a Hindi passage exists and prevent false positives."""
        if obj.passage_hindi is None or obj.passage_hindi.strip().lower() == "none" or obj.passage_hindi.strip() == "":
            return False
        return True

    has_hindi.boolean = True
    has_hindi.short_description = "Hindi Available"

    def has_german(self, obj):
        if obj.passage_german is None or obj.passage_german.strip().lower() == "none" or obj.passage_german.strip() == "":
            return False
        return True

    has_german.boolean = True
    has_german.short_description = "German Available"

    def has_french(self, obj):
        if obj.passage_french is None or obj.passage_french.strip().lower() == "none" or obj.passage_french.strip() == "":
            return False
        return True

    has_french.boolean = True
    has_french.short_description = "French Available"




@admin.register(ExamType)
class ExamTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'instructions_preview')  # ✅ Show ID, Exam Name, and Instructions
    search_fields = ('name',)  # ✅ Search by Exam Name
    ordering = ('name',)

    def instructions_preview(self, obj):
        """Show first few lines of instructions in Admin Panel."""
        return obj.instructions[:50] + "..." if obj.instructions else "No instructions found"

    instructions_preview.short_description = "Instructions"




@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('title', 'content')


# @admin.register(TestResult)
# class TestResultAdmin(admin.ModelAdmin):
#     list_display = ('exam_content', 'session_id')
#     search_fields = ('exam_content__exam_type', 'session_id')
    # ordering = ('-test_date',)

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