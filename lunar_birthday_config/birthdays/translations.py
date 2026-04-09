"""
Simple translation dictionary for English and Chinese.
No i18n framework needed - just a simple dict!
"""

TRANSLATIONS = {
    'en': {
        'title': 'Lunar Birthday ICS Generator',
        'name': 'Name',
        'name_placeholder': "Enter person's name",
        'lunar_month': 'Lunar Month',
        'lunar_month_placeholder': 'Month (1-12)',
        'lunar_day': 'Lunar Day',
        'lunar_day_placeholder': 'Day (1-30)',
        'repeat_years': 'Repeat Years',
        'repeat_years_placeholder': 'Number of years to repeat',
        'repeat_years_help': 'Number of years to generate reminders for',
        'start_year': 'Start Year',
        'start_year_placeholder': 'Start year (e.g. 2024)',
        'generate_btn': 'Generate ICS',
        'lang_en': 'English',
        'lang_zh': '简体中文',
    },
    'zh': {
        'title': '农历生日日历提醒生成器',
        'name': '名字',
        'name_placeholder': '输入人物名字',
        'lunar_month': '农历月份',
        'lunar_month_placeholder': '月份 (1-12)',
        'lunar_day': '农历日期',
        'lunar_day_placeholder': '日期 (1-30)',
        'repeat_years': '重复年数',
        'repeat_years_placeholder': '生成提醒的年数',
        'repeat_years_help': '生成提醒的年数',
        'start_year': '开始年份',
        'start_year_placeholder': '开始年份 (例如 2024)',
        'generate_btn': '生成日历文件',
        'lang_en': 'English',
        'lang_zh': '简体中文',
    }
}


def get_text(language, key):
    """Get translated text for a key."""
    lang = language if language in TRANSLATIONS else 'en'
    return TRANSLATIONS[lang].get(key, key)
