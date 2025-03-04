from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
import uuid
import random
import re
from difflib import SequenceMatcher
from .models import *
from .forms import FeedbackForm
import time
from django.http import HttpResponse


def home_view(request):
    color_map = {
    "CHSL": "primary",
    "CGL": "success",
    "CPCT": "danger",
    "PRACTISE": "info",
    "NTPC": "secondary",

}
    exams = ExamType.objects.all()  # Fetch all exam types from the database
    exams = exams.exclude(name="PRACTISE")
    for exam in exams:
        exam.color = color_map.get(exam.name, "secondary") 
    exam_count = exams.count()  # Get the number of exams
    column_size = 12 // min(exam_count, 4)  # Dynamically calculate the column size
    ads = AdPlacement.objects.filter(active=True)
    
    return render(request, "typing_app/home.html", {"exams": exams, "column_size": column_size,"ads": ads})
 


def tips_view(request):
    return render(request, "typing_app/tips.html")


def tests_view(request):
    exams = ExamType.objects.all()  # Fetch all exam types from the database
    exams = exams.exclude(name="PRACTISE")
    exam_count = exams.count()  # Get the number of exams
    column_size = 12 // min(exam_count, 4)  # Dynamically calculate the column size
    return render(request, "typing_app/tests.html", {"exams": exams, "column_size": column_size})



def passages_view(request, exam_type):
    """Displays available passages for a selected exam type."""
    predefined_durations = [5, 10, 15, 20, 25, 30]

    try:
        exam_type_obj = ExamType.objects.get(name=exam_type)
    except ExamType.DoesNotExist:
        return render(request, "typing_app/error.html", {
            "message": f"No passages found for {exam_type}. Please contact support."
        }, status=404)

    if exam_type == "CPCT" or exam_type == "NTPC" or exam_type == "ARO" :
        # ✅ Fetch separate lists of Hindi and English passages (max 10 each)
        hindi_passages = ExamContent.objects.filter(
            exam_types=exam_type_obj
        ).exclude(passage_hindi__isnull=True).exclude(passage_hindi="")[:10]

        english_passages = ExamContent.objects.filter(
            exam_types=exam_type_obj
        ).exclude(passage_english__isnull=True).exclude(passage_english="")[:10]

        return render(request, "typing_app/passages.html", {
            "exam_type": exam_type,
            "hindi_passages": hindi_passages,  # ✅ Hindi on left side
            "english_passages": english_passages,  # ✅ English on right side
            "predefined_durations": predefined_durations
        })

    else:
        # ✅ For non-CPCT exams, keep the existing logic
        passages_data = ExamContent.objects.filter(exam_types=exam_type_obj)[:20]

        return render(request, "typing_app/passages.html", {
            "exam_type": exam_type,
            "passages_data": passages_data,
            "predefined_durations": predefined_durations
        })

# views.py

# def passages_languages_view(request, exam_type, language, duration):
#     # Define the possible predefined durations and languages for reference (in case you need them later)
#     predefined_durations = [5, 10, 15, 20, 25, 30]
#     languages = ["Hindi", "English", "German", "French"]

#     # Check if the passed language and duration are valid
#     if language not in languages:
#         return render(request, "typing_app/error.html", {"error": "Invalid language selected!"})
#     if duration not in predefined_durations:
#         return render(request, "typing_app/error.html", {"error": "Invalid duration selected!"})

#     # Now, pass the selected language and duration to the template
#     return render(request, "typing_app/practise_instructions.html", {
#         "exam_type": exam_type,
#         "language": language,
#         "duration": duration,
#         "languages": languages,
#         "predefined_durations": predefined_durations,
#     })



def practise_instruction_view(request, exam_type):
    """Displays instructions for the selected exam type."""
    
    # ✅ Get the exam type object and instructions
    try:
        exam_type_obj = ExamType.objects.get(name=exam_type)
    except ExamType.DoesNotExist:
        return render(request, "typing_app/error.html", {
            "message": f"No instructions found for {exam_type}. Please contact support."
        }, status=404)

    # ✅ No need to fetch a passage here (it will be done in the typing test view)
    predefined_durations = [5, 10, 15, 20, 25, 30]

    return render(request, "typing_app/practise_instructions.html", {
        "exam_type": exam_type,
        "instructions": exam_type_obj.instructions,  # ✅ Fetching from ExamType
        "predefined_durations": predefined_durations,  # ✅ Allow user to select duration
    })




