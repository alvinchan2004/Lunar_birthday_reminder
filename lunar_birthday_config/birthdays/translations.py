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
        'help_description': 'Enter the lunar calendar month and day to generate reminders for your birthdays. Lunar calendar dates follow the traditional Chinese calendar system. You can set how many years to repeat the reminders and specify the starting year for the generation. This tool will generate an ICS file that you can import into any calendar application that supports ICS format, such as Google Calendar, Apple Calendar, etc. For information on how to import ICS files, please search online for relevant tutorials. Usually you just need to select the "Import" function in your calendar application and select the generated ICS file.',
        'name_help': "The person's name",
        'lunar_month_help': 'Month in the lunar calendar (1-12)',
        'lunar_day_help': 'Day in the lunar month (1-30)',
        'start_year_help': 'The year to begin generating reminders',
        'help_title': 'Help',
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
        'help_description': '输入农历月份和日期以为您的生日生成提醒。农历日期遵循传统的中国日历系统。您可以设置重复提醒的年数，并指定生成的开始年份。此工具会生成一个ICS文件，您可以将其导入到任何支持ICS格式的日历应用中，如Google Calendar、Apple Calendar等。关于如何导入ICS文件，请上网搜索相关教程，通常在日历应用中选择“导入”功能并选择生成的ICS文件即可。',
        'name_help': '人物的名字',
        'lunar_month_help': '农历月份 (1-12)',
        'lunar_day_help': '农历日期 (1-30)',
        'start_year_help': '开始生成提醒的年份',
        'help_title': '使用说明'
    }
}


def get_text(language, key):
    """Get translated text for a key."""
    lang = language if language in TRANSLATIONS else 'en'
    return TRANSLATIONS[lang].get(key, key)
