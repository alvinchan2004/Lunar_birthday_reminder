"""
Views for the birthdays app - stateless ICS generation.

Author: Shaowen Chen
Email: alvinchan2004@hotmail.com
Date: 2026-04-08
"""

from django.shortcuts import render, redirect
from django.http import HttpResponse
from urllib.parse import quote
from .forms import BirthdayGeneratorForm
from .services import LunarBirthdayReminder
from .translations import TRANSLATIONS, get_text


def get_language(request):
    """Get current language from session, default to 'en'."""
    return request.session.get('language', 'en')


def set_language(request, language):
    """Set language in session and redirect back."""
    if language in TRANSLATIONS:
        request.session['language'] = language
    next_url = request.GET.get('next', '/')
    return redirect(next_url)


def index(request):
    """Display form and generate ICS file on POST.

    This view does not persist any data; it generates the ICS
    content on-the-fly and returns it as a downloadable file.
    """
    language = get_language(request)
    
    if request.method == 'POST':
        form = BirthdayGeneratorForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            lunar_month = form.cleaned_data['lunar_month']
            lunar_day = form.cleaned_data['lunar_day']
            repeat_years = form.cleaned_data['repeat_years']
            start_year = form.cleaned_data['start_year']

            service = LunarBirthdayReminder()
            content = service.generate_ics_content(
                name=name,
                lunar_month=lunar_month,
                lunar_day=lunar_day,
                repeat_years=repeat_years,
                start_year=start_year,
                language=language,
            )

            response = HttpResponse(content, content_type='text/calendar; charset=utf-8')
            # Use RFC 5987 encoding to support non-ASCII filenames (e.g., Chinese characters)
            if language == 'zh':
                filename = f"{name}_农历生日.ics"
            else:
                filename = f"{name}_lunar_birthday.ics"
            encoded_filename = quote(filename, safe='')
            response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{encoded_filename}'
            return response
    else:
        form = BirthdayGeneratorForm()

    context = {
        'form': form,
        'language': language,
        'translations': TRANSLATIONS[language],
        'available_languages': [('en', get_text('en', 'lang_en')), ('zh', get_text('en', 'lang_zh'))],
    }
    return render(request, 'birthdays/index.html', context)