def instruction_view(request, exam_type, passage_id):
    """Displays instructions for the selected exam type and passage."""
    language = request.GET.get("language", "english").lower()
    print(exam_type,"yhi hai")
    

    # ✅ Get the exam type object and instructions
    try:
        exam_type_obj = ExamType.objects.get(name=exam_type)
    except ExamType.DoesNotExist:
        return render(request, "typing_app/error.html", {
            "message": f"No instructions found for {exam_type}. Please contact support."
        }, status=404)

    # ✅ Fetch selected passage by ID
    try:
        exam_content = ExamContent.objects.get(id=passage_id, exam_types=exam_type_obj)
    except ExamContent.DoesNotExist:
        return render(request, "typing_app/error.html", {
            "message": f"Passage not found for {exam_type}. Please select again."
        }, status=404)

    return render(request, "typing_app/instructions.html", {
        "exam_type": exam_type,
        "instructions": exam_type_obj.instructions,  # ✅ Fetching from ExamType
        "passage_id": passage_id,
        "language":language
        
    })



def typing_test_view(request, exam_type, passage_id=None, language="english",duration=10):
    """ Fetches a passage dynamically if passage_id is not provided. """

    if passage_id:
        # ✅ Get the passage using the provided ID
        exam_content = get_object_or_404(ExamContent, id=passage_id)
        print(exam_type,passage_id)
    else:
        # ✅ Fetch passages dynamically based on exam type
        if exam_type == "PRACTISE":
            language = request.GET.get("language", "english").lower()
            # ✅ Get language from URL
            selected_duration = int(request.GET.get("duration", 10))  

            # ✅ Filter by exam type, language, and duration
            if language == "english":
                exam_contents = ExamContent.objects.filter(
                    exam_types__name=exam_type,
                    duration=selected_duration
                ).exclude(passage_english__isnull=True).exclude(passage_english="")
            elif language == "hindi":  # Hindi case
                exam_contents = ExamContent.objects.filter(
                    exam_types__name=exam_type,
                    duration=selected_duration
                ).exclude(passage_hindi__isnull=True).exclude(passage_hindi="")
            elif language == "german":  # German case
                exam_contents = ExamContent.objects.filter(
                    exam_types__name=exam_type,
                    duration=selected_duration
                ).exclude(passage_german__isnull=True).exclude(passage_german="")
            else :  # Hindi case
                exam_contents = ExamContent.objects.filter(
                    exam_types__name=exam_type,
                    duration=selected_duration
                ).exclude(passage_french__isnull=True).exclude(passage_french="")
        else:

            # ✅ Fetch correct passages for CGL, CHSL, and all other exams (Only English)
            exam_contents = ExamContent.objects.filter(
                exam_types__name=exam_type
            ).exclude(passage_english__isnull=True).exclude(passage_english="")


        # ✅ Select a passage randomly
        if exam_contents.exists():
            if exam_contents.count() > 1:
                exam_content = random.choice(list(exam_contents))  # ✅ Ensure random.choice gets a list
            else:
                exam_content = exam_contents.first()
        else:
            return render(request, "typing_app/error.html", {
                "message": f"No passage found for {exam_type} in {language} with {selected_duration} minutes."
            }, status=404)

    if exam_type != "PRACTISE":
        selected_duration = exam_content.duration  

    
    if language == "hindi":
        passage = exam_content.passage_hindi
    elif language == "german":
        passage = exam_content.passage_german
    elif language == "french":
        passage = exam_content.passage_french
    else:
        passage = exam_content.passage_english


    return render(request, "typing_app/typing_test.html", {
        "exam_type": exam_type,
        "passage": passage,
        "language": language,
        "duration": selected_duration,  # ✅ Pass correct duration from the passage
    })





