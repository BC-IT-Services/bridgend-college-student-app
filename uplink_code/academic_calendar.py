from datetime import datetime, timedelta
from typing import Dict, Tuple

class AcademicCalendar:
    def __init__(self, start_date: datetime, end_date: datetime):
        self.start_date = start_date.date()
        self.end_date = end_date.date()
        self.week_dict = self._generate_week_dict()

    def _generate_week_dict(self) -> Dict[int, Tuple[datetime.date, datetime.date]]:
        week_dict = {}
        current_date = self.start_date
        week_number = 1

        while current_date <= self.end_date:
            week_start = current_date
            week_end = min(week_start + timedelta(days=6), self.end_date)
            week_dict[week_number] = (week_start, week_end)
            week_number += 1
            current_date = week_end + timedelta(days=1)

        return week_dict

    def get_week_number(self, date: datetime) -> int:
        date = date.date() if isinstance(date, datetime) else date
        for week, (start, end) in self.week_dict.items():
            if start <= date <= end:
                return week
        return -1  # Return -1 if the date is outside the academic year

    def print_calendar(self):
        for week, (start, end) in self.week_dict.items():
            print(f"Week {week}: {start} to {end}")