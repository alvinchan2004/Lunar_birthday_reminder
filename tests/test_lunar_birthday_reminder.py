"""
Unit tests for LunarBirthdayReminder class.

Author: Shaowen Chen
Email: alvinchan2004@hotmail.com
Date: 2026-04-06
"""

import pytest
import tempfile
from datetime import datetime
from pathlib import Path
from lunar_birthday_config.birthdays.services import LunarBirthdayReminder


@pytest.fixture
def reminder():
    """Provide LunarBirthdayReminder instance."""
    return LunarBirthdayReminder()


@pytest.fixture
def temp_dir():
    """Provide temporary directory."""
    temp = tempfile.TemporaryDirectory()
    yield temp
    temp.cleanup()


def test_initialization(reminder):
    """Test that LunarBirthdayReminder initializes correctly."""
    assert reminder is not None


def test_fallback_lunar_to_gregorian_valid_date(reminder):
    """Test fallback conversion with valid lunar date."""
    # Lunar date: Year 2026, Month 1, Day 1
    result = reminder._fallback_lunar_to_gregorian(2026, 1, 1)
    
    assert isinstance(result, datetime)
    assert result.year == 2026  # Adjusted due to fallback logic
    assert result.month == 1
    assert result.day > 0


def test_fallback_lunar_to_gregorian_month_boundary(reminder):
    """Test fallback conversion near month boundary."""
    # Test when lunar_month <= 2 (no year adjustment)
    result = reminder._fallback_lunar_to_gregorian(2026, 2, 15)
    assert isinstance(result, datetime)
    assert result.month == 2


def test_fallback_lunar_to_gregorian_invalid_day(reminder):
    """Test fallback conversion with invalid day (should clamp to valid range)."""
    # Day 31 in month that only has 28 days in fallback
    result = reminder._fallback_lunar_to_gregorian(2026, 2, 31)
    assert isinstance(result, datetime)
    assert result.day <= 29


def test_generate_ics_content_structure(reminder):
    """Test that ICS content has correct structure."""
    ics_content = reminder.generate_ics_content(
        name="Test Person",
        lunar_month=1,
        lunar_day=1,
        repeat_years=2,
        start_year=2026
    )
    
    # Check header and footer
    assert "BEGIN:VCALENDAR" in ics_content
    assert "END:VCALENDAR" in ics_content
    assert "VERSION:2.0" in ics_content
    assert "PRODID:-//Lunar Birthday Reminder//EN" in ics_content


def test_generate_ics_content_events_count(reminder):
    """Test that ICS content contains correct number of events."""
    repeat_years = 3
    ics_content = reminder.generate_ics_content(
        name="Test Person",
        lunar_month=1,
        lunar_day=1,
        repeat_years=repeat_years,
        start_year=2026
    )
    
    # Count VEVENT blocks
    event_count = ics_content.count("BEGIN:VEVENT")
    assert event_count == repeat_years


def test_generate_ics_content_with_default_year(reminder):
    """Test that ICS generation uses current year by default."""
    current_year = datetime.now().year
    ics_content = reminder.generate_ics_content(
        name="Test Person",
        lunar_month=1,
        lunar_day=1,
        repeat_years=1
    )
    
    # Should contain current year
    assert "BEGIN:VEVENT" in ics_content
    assert ics_content is not None


def test_create_vevent_format(reminder):
    """Test that VEVENT is created with correct ICS format."""
    test_date = datetime(2026, 2, 14)
    lunar_date = (2026, 1, 1)
    
    vevent = reminder._create_vevent(
        name="John Doe",
        date=test_date,
        lunar_date=lunar_date
    )
    
    # Check required ICS fields
    assert "BEGIN:VEVENT" in vevent
    assert "END:VEVENT" in vevent
    assert "UID:" in vevent
    assert "DTSTAMP:" in vevent
    assert "DTSTART;VALUE=DATE:" in vevent
    assert "SUMMARY:John Doe's lunar birthday" in vevent
    assert "DESCRIPTION:Lunar: 2026/1/1" in vevent