# Helper function to calculate WPM, accuracy, and handle mistakes
def calculate_wpm_and_accuracy(typed_text, passage_text,duration):
    words_typed = typed_text.split()
    words_passage = passage_text.split()

    total_words_typed = len(words_typed)
    correct_words = 0
    mistakes = {
        'full': 0,  # Full mistakes count
        'half': 0,  # Half mistakes count
        'omissions': 0,  # Omission errors (full mistakes)
        'substitutions': 0,  # Substitution errors (full mistakes)
        'spelling_errors': 0,  # Spelling errors (full mistakes)
        'repetitions': 0,  # Repetition errors (full mistakes)
        'incomplete_words': 0,  # Incomplete words (full mistakes)
        'additions': 0,  # Addition errors (full mistakes)
        'spacing': 0,  # Spacing errors (half mistakes)
        'capitalization': 0,  # Capitalization errors (half mistakes)
        'punctuation': 0  # Punctuation errors (half mistakes)
    }

    # To handle word-by-word comparison
    for i in range(min(len(words_typed), len(words_passage))):
        typed_word = words_typed[i]
        correct_word = words_passage[i]
        
        if typed_word != correct_word:
            mistakes['full'] += 1  # Count as a full mistake

            # Additional checks for specific full mistakes
            if typed_word == '':
                mistakes['omissions'] += 1  # Omission
            elif typed_word != correct_word:
                mistakes['substitutions'] += 1  # Substitution

    # Check for additional words typed (Additions)
    if len(words_typed) > len(words_passage):
        mistakes['full'] += len(words_typed) - len(words_passage)
        mistakes['additions'] += len(words_typed) - len(words_passage)

    # Check for repetition of words
    seen_words = set()
    for word in words_typed:
        if word in seen_words:
            mistakes['full'] += 1  # Repeated word is a full mistake
            mistakes['repetitions'] += 1  # Track repetition
        seen_words.add(word)

    # Check for incomplete words (half-typed words)
    for word in words_typed:
        if len(word) < 2:  # A basic check for incomplete words (e.g., "h" instead of "hello")
            mistakes['full'] += 1
            mistakes['incomplete_words'] += 1  # Track incomplete word

    # Check for spacing errors (half mistakes)
    for i in range(1, len(words_typed)):
        if words_typed[i-1] == '' or words_typed[i] == '':
            mistakes['half'] += 1  # No space or undesired space between words
            mistakes['spacing'] += 1  # Track spacing errors

    # Check for capitalization errors (half mistakes)
    for typed_word, correct_word in zip(words_typed, words_passage):
        if typed_word.lower() == correct_word.lower() and typed_word != correct_word:
            mistakes['half'] += 1  # Incorrect capitalization is a half mistake
            mistakes['capitalization'] += 1  # Track capitalization errors

    # Check for punctuation errors (half mistakes)
    for typed_word, correct_word in zip(words_typed, words_passage):
        if typed_word.strip(",.!?") == correct_word.strip(",.!?") and typed_word != correct_word:
            mistakes['half'] += 1  # Incorrect punctuation is a half mistake
            mistakes['punctuation'] += 1  # Track punctuation errors

    # Calculate WPM (Words per Minute)
    wpm = total_words_typed / duration if duration > 0 else 0

    # Round the WPM to 2 decimal places to make it more readable
    wpm = round(wpm, 2)

    # Calculate accuracy
    accuracy = (correct_words / total_words_typed) * 100 if total_words_typed > 0 else 0

    # Return all calculated metrics
    return wpm, accuracy, mistakes, total_words_typed, len(typed_text)  # Returning key depressions as length of typed text

def calculate_ssc_view(passage, user_input, duration):
    """Calculate typing test results for SSC exams (CGL/CHSL)"""
    start_time = time.time()  # Start time for calculation
    
    # Calculate WPM, accuracy, and mistakes using the existing helper function
    typed_text = user_input.strip() 

    # Calculate WPM, accuracy, and mistakes
    wpm, accuracy, mistakes, total_words_typed, actual_key_depressions = calculate_wpm_and_accuracy(typed_text, passage,duration)

    result = {
        'passage': passage,
        'typed_text': typed_text,
        'wpm': wpm,
        'accuracy': accuracy,
        'full_mistakes': mistakes['full'],
        'half_mistakes': mistakes['half'],
        'omissions': mistakes['omissions'],
        'substitutions': mistakes['substitutions'],
        'spelling_errors': mistakes['spelling_errors'],
        'repetitions': mistakes['repetitions'],
        'incomplete_words': mistakes['incomplete_words'],
        'additions': mistakes['additions'],
        'spacing': mistakes['spacing'],
        'capitalization': mistakes['capitalization'],
        'punctuation': mistakes['punctuation'],
        'total_words_typed': total_words_typed,
        'actual_key_depressions': actual_key_depressions,
        'time_taken': (time.time() - start_time),
    }
    return result




# Main View for Calculating SSC Exam (CGL/CHSL)

