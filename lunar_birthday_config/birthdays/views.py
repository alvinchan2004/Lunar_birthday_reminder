"""
Views for the birthdays app - stateless ICS generation.

Author: Shaowen Chen
Email: alvinchan2004@hotmail.com
Date: 2026-04-08
"""

from django.shortcuts import render
from django.http import HttpResponse
from .forms import BirthdayGeneratorForm
from .services import LunarBirthdayReminder


def index(request):
    """Display form and generate ICS file on POST.

    This view does not persist any data; it generates the ICS
    content on-the-fly and returns it as a downloadable file.
    """
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
            )

            response = HttpResponse(content, content_type='text/calendar; charset=utf-8')
            response['Content-Disposition'] = f'attachment; filename="{name}_birthday.ics"'
            return response
    else:
        form = BirthdayGeneratorForm()

    return render(request, 'birthdays/index.html', {'form': form})
from django.shortcuts import render

# Create your views here.
