from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import *  # Assuming Passage model holds exam_type, passage_id, and other related data

class StaticViewSitemap(Sitemap):
    def items(self):
        return ['home', 'tips', 'tests', 'feedback', 'privacy-policy', 'terms-and-conditions', 'typing-games']

    def location(self, item):
        return reverse(item)

class DynamicPagesSitemap(Sitemap):
    def items(self):
        # Add static and dynamic pages
        return ['passages', 'instructions', 'typing-test', 'test-result', 'practise-instructions', 'typing-games', 'typing-game', 'submit-typing-game']

    def location(self, item):
        # Handle static URLs first
        if item == 'passages':
            exam_types = ['CPCT', 'CHSL', 'CGL', 'NTPC', 'PRACTISE']
            urls = []
            for exam_type in exam_types:
                # Generate URL for passages
                urls.append(reverse(item, args=[exam_type]))
            return urls

        elif item == 'instructions':
            # For instructions, generate URLs based on exam_type and passage_id
            exam_types = ['CPCT', 'CHSL', 'CGL', 'NTPC', 'PRACTISE']
            passage_ids = [1, 2, 3]  # Assuming we have a list of passage_ids to loop through
            urls = []
            for exam_type in exam_types:
                for passage_id in passage_ids:
                    # Generate URL for instructions page
                    urls.append(reverse(item, args=[exam_type, passage_id]))
            return urls

        elif item == 'typing-test':
            exam_types = ['CPCT', 'CHSL', 'CGL', 'NTPC', 'PRACTISE']
            passage_ids = [1, 2, 3]  # Example passage IDs
            urls = []
            for exam_type in exam_types:
                for passage_id in passage_ids:
                    # Generate URL for exam-specific typing test
                    urls.append(reverse('typing-test-exam-specific', args=[exam_type, passage_id]))
            return urls

        elif item == 'test-result':
            exam_types = ['CPCT', 'CHSL', 'CGL', 'NTPC', 'PRACTISE']
            urls = []
            for exam_type in exam_types:
                # Generate URL for test results page
                urls.append(reverse(item, args=[exam_type]))
            return urls

        elif item == 'practise-instructions':
            # Only for 'practise' exam type
            return [reverse(item, args=['practise'])]

        elif item == 'typing-games':
            # Static URL for typing games
            return [reverse(item)]

        elif item == 'typing-game':
            game_names = ['game1', 'game2', 'game3']  # Example game names, can be fetched dynamically if needed
            urls = []
            for game_name in game_names:
                # Generate URL for each typing game
                urls.append(reverse(item, args=[game_name]))
            return urls

        elif item == 'submit-typing-game':
            game_names = ['game1', 'game2', 'game3']
            urls = []
            for game_name in game_names:
                # Generate URL for submitting typing game results
                urls.append(reverse(item, args=[game_name]))
            return urls

        return reverse(item)

class AdsSitemap(Sitemap):
    def items(self):
        # Static URL for ads.txt
        return ['ads-get']

    def location(self, item):
        return reverse(item)
