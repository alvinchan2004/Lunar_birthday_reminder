"""
Forms for the birthdays app - lunar birthday reminder form.

Author: Shaowen Chen
Email: alvinchan2004@hotmail.com
Date: 2026-04-08
"""

from django import forms


class BirthdayGeneratorForm(forms.Form):
    """Form for generating lunar birthday reminder ICS files."""
    
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter person\'s name'
        }),
        label='Name'
    )
    
    lunar_month = forms.IntegerField(
        min_value=1,
        max_value=12,
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Month (1-12)'
        }),
        label='Lunar Month'
    )
    
    lunar_day = forms.IntegerField(
        min_value=1,
        max_value=30,
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Day (1-30)'
        }),
        label='Lunar Day'
    )
    
    repeat_years = forms.IntegerField(
        min_value=1,
        max_value=100,
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Number of years to repeat'
        }),
        label='Repeat Years',
        help_text='Number of years to generate reminders for (max 100 years)',
        error_messages={
            'max_value': 'Repeat years cannot exceed 100. Please enter a value between 1 and 100.',
            'min_value': 'Repeat years must be at least 1.',
            'required': 'This field is required.',
            'invalid': 'Please enter a valid number.'
        }
    )
    
    start_year = forms.IntegerField(
        min_value=0,
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': f'Start year (e.g. {2024})'
        }),
        label='Start Year'
    )
