from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.conf import settings
from .models import ExamContent, ExamType, Feedback, TypingGameResult, Blog


from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ['home', 'tips', 'tests', 'feedback', 'privacy-policy', 'terms-and-conditions', 'typing-games']

    def location(self, item):
        return reverse(item)
    
    
class DynamicPagesSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        all_items = []

        # Exam Types and Contents
        exam_types = ExamType.objects.all()
        for exam_type in exam_types:
            all_items.append(('passages', exam_type.name))
            all_items.append(('practise-instructions', exam_type.name))
            all_items.append(('typing-test', exam_type.name)) # typing test without passage id.

            exam_contents = ExamContent.objects.filter(exam_types=exam_type)
            for content in exam_contents:
                all_items.append(('instructions', exam_type.name, content.id))
                all_items.append(('typing-test-exams', exam_type.name, content.id)) # typing test with passage id.
                all_items.append(('test-result', exam_type.name))

        # Typing Game Results
        game_choices = TypingGameResult.GAME_CHOICES
        for game_choice in game_choices:
            all_items.append(('typing-game', game_choice[0]))
            all_items.append(('submit-typing-game', game_choice[0]))

        #Blog Posts
        blogs = Blog.objects.filter(is_published = True)
        for blog in blogs:
            all_items.append(('blog-detail', blog.slug))

        return all_items

    def location(self, item):
        if isinstance(item, tuple):
            if item[0] == 'passages':
                return reverse('passages', args=[item[1]])
            elif item[0] == 'instructions':
                return reverse('instructions', args=[item[1], item[2]])
            elif item[0] == 'practise-instructions':
                return reverse('practise-instructions', args=[item[1]])
            elif item[0] == 'typing-test':
                return reverse('typing-test', args=[item[1]])
            elif item[0] == 'typing-test-exams':
                return reverse('typing-test-exams', args=[item[1], 'english', item[2]])
            elif item[0] == 'test-result':
                return reverse('test-result', args=[item[1]])
            elif item[0] == 'typing-game':
                return reverse('typing-game', args=[item[1]])
            elif item[0] == 'submit-typing-game':
                return reverse('submit-typing-game', args=[item[1]])
            elif item[0] == 'blog-detail':
                return reverse('blog-detail', args = [item[1]])
            else:
                print(f"Error: Unhandled tuple in location: {item}")
                return "/"
        else:
            try:
                return reverse(item)
            except Exception as e:
                print(f"Error reversing {item}: {e}")
                return "/"

    def get_absolute_uri(self, location):
        return f"http://{settings.SITE_DOMAIN}{location}"

    def lastmod(self, item):
        if isinstance(item, tuple):
            if item[0] in ['instructions', 'typing-test-exams']:
                try:
                    exam_content = ExamContent.objects.get(id=item[2])
                    return exam_content.created_at #or use a last modified date.
                except ExamContent.DoesNotExist:
                    return None
            elif item[0] == 'blog-detail':
                try:
                    blog = Blog.objects.get(slug = item[1])
                    return blog.updated_at
                except Blog.DoesNotExist:
                    return None
        return None
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    