def calculate_all_metrics(passage, user_input, duration):
    """Minimal CPCT calculations with only essential metrics."""
    passage_words = passage.split()
    user_words = user_input.split()

    total_word_count = len(passage_words)
    typed_word_count = len(user_words)
    pending_word_count = max(0, total_word_count - typed_word_count)

    # ✅ Calculate errors as the difference between passage & user input
    errors = sum(1 for p, u in zip(passage_words, user_words) if p != u)
    errors += abs(len(passage_words) - len(user_words))  # Account for missing/extra words

    # ✅ Keystroke count (Total typed characters)
    keystrokes_count = len(user_input)

    # ✅ Calculate NWPM (Net Words Per Minute)
    net_wpm = max(0, (typed_word_count - errors) / (duration / 60))  # Avoid negative NWPM

    return {
        "errors": errors,
        "keystrokes_count": keystrokes_count,
        "total_word_count": total_word_count,
        "typed_word_count": typed_word_count,
        "pending_word_count": pending_word_count,
        "net_wpm": round(net_wpm, 2)  # ✅ Ensure NWPM is rounded to 2 decimal places
    }

def calculate_scaled_score(nwpm, exam_type, language):
    """Returns scaled percentage based on NWPM for Hindi or English."""
    hindi_scores = [(20, 25, 50), (26, 30, 60), (31, 35, 70), (36, 40, 80), (41, 50, 90), (51, float('inf'), 100)]
    english_scores = [(30, 40, 50), (41, 50, 60), (51, 60, 70), (61, 70, 80), (71, 80, 90), (81, float('inf'), 100)]

    score_chart = hindi_scores if language == "hindi" else english_scores

    for min_wpm, max_wpm, score in score_chart:
        if min_wpm <= nwpm <= max_wpm:
            return score
    return 0  # Default if NWPM is too low


def test_result_view(request, exam_type):
    """Applies different typing test rules based on the exam type."""
    
    if request.method == "POST":
        passage_id = request.POST.get('passage_id')
        if passage_id:
            exam_content = get_object_or_404(ExamContent, id=passage_id)
        else:
            exam_contents = ExamContent.objects.filter(exam_types__name=exam_type)
            if not exam_contents.exists():
                return render(request, "typing_app/error.html", {
                    "message": f"No passage found for {exam_type}. Please contact support."
                }, status=404)
            exam_content = random.choice(exam_contents)

        user_input = request.POST.get('userInput', '').strip()
        session_id = request.POST.get('session_id', str(uuid.uuid4()))
        backspaces = int(request.POST.get('backspaces', 0))
        spaces = int(request.POST.get('spaces', 0))


        
        language = request.GET.get("language") or "english" 
            
        if language == "hindi":
            passage = exam_content.passage_hindi.strip() if exam_content.passage_hindi else ""  # Use passage_hindi for Hindi
        elif language == "english":
            passage = exam_content.passage_english.strip() if exam_content.passage_english else ""  # Use passage_english for English
        elif language == "german":
            passage = exam_content.passage_german.strip() if exam_content.passage_german else ""
        elif language == "french":
            passage = exam_content.passage_french.strip() if exam_content.passage_french else ""
        
        
        # Normalize the text (Remove extra spaces)
        passage = re.sub(r'\s+', ' ', passage)
        
        user_input = re.sub(r'\s+', ' ', user_input)
        duration = exam_content.duration

        # ✅ Minimal Calculation for CPCT
        if exam_type == "CPCT" or exam_type == "PRACTISE" or exam_type == "NTPC" or exam_type == "ARO":
            result = calculate_all_metrics(passage, user_input,duration)
        else:
            result = calculate_ssc_view(passage, user_input,duration)  # Default SSC method
            

      
        nwpm = result.get("net_wpm", 0)
        language = request.POST.get("language", "english") 
        scaled_score = calculate_scaled_score(nwpm,language, exam_type)
        if exam_type == "CPCT" or exam_type == "PRACTISE" or exam_type =="NTPC" or exam_type == "ARO":

            return render(request, "typing_app/result.html", {
                "exam_type": exam_type,
                "language": language,
                "errors": result["errors"],
                "backspaces": backspaces,
                "spaces": spaces,
                "scaled_score":scaled_score,
                "net_wpm": result["net_wpm"],
                "keystrokes_count": result["keystrokes_count"],
                "total_word_count": result["total_word_count"],
                "typed_word_count": result["typed_word_count"],
                "pending_word_count": result["pending_word_count"],
            })
        elif exam_type== "CGL" or exam_type == "CHSL":
            return render(request, "typing_app/result.html", {
                'exam_type': exam_type,
            'wpm': result['wpm'],
            'accuracy': result['accuracy'],
            'full_mistakes': result['full_mistakes'],
            'half_mistakes': result['half_mistakes'],
            'omissions': result['omissions'],
            'substitutions': result['substitutions'],
            'spelling_errors': result['spelling_errors'],
            'repetitions': result['repetitions'],
            'incomplete_words': result['incomplete_words'],
            'additions': result['additions'],
            'spacing': result['spacing'],
            'capitalization': result['capitalization'],
            'punctuation': result['punctuation'],
            'total_words_typed': result['total_words_typed'],
            'actual_key_depressions': result['actual_key_depressions'],
            'time_taken': result['time_taken'],
            })


