"""
Lunar birthday reminder ICS file generator.

Author: Shaowen Chen
Email: alvinchan2004@hotmail.com
Date: 2026-04-06
"""

from datetime import datetime
from pathlib import Path
import uuid
from src.utilities.logger import Loggable
import logging


class LunarBirthdayReminder(Loggable):
    """Generate ICS files for lunar calendar birthdays."""
    
    def __init__(self):
        """Initialize the lunar birthday reminder."""
        super().__init__(module_name="LunarBirthdayReminder", output_function=None)
    
    def _get_translations(self, language: str = 'en'):
        """Get translations for ICS content.
        
        Args:
            language: Language code ('en' or 'zh')
            
        Returns:
            Dictionary with translation keys
        """
        translations = {
            'en': {
                'birthday': "'s lunar birthday",
                'lunar': "Lunar: {}/{}/{}"
            },
            'zh': {
                'birthday': '的农历生日',
                'lunar': "农历: {}/{}/{}"
            }
        }
        return translations.get(language, translations['en'])
    
    def lunar_to_gregorian(self, lunar_year: int, lunar_month: int, lunar_day: int) -> datetime:
        """
        Convert lunar calendar date to Gregorian calendar date.
        
        Uses the lunarcalendar library for accurate Chinese lunar calendar conversion.
        
        Args:
            lunar_year: Year in lunar calendar
            lunar_month: Month in lunar calendar (1-12)
            lunar_day: Day in lunar calendar (1-30)
        
        Returns:
            datetime object in Gregorian calendar
        """
        try:
            # Import lunarcalendar library for accurate conversion
            from lunarcalendar import Converter, Lunar
            
            lunar = Lunar(lunar_year, lunar_month, lunar_day)
            solar = Converter.Lunar2Solar(lunar)
            gregorian_date = solar.to_date()
            return datetime(gregorian_date.year, gregorian_date.month, gregorian_date.day)
        except (ImportError, Exception) as e:
            self.output_and_log(f"lunarcalendar conversion failed: {e}. Using fallback conversion.", level=logging.WARNING)
            return self._fallback_lunar_to_gregorian(lunar_year, lunar_month, lunar_day)
    
    def _fallback_lunar_to_gregorian(self, lunar_year: int, lunar_month: int, lunar_day: int) -> datetime:
        """
        Fallback lunar to Gregorian conversion (simplified approximation).
        
        Note: This is an approximation and may not be 100% accurate.
        For production use, install lunisolar package.
        """
        # Simplified: lunar calendar is roughly 11 days behind gregorian
        # This is a rough estimate; actual conversion requires lookup tables
        approx_gregorian_day = lunar_day
        approx_gregorian_month = lunar_month
        approx_gregorian_year = lunar_year
        
        # Adjust for lunar year offset (rough approximation)
        if lunar_month > 2:
            approx_gregorian_year -= 1
        
        try:
            return datetime(approx_gregorian_year, approx_gregorian_month, min(approx_gregorian_day, 28))
        except ValueError:
            return datetime(approx_gregorian_year, approx_gregorian_month, 1)
    
    def generate_ics_content(
        self,
        name: str,
        lunar_month: int,
        lunar_day: int,
        repeat_years: int,
        start_year: int = None,
        language: str = 'en'
    ) -> str:
        """
        Generate ICS file content for lunar birthday reminders.
        
        Args:
            name: Person's name (e.g., "Max Musterman")
            lunar_month: Birth month in lunar calendar (1-12)
            lunar_day: Birth day in lunar calendar (1-30)
            repeat_years: Number of years to generate reminders for
            start_year: Start year (default: current year)
            language: Language code ('en' or 'zh')
        
        Returns:
            ICS file content as string
        """
        if start_year is None:
            start_year = datetime.now().year
        
        # ICS file header
        ics_content = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//Lunar Birthday Reminder//EN",
            f"CALSCALE:GREGORIAN",
            "METHOD:PUBLISH",
        ]
        
        # Generate events for each year
        for year_offset in range(repeat_years):
            current_year = start_year + year_offset
            
            # Convert lunar to gregorian
            gregorian_date = self.lunar_to_gregorian(
                current_year, lunar_month, lunar_day
            )
            
            # Create event
            event = self._create_vevent(
                name=name,
                date=gregorian_date,
                lunar_date=(current_year, lunar_month, lunar_day),
                language=language
            )
            ics_content.append(event)
        
        # ICS file footer
        ics_content.append("END:VCALENDAR")
        
        return "\n".join(ics_content)
    
    def _create_vevent(
        self,
        name: str,
        date: datetime,
        lunar_date: tuple,
        language: str = 'en'
    ) -> str:
        """
        Create a VEVENT block for ICS file.
        
        Args:
            name: Person's name
            date: Gregorian date
            lunar_date: Tuple of (year, month, day) in lunar calendar
            language: Language code ('en' or 'zh')
        
        Returns:
            VEVENT block as string
        """
        # Generate unique ID
        event_id = f"{uuid.uuid4()}@lunarbirthdayreminder.local"
        
        # Format date for ICS (YYYYMMDD for all-day events)
        date_str = date.strftime("%Y%m%d")
        now_str = datetime.now().strftime("%Y%m%dT%H%M%SZ")
        
        # Get translations
        trans = self._get_translations(language)
        
        # Title with lunar date reference
        lunar_year, lunar_month, lunar_day = lunar_date
        title = f"{name}{trans['birthday']}"
        description = trans['lunar'].format(lunar_year, lunar_month, lunar_day)
        
        event_lines = [
            "BEGIN:VEVENT",
            f"UID:{event_id}",
            f"DTSTAMP:{now_str}",
            f"DTSTART;VALUE=DATE:{date_str}",
            f"SUMMARY:{title}",
            f"DESCRIPTION:{description}",
            f"LOCATION:",
            "TRANSP:TRANSPARENT",
            "STATUS:CONFIRMED",
            "END:VEVENT",
        ]
        
        return "\n".join(event_lines)
    
    def save_ics_file(
        self,
        name: str,
        lunar_month: int,
        lunar_day: int,
        repeat_years: int,
        output_path: str = None,
        start_year: int = None,
        language: str = 'en'
    ) -> Path:
        """
        Generate and save ICS file for lunar birthday reminder.
        
        Args:
            name: Person's name
            lunar_month: Birth month in lunar calendar
            lunar_day: Birth day in lunar calendar
            repeat_years: Number of years to generate
            output_path: Output file path (default: ./output/{name}_birthday.ics)
            start_year: Start year (default: current year)
            language: Language code ('en' or 'zh')
        
        Returns:
            Path object of created file
        """
        # Generate ICS content
        ics_content = self.generate_ics_content(
            name=name,
            lunar_month=lunar_month,
            lunar_day=lunar_day,
            repeat_years=repeat_years,
            start_year=start_year,
            language=language
        )
        
        # Determine output path
        if output_path is None:
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)
            filename = f"{name.replace(' ', '_')}_birthday.ics"
            output_path = output_dir / filename
        else:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(ics_content)
        
        self.output_and_log(f"ICS file created: {output_path}", level=logging.INFO)    
        return output_path


# Example usage
if __name__ == "__main__":
    reminder = LunarBirthdayReminder()
    
    # Generate birthday reminder for Max Musterman
    # Lunar birthday: Month 1, Day 1 (first day of first lunar month)
    # Repeat for 5 years starting from 2026
    output_file = reminder.save_ics_file(
        name="Max Musterman",
        lunar_month=1,
        lunar_day=1,
        repeat_years=5,
        start_year=2026
    )
    print(f"Birthday reminder saved to: {output_file}")