def test_create_vevent_date_format(reminder):
    """Test that VEVENT date is in correct format (YYYYMMDD)."""
    test_date = datetime(2026, 2, 14)
    lunar_date = (2026, 1, 1)
    
    vevent = reminder._create_vevent(
        name="Test Person",
        date=test_date,
        lunar_date=lunar_date
    )
    
    # Check date format
    assert "DTSTART;VALUE=DATE:20260214" in vevent


def test_save_ics_file_creates_file(reminder, temp_dir):
    """Test that save_ics_file creates a file."""
    output_path = reminder.save_ics_file(
        name="Test Person",
        lunar_month=1,
        lunar_day=1,
        repeat_years=1,
        output_path=f"{temp_dir.name}/test_birthday.ics",
        start_year=2026
    )
    
    # Check file exists
    assert output_path.exists()
    assert output_path.is_file()


def test_save_ics_file_content(reminder, temp_dir):
    """Test that saved ICS file contains valid content."""
    output_path = reminder.save_ics_file(
        name="Max Musterman",
        lunar_month=1,
        lunar_day=1,
        repeat_years=2,
        output_path=f"{temp_dir.name}/max_birthday.ics",
        start_year=2026
    )
    
    # Read file and verify content
    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    assert "BEGIN:VCALENDAR" in content
    assert "END:VCALENDAR" in content
    assert "Max Musterman's lunar birthday" in content
    assert content.count("BEGIN:VEVENT") == 2


def test_save_ics_file_creates_directory(reminder, temp_dir):
    """Test that save_ics_file creates output directory if it doesn't exist."""
    nested_path = f"{temp_dir.name}/nested/dir/structure/birthday.ics"
    output_path = reminder.save_ics_file(
        name="Test Person",
        lunar_month=1,
        lunar_day=1,
        repeat_years=1,
        output_path=nested_path,
        start_year=2026
    )
    
    # Check nested directories were created
    assert output_path.exists()
    assert output_path.parent.exists()


def test_save_ics_file_default_path(reminder, temp_dir):
    """Test that save_ics_file uses default path when not specified."""
    import os
    original_cwd = os.getcwd()
    os.chdir(temp_dir.name)
    
    try:
        output_path = reminder.save_ics_file(
            name="Test Person",
            lunar_month=1,
            lunar_day=1,
            repeat_years=1,
            start_year=2026
        )
        
        # Check default path structure
        assert output_path.exists()
        assert "output" in str(output_path)
        assert "Test_Person_birthday.ics" in str(output_path)
    finally:
        os.chdir(original_cwd)


def test_save_ics_file_special_characters_in_name(reminder, temp_dir):
    """Test that save_ics_file handles special characters in names."""
    output_path = reminder.save_ics_file(
        name="Jean-Pierre Dupont",
        lunar_month=5,
        lunar_day=15,
        repeat_years=1,
        output_path=f"{temp_dir.name}/jean_birthday.ics",
        start_year=2026
    )
    
    assert output_path.exists()
    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "Jean-Pierre Dupont's lunar birthday" in content


def test_generate_multiple_years(reminder):
    """Test generating reminders for multiple years."""
    repeat_years = 10
    ics_content = reminder.generate_ics_content(
        name="Test Person",
        lunar_month=3,
        lunar_day=15,
        repeat_years=repeat_years,
        start_year=2026
    )
    
    # Verify multiple events
    assert ics_content.count("BEGIN:VEVENT") == repeat_years
    assert "SUMMARY:Test Person's lunar birthday" in ics_content


# Integration tests
def test_end_to_end_workflow(reminder, temp_dir):
    """Test complete workflow from generation to file creation."""
    # Generate and save
    output_path = reminder.save_ics_file(
        name="Maria Garcia",
        lunar_month=6,
        lunar_day=8,
        repeat_years=5,
        output_path=f"{temp_dir.name}/maria_birthday.ics",
        start_year=2024
    )
    
    # Verify file
    assert output_path.exists()
    
    # Read and validate content
    with open(output_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # Check structure
    assert any("BEGIN:VCALENDAR" in line for line in lines)
    assert any("END:VCALENDAR" in line for line in lines)
    assert any("Maria Garcia's lunar birthday" in line for line in lines)
    assert any("Lunar: 2028/6/8" in line for line in lines)