def feedback_view(request):
    """Handles feedback form submissions."""
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for your feedback!")
            return redirect('home')  # Redirect back to the home page
        else:
            print(form.errors)
    else:
        print(request.method)
        form = FeedbackForm()

    return render(request, "typing_app/feedback.html", {"form": form})




# 🔹 Sample passages for different games
GAME_PASSAGES = {
    "speed_typing": [
        "The quick brown fox jumps over the lazy dog.",
        "Typing fast requires both speed and accuracy.",
        "Consistent practice helps improve typing skills.",
    ],
    "missing_word": [
        "Fill in the _____ words correctly to earn points.",
        "This game _____ word recognition and typing speed.",
    ],
}

def typing_games_view(request):
    """Renders the main typing games page with dynamic links."""
    games = [
        {"name": "Speed Typing Challenge", "slug": "speed_typing", "icon": "⚡"},
        {"name": "Key Hit Trainer", "slug": "key_hit_trainer", "icon": "🎯"},
        {"name": "Type the Missing Word", "slug": "missing_word", "icon": "📝"},
    ]
    # return render(request, "typing_app/typing_games.html", {"games": games})
    return render(request, "typing_app/coming_soon.html", {"games": games})

def typing_game_view(request, game_name):
    """Handles different typing games dynamically."""
    if game_name not in GAME_PASSAGES and game_name != "key_hit_trainer":
        return render(request, "typing_app/error.html", {"message": "Game not found"})

    # return render(request, "typing_app/typing_game.html", {
    #     "game_name": game_name,
    #     "passages": GAME_PASSAGES.get(game_name, []),
    # })
    return render(request, "typing_app/coming_soon.html", {
        "game_name": game_name,
        "passages": GAME_PASSAGES.get(game_name, []),
    })
    

def submit_typing_game_result(request, game_name):
    """Handles game result submissions dynamically."""
    if request.method == "POST":
        session_id = request.POST.get("session_id", str(uuid.uuid4()))
        passage = request.POST.get("passage", "")
        correct_hits = int(request.POST.get("correct_hits", 0))
        incorrect_hits = int(request.POST.get("incorrect_hits", 0))
        wpm = float(request.POST.get("wpm", 0))
        accuracy = float(request.POST.get("accuracy", 0))
        errors = int(request.POST.get("errors", 0))
        time_taken = int(request.POST.get("time_taken", 60))

        TypingGameResult.objects.create(
            game_name=game_name,
            session_id=session_id,
            passage=passage,
            correct_hits=correct_hits,
            incorrect_hits=incorrect_hits,
            wpm=wpm,
            accuracy=accuracy,
            errors=errors,
            time_taken=time_taken,
        )

        return JsonResponse({"message": "Result saved!", "session_id": session_id})

    return JsonResponse({"error": "Invalid request"}, status=400)



def blog_list(request):
    blogs = Blog.objects.filter(is_published=True)
    return render(request, 'blogs/blog_list.html', {'blogs': blogs})

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug, is_published=True)
    return render(request, 'blogs/blog_detail.html', {'blog': blog})



def learn(request):
    return render(request, "typing_app/coming_soon.html")

def languages(request):
    predefined_durations = [5, 10, 15, 20, 25, 30]
    languages = ["Hindi","English","German","French"]
    return render(request, "navbar/languages.html", {
        "exam_type":'PRACTISE',
        "languages": languages,
        "predefined_durations": predefined_durations,  # ✅ Allow user to select duration
    })




def privacy_policy(request):
    return render(request, 'typing_app/privacy_policy.html')

def terms_and_conditions(request):
    return render(request, 'typing_app/terms_and_conditions.html')





def ads_get(request, *args, **kwargs):
    line  =  "google.com, pub-7684260029366134, DIRECT, f08c47fec0942fa0"
    return HttpResponse(line)



