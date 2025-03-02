from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

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
        print(f"Generating URL for: {item}")  # Debug print
        
        # Handle static URLs first
        if item == 'passages':
            exam_types = ['CPCT', 'CHSL', 'CGL', 'NTPC', 'PRACTISE']
            urls = []
            for exam_type in exam_types:
                # Generate URL for passages
                url = reverse(item, args=[exam_type])
                print(f"Passages URL: {url}")  # Debug print
                urls.append(url)
            return urls

        elif item == 'instructions':
            # For instructions, generate URLs based on exam_type and passage_id
            exam_types = ['CPCT', 'CHSL', 'CGL', 'NTPC', 'PRACTISE']
            passage_ids = [1, 2, 3]  # Assuming we have a list of passage_ids to loop through
            urls = []
            for exam_type in exam_types:
                for passage_id in passage_ids:
                    url = reverse(item, args=[exam_type, passage_id])
                    print(f"Instructions URL: {url}")  # Debug print
                    urls.append(url)
            return urls

        elif item == 'typing-test':
            exam_types = ['CPCT', 'CHSL', 'CGL', 'NTPC', 'PRACTISE']
            passage_ids = [1, 2, 3]  # Example passage IDs
            urls = []
            for exam_type in exam_types:
                for passage_id in passage_ids:
                    url = reverse('typing-test-exam-specific', args=[exam_type, passage_id])
                    print(f"Typing Test URL: {url}")  # Debug print
                    urls.append(url)
            return urls

        elif item == 'test-result':
            exam_types = ['CPCT', 'CHSL', 'CGL', 'NTPC', 'PRACTISE']
            urls = []
            for exam_type in exam_types:
                url = reverse(item, args=[exam_type])
                print(f"Test Result URL: {url}")  # Debug print
                urls.append(url)
            return urls

        elif item == 'practise-instructions':
            # Only for 'practise' exam type
            url = reverse(item, args=['practise'])
            print(f"Practise Instructions URL: {url}")  # Debug print
            return [url]

        elif item == 'typing-games':
            # Static URL for typing games
            url = reverse(item)
            print(f"Typing Games URL: {url}")  # Debug print
            return [url]

        elif item == 'typing-game':
            game_names = ['game1', 'game2', 'game3']  # Example game names
            urls = []
            for game_name in game_names:
                url = reverse(item, args=[game_name])
                print(f"Typing Game URL: {url}")  # Debug print
                urls.append(url)
            return urls

        elif item == 'submit-typing-game':
            game_names = ['game1', 'game2', 'game3']
            urls = []
            for game_name in game_names:
                url = reverse(item, args=[game_name])
                print(f"Submit Typing Game URL: {url}")  # Debug print
                urls.append(url)
            return urls

        return reverse(item)

class AdsSitemap(Sitemap):
    def items(self):
        # Static URL for ads.txt
        return ['ads-get']

    def location(self, item):
        return reverse(item)
