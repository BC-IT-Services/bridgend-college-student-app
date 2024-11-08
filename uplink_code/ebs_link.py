import math
from datetime import date, datetime
from decimal import Decimal
from academic_calendar import AcademicCalendar
from html import unescape
import logging
from pathlib import Path
from ebs_auth import EBSDBAuth
from dotenv import load_dotenv
import os

load_dotenv()

logger = logging.getLogger('EBS Link')

path = Path(__file__).resolve().parent / 'queries'

db_uid = os.environ.get("DB_UID") 
db_pwd =os.environ.get("DB_PWD")
database = os.environ.get("DB_DATABASE")
server = os.environ.get("DB_SERVER")

database = EBSDBAuth(queries_location=path)

def get_current_academic_year(date=datetime.now().date()):
    result = database.execute_query(query_name='get_current_year', params=date)
    if not result:
        logger.error("Failed to retrieve current year data")
        return {}

    current_year = result[0]
    start_date = current_year["start_date"].date()
    current_date = date.today()
    weeks_passed = math.ceil((current_date - start_date).days / 7)
    
    current_year.update({"current_week": weeks_passed})
    logger.info(f"Retrieved current year data - {current_year}")
    return current_year

current_year = get_current_academic_year(date.today())

def get_student_name(person_code):
    result = database.execute_query(query_name='get_student_name', params=person_code)
    result[0]['Personcode'] = str(Decimal(result[0]['Personcode']))
    logger.info(f"Retrieved name for {person_code} - {result}")
    return result

def get_student_timetable(person_code, year=current_year['session_code']):
    try:
        result = database.execute_query(query_name='get_student_timetable', params=(person_code, year))
        timetable_data = {}
        for row in result:
            if row["WEEK_PATTERN_TEXT_MATCH"][academic_calendar.get_week_number(row["PLANNED_START_DATE"])-1] == "1":
                dict_key = row["PLANNED_START_DATE"].strftime("%d/%m/%Y")
                event_id = str(row["REGISTER_EVENT_ID"])
                unique_event_id = f"{event_id}_{dict_key}"

                existing_event = next((event for event in timetable_data.get(dict_key, []) 
                                       if f"{event['event_id']}_{dict_key}" == unique_event_id), None)

                if existing_event:
                    existing_event["room"] += f", {fix_room_name(row['ROOM_CODE'])}"
                    continue
                else:
                    timetable_row = {
                        "event_id": event_id,
                        "start_time": row["PLANNED_START_DATE"],
                        "session_title": row["DESCRIPTION"],
                        "room": fix_room_name(row["ROOM_CODE"]),
                        "end_time": row["PLANNED_END_DATE"]
                    }
                if dict_key not in timetable_data:
                    timetable_data[dict_key] = [timetable_row]
                else:
                    timetable_data[dict_key].append(timetable_row)
        logger.info(f"Retrieved lite timetable data for {person_code}")
        
        sorted_timetable = {}

        for date, rows in timetable_data.items():
            sorted_rows = sorted(rows, key=lambda x: x["start_time"])
            sorted_timetable[date] = sorted_rows
    except Exception as e:
        logger.error(e.message)
        return {}

    return sorted_timetable

academic_calendar = AcademicCalendar(current_year["start_date"], current_year["end_date